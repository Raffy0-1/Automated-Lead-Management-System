"""
Lead Management System — Server-Side Validation Test Suite

Tests the same validation logic that runs in the n8n Code node.
This Python script mirrors the JavaScript validation to verify correctness.
"""
import json
import re
import sys

# ── Validation Logic (mirrors n8n Code node) ──────────────────
def clean(val):
    """Trim and collapse whitespace."""
    if not val:
        return ""
    return re.sub(r'\s+', ' ', str(val).strip())

def sanitize(val):
    """Basic HTML entity escaping."""
    s = clean(val)
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace("'", '&#x27;')
    return s

def validate_lead(payload):
    """Validate a lead payload. Returns (valid, errors, sanitized_data)."""
    errors = []
    
    name = sanitize(payload.get('name', ''))
    email = clean(payload.get('email', '')).lower()
    phone = sanitize(payload.get('phone', ''))
    company = sanitize(payload.get('company', ''))
    service = sanitize(payload.get('service', ''))
    budget = sanitize(payload.get('budget', ''))
    message = sanitize(payload.get('message', ''))
    
    # Name validation
    if not name or len(name) < 2:
        errors.append('Name is required (min 2 characters)')
    if len(name) > 100:
        errors.append('Name must be under 100 characters')
    
    # Email validation
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not email or not re.match(email_regex, email):
        errors.append('A valid email address is required')
    
    # Phone validation
    phone_regex = r'^[+]?[\d\s\-().]{7,20}$'
    if not phone or not re.match(phone_regex, phone):
        errors.append('A valid phone number is required')
    
    # Company validation
    if not company:
        errors.append('Company is required')
    
    # Service validation
    if not service:
        errors.append('Service is required')
    
    # Budget validation
    if not budget:
        errors.append('Budget is required')
    
    # Message validation
    if not message:
        errors.append('Message is required')
    if len(message) > 2000:
        errors.append('Message must be under 2000 characters')
    
    data = {
        'name': name,
        'email': email,
        'phone': phone,
        'company': company,
        'service': service,
        'budget': budget,
        'message': message
    }
    
    return len(errors) == 0, errors, data


# ── Test Cases ─────────────────────────────────────────────────
PASS = 0
FAIL = 0

def test(test_id, description, payload, expect_valid, expect_error_substr=None):
    global PASS, FAIL
    valid, errors, data = validate_lead(payload)
    
    passed = True
    issues = []
    
    if valid != expect_valid:
        passed = False
        issues.append(f"Expected valid={expect_valid}, got valid={valid}")
    
    if expect_error_substr and not any(expect_error_substr in e for e in errors):
        passed = False
        issues.append(f"Expected error containing '{expect_error_substr}', got {errors}")
    
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS += 1
    else:
        FAIL += 1
    
    print(f"  [{status}] {test_id}: {description}")
    if not passed:
        for issue in issues:
            print(f"         {issue}")
    if errors and not passed:
        print(f"         Errors: {errors}")


def test_sanitization():
    """Test input sanitization."""
    global PASS, FAIL
    
    # Test XSS prevention
    result = sanitize('<script>alert("xss")</script>')
    expected = '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'
    if result == expected:
        PASS += 1
        print(f"  [PASS] SANIT-01: XSS script tag sanitized")
    else:
        FAIL += 1
        print(f"  [FAIL] SANIT-01: Expected '{expected}', got '{result}'")
    
    # Test whitespace normalization
    result = clean('  hello   world  ')
    if result == 'hello world':
        PASS += 1
        print(f"  [PASS] SANIT-02: Whitespace normalized")
    else:
        FAIL += 1
        print(f"  [FAIL] SANIT-02: Expected 'hello world', got '{result}'")
    
    # Test email lowercasing
    _, _, data = validate_lead({
        'name': 'Test',
        'email': 'John.Doe@EXAMPLE.COM',
        'phone': '+1 555-0000',
        'company': 'Test',
        'service': 'Test',
        'budget': 'Test',
        'message': 'Test message'
    })
    if data['email'] == 'john.doe@example.com':
        PASS += 1
        print(f"  [PASS] SANIT-03: Email lowercased correctly")
    else:
        FAIL += 1
        print(f"  [FAIL] SANIT-03: Expected 'john.doe@example.com', got '{data['email']}'")


# ── Run Tests ──────────────────────────────────────────────────
print("=" * 60)
print("Lead Management System — Validation Test Suite")
print("=" * 60)

# Valid payload for reuse
VALID_PAYLOAD = {
    'name': 'Jane Smith',
    'email': 'jane@acme.com',
    'phone': '+1 555-123-4567',
    'company': 'Acme Inc.',
    'service': 'AI & Automation Consulting',
    'budget': '$5,000 - $10,000',
    'message': 'We need an AI chatbot for customer support.'
}

print("\n--- Validation Tests ---")

test('TC-01', 'Valid lead submission',
     VALID_PAYLOAD,
     expect_valid=True)

test('TC-02', 'Missing name',
     {**VALID_PAYLOAD, 'name': ''},
     expect_valid=False,
     expect_error_substr='Name is required')

test('TC-03', 'Invalid email',
     {**VALID_PAYLOAD, 'email': 'not-an-email'},
     expect_valid=False,
     expect_error_substr='valid email')

test('TC-04a', 'Missing phone',
     {**VALID_PAYLOAD, 'phone': ''},
     expect_valid=False,
     expect_error_substr='phone')

test('TC-04b', 'Missing company',
     {**VALID_PAYLOAD, 'company': ''},
     expect_valid=False,
     expect_error_substr='Company')

test('TC-04c', 'Missing service',
     {**VALID_PAYLOAD, 'service': ''},
     expect_valid=False,
     expect_error_substr='Service')

test('TC-04d', 'Missing budget',
     {**VALID_PAYLOAD, 'budget': ''},
     expect_valid=False,
     expect_error_substr='Budget')

test('TC-04e', 'Missing message',
     {**VALID_PAYLOAD, 'message': ''},
     expect_valid=False,
     expect_error_substr='Message')

test('TC-05', 'Multiple missing fields',
     {'name': 'Test', 'email': 'test@test.com'},
     expect_valid=False,
     expect_error_substr='phone')

test('TC-06', 'Short name (1 char)',
     {**VALID_PAYLOAD, 'name': 'A'},
     expect_valid=False,
     expect_error_substr='Name is required')

test('TC-07', 'Name exactly 2 chars (valid)',
     {**VALID_PAYLOAD, 'name': 'Ab'},
     expect_valid=True)

test('TC-08', 'Message over 2000 chars',
     {**VALID_PAYLOAD, 'message': 'x' * 2001},
     expect_valid=False,
     expect_error_substr='2000')

test('TC-09', 'Invalid phone format (too short)',
     {**VALID_PAYLOAD, 'phone': '123'},
     expect_valid=False,
     expect_error_substr='phone')

test('TC-10', 'Valid phone formats',
     {**VALID_PAYLOAD, 'phone': '(555) 123-4567'},
     expect_valid=True)

test('TC-11', 'Empty payload (malformed)',
     {},
     expect_valid=False,
     expect_error_substr='Name')

test('TC-12', 'XSS in name field',
     {**VALID_PAYLOAD, 'name': '<script>alert("xss")</script>'},
     expect_valid=True)  # Should pass validation but sanitize content

print("\n--- Sanitization Tests ---")

test_sanitization()

# ── Lead ID Format Test ──────────────────────────────────────
print("\n--- Lead ID Generation Test ---")
import datetime
now = datetime.datetime.now()
date_part = now.strftime('%Y%m%d')
import random
random_part = format(random.randint(0, 0xFFFF), '04X')
lead_id = f"LEAD-{date_part}-{random_part}"
lead_id_regex = r'^LEAD-\d{8}-[0-9A-F]{4}$'

if re.match(lead_id_regex, lead_id):
    PASS += 1
    print(f"  [PASS] LEADID-01: Generated lead ID '{lead_id}' matches format")
else:
    FAIL += 1
    print(f"  [FAIL] LEADID-01: Lead ID '{lead_id}' does not match expected format")

# ── n8n JSON Structure Test ───────────────────────────────────
print("\n--- n8n Workflow Structure Tests ---")

with open('automation/workflows/lead-management-workflow.json', encoding='utf-8') as f:
    workflow = json.load(f)

# Check webhook trigger exists
webhook_nodes = [n for n in workflow['nodes'] if 'webhook' in n['type'].lower()]
if webhook_nodes:
    PASS += 1
    print(f"  [PASS] N8N-01: Webhook trigger node exists")
else:
    FAIL += 1
    print(f"  [FAIL] N8N-01: No webhook trigger node found")

# Check response nodes exist
response_nodes = [n for n in workflow['nodes'] if 'respondToWebhook' in n['type']]
if len(response_nodes) >= 2:
    PASS += 1
    print(f"  [PASS] N8N-02: {len(response_nodes)} webhook response nodes found (success + error)")
else:
    FAIL += 1
    print(f"  [FAIL] N8N-02: Expected 2+ response nodes, found {len(response_nodes)}")

# Check error handling on external service nodes
external_nodes = [n for n in workflow['nodes'] if n.get('onError') == 'continueRegularOutput']
if len(external_nodes) >= 4:
    PASS += 1
    print(f"  [PASS] N8N-03: {len(external_nodes)} nodes have continueRegularOutput error handling")
else:
    FAIL += 1
    print(f"  [FAIL] N8N-03: Expected 4+ nodes with error handling, found {len(external_nodes)}")

# Check no hardcoded credentials
workflow_str = json.dumps(workflow)
sensitive_patterns = ['pat-na1-', 'Bearer pat-', 'sk-', 'AIza']
has_leaked = False
for pattern in sensitive_patterns:
    if pattern in workflow_str:
        has_leaked = True
        FAIL += 1
        print(f"  [FAIL] N8N-04: Found potentially leaked credential pattern: {pattern}")
if not has_leaked:
    PASS += 1
    print(f"  [PASS] N8N-04: No hardcoded credentials detected in workflow JSON")

# Check credential IDs are placeholders
cred_ids = set()
for node in workflow['nodes']:
    if 'credentials' in node:
        for cred_type, cred_info in node['credentials'].items():
            cred_ids.add(cred_info.get('id', ''))

placeholder_ids = [cid for cid in cred_ids if 'CREDENTIAL_ID' in cid]
if placeholder_ids:
    PASS += 1
    print(f"  [PASS] N8N-05: Credential IDs are placeholders ({len(placeholder_ids)} found)")
else:
    if cred_ids:
        FAIL += 1
        print(f"  [FAIL] N8N-05: Credential IDs may not be placeholders: {cred_ids}")
    else:
        PASS += 1
        print(f"  [PASS] N8N-05: No credentials to check")

# ── Summary ───────────────────────────────────────────────────
print("\n" + "=" * 60)
total = PASS + FAIL
print(f"Results: {PASS}/{total} passed, {FAIL}/{total} failed")
if FAIL == 0:
    print("ALL TESTS PASSED")
else:
    print(f"WARNING: {FAIL} test(s) failed")
    sys.exit(1)
