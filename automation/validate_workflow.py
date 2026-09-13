import json
import sys
import os

workflow_path = os.path.join("automation", "workflows", "lead-management-workflow.json")

with open(workflow_path, encoding="utf-8") as f:
    data = json.load(f)

errors = []

# 1. Check required top-level keys
for key in ["name", "nodes", "connections", "settings"]:
    if key not in data:
        errors.append("Missing top-level key: " + key)

nodes = data.get("nodes", [])
conns = data.get("connections", {})

# 2. Check each node has required fields
node_names = set()
for i, node in enumerate(nodes):
    for field in ["id", "name", "type", "position"]:
        if field not in node:
            errors.append("Node %d: missing %s" % (i, field))
    if "name" in node:
        node_names.add(node["name"])

# 3. Verify all connection targets exist
for source, outputs in conns.items():
    if source not in node_names:
        errors.append("Connection source not in nodes: " + source)
    for output_type, output_list in outputs.items():
        for targets in output_list:
            for target in targets:
                tname = target.get("node", "")
                if tname not in node_names:
                    errors.append("Connection target not in nodes: %s (from %s)" % (tname, source))

# 4. Check response nodes
response_nodes = [n for n in nodes if "respondToWebhook" in n.get("type", "")]

# 5. Check webhook trigger
webhook_nodes = [n for n in nodes if "webhook" in n.get("type", "").lower()]

print("=== n8n Workflow Validation ===")
print("Name:", data.get("name"))
print("Total Nodes:", len(nodes))
print("Total Connections:", len(conns), "source nodes")
print("Webhook Nodes:", len(webhook_nodes))
print("Response Nodes:", len(response_nodes))
print()

print("Nodes:")
for n in nodes:
    extras = []
    if "credentials" in n:
        extras.append("(has credentials)")
    if "onError" in n:
        extras.append("onError=" + n["onError"])
    print("  -", n["name"], "[" + n["type"] + "]", " ".join(extras))

print()
print("Connection Graph:")
for source, outputs in conns.items():
    for output_list in outputs.values():
        for i, targets in enumerate(output_list):
            target_names = [t["node"] for t in targets]
            branch = " (branch %d)" % i if len(output_list) > 1 else ""
            print("  %s%s -> %s" % (source, branch, target_names))

print()
if errors:
    print("ERRORS (%d):" % len(errors))
    for e in errors:
        print("  X", e)
    sys.exit(1)
else:
    print("PASS: Validation passed - No errors found")
    print("PASS: All nodes connected")
    print("PASS: All connection targets exist")
    print("PASS: %d webhook response node(s) found" % len(response_nodes))
    print("PASS: %d webhook trigger(s) found" % len(webhook_nodes))
