# Workflow Diagram — Lead Management System

## High-Level Flow

```mermaid
flowchart TD
    A["🌐 Web Form\n(frontend/index.html)"] -->|POST JSON| B["⚡ Webhook Trigger\n(/webhook/lead-form)"]
    B --> C["🔍 Validate Input\n(sanitize + validate)"]
    C --> D{"✅ Valid?"}
    D -->|No| E["❌ Respond 400\n(validation errors)"]
    D -->|Yes| F["🆔 Generate Lead ID\n(LEAD-YYYYMMDD-XXXX)"]
    F --> G["🔎 Check Duplicate\n(search email in Sheets)"]
    G --> H["📊 Process Duplicate\n(flag if exists)"]
    H --> I["📝 Store Lead\n(append to Google Sheets)"]
    I --> J["🔀 Prepare Downstream"]
    J --> K["📧 Send Customer Email\n(Gmail confirmation)"]
    J --> L["🔔 Send Discord\n(webhook embed)"]
    J --> M["🏢 CRM Create Contact\n(HubSpot API)"]
    K --> N["📊 Aggregate Results"]
    L --> N
    M --> N
    N --> O["📝 Update Lead Status\n(update Sheets row)"]
    O --> P["✅ Respond 200\n(lead_id + status)"]

    style A fill:#6366f1,color:#fff
    style B fill:#818cf8,color:#fff
    style D fill:#f59e0b,color:#000
    style E fill:#ef4444,color:#fff
    style P fill:#22c55e,color:#fff
    style K fill:#4285f4,color:#fff
    style L fill:#5865f2,color:#fff
    style M fill:#ff7a59,color:#fff
```

## Data Flow

```mermaid
flowchart LR
    subgraph Input
        A["JSON Payload"]
    end
    subgraph Processing
        B["Validated Data"]
        C["Lead ID + Timestamp"]
        D["Duplicate Flag"]
    end
    subgraph Storage
        E["Google Sheets Row"]
    end
    subgraph Notifications
        F["Gmail\n(customer)"]
        G["Discord\n(internal team)"]
    end
    subgraph CRM
        H["HubSpot Contact"]
    end

    A --> B --> C --> D --> E
    E --> F
    E --> G
    E --> H
```

## Error Handling Flow

```mermaid
flowchart TD
    A["Downstream Service Call"] --> B{"Success?"}
    B -->|Yes| C["Set status = sent/synced"]
    B -->|No| D["Set status = failed"]
    D --> E["Record error message"]
    C --> F["Aggregate Results"]
    E --> F
    F --> G["Update Google Sheets\n(status columns)"]
    G --> H["Respond to Webhook\n(include service statuses)"]
```

## Node Reference

| # | Node | Type | Purpose |
|---|------|------|---------|
| 1 | Webhook Trigger | `webhook` | Receives POST from frontend form |
| 2 | Validate Input | `code` | Server-side validation + sanitization |
| 3 | Is Valid? | `if` | Routes valid vs. invalid payloads |
| 4 | Respond Validation Error | `respondToWebhook` | Returns 400 with error details |
| 5 | Generate Lead ID | `code` | Creates unique ID + ISO timestamp |
| 6 | Check Duplicate | `googleSheets` (search) | Looks up existing leads by email |
| 7 | Process Duplicate Check | `code` | Flags duplicates, sets status |
| 8 | Store Lead in Sheets | `googleSheets` (append) | Writes full lead row |
| 9 | Prepare Downstream | `code` | Checks store result, passes data forward |
| 10 | Send Customer Email | `gmail` | HTML confirmation email to customer |
| 11 | Send Discord Notification | `httpRequest` | Rich embed to Discord channel |
| 12 | CRM Create Contact | `httpRequest` | Creates contact in HubSpot CRM |
| 13 | Aggregate Results | `code` | Collects statuses from all services |
| 14 | Update Lead Status | `googleSheets` (update) | Updates status columns in sheet |
| 15 | Respond Success | `respondToWebhook` | Returns 200 with lead_id + statuses |
