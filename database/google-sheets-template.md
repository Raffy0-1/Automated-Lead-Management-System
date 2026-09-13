# Google Sheets Database Template

## Setup Instructions

1. Create a new Google Spreadsheet
2. Rename the first sheet tab to **`Leads`**
3. In row 1, add the following column headers **exactly** as shown:

## Column Headers (Row 1)

| Column | Header | Data Type | Description |
|--------|--------|-----------|-------------|
| A | `lead_id` | String | Unique ID: `LEAD-YYYYMMDD-XXXX` |
| B | `timestamp` | ISO 8601 String | Submission timestamp |
| C | `name` | String | Full name (sanitized) |
| D | `email` | String | Email (lowercased) |
| E | `phone` | String | Phone number (cleaned) |
| F | `company` | String | Company name |
| G | `service` | String | Service requested |
| H | `budget` | String | Budget range selected |
| I | `message` | String | Project description |
| J | `status` | String | `new` / `duplicate` / `contacted` / `qualified` |
| K | `email_status` | String | `sent` / `failed` / `pending` |
| L | `notification_status` | String | `sent` / `failed` / `pending` |
| M | `crm_status` | String | `synced` / `failed` / `pending` / `mock` / `duplicate_in_crm` |
| N | `error_message` | String | Error details (empty if no errors) |

## Quick-Copy Header Row

Copy and paste this into row 1 (tab-separated):

```
lead_id	timestamp	name	email	phone	company	service	budget	message	status	email_status	notification_status	crm_status	error_message
```

## Example Data Row

```
LEAD-20260910-A3F2	2026-09-10T07:30:00.000Z	John Doe	john@acme.com	+1 555-123-4567	Acme Inc.	AI & Automation Consulting	$5,000 – $10,000	We need help automating our sales pipeline.	new	sent	sent	synced	
```

## Status Values Reference

### `status`
| Value | Meaning |
|-------|---------|
| `new` | Fresh lead, just received |
| `duplicate` | Email already exists in the system |
| `contacted` | Sales team has reached out |
| `qualified` | Lead is qualified for follow-up |

### `email_status`
| Value | Meaning |
|-------|---------|
| `pending` | Not yet attempted |
| `sent` | Confirmation email sent successfully |
| `failed` | Email sending failed (see error_message) |

### `notification_status`
| Value | Meaning |
|-------|---------|
| `pending` | Not yet attempted |
| `sent` | Discord notification sent |
| `failed` | Discord webhook failed (see error_message) |

### `crm_status`
| Value | Meaning |
|-------|---------|
| `pending` | Not yet attempted |
| `synced` | Contact created in HubSpot |
| `failed` | CRM API call failed |
| `mock` | Running in test/mock mode |
| `duplicate_in_crm` | Contact already exists in CRM |

## Important Notes

1. **Do not rename columns** — the n8n workflow references columns by header name
2. **Do not delete the header row** — the Google Sheets node needs it
3. The `lead_id` column is used as the match key for status updates
4. Keep the sheet tab named exactly **`Leads`** (case-sensitive)
