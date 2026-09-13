# Automated Lead Management System

> **DigiHust AI & Automation** — Internship Assignment  
> A production-quality system that captures leads from a web form and automatically processes them through validation, storage, email, notifications, and CRM integration using n8n automation.

---

## Table of Contents

- [Project Purpose](#project-purpose)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [n8n Setup](#n8n-setup)
- [Google Sheets Setup](#google-sheets-setup)
- [Gmail Setup](#gmail-setup)
- [Discord Setup](#discord-setup)
- [CRM Setup (HubSpot)](#crm-setup-hubspot)
- [Running the System](#running-the-system)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

---

## Project Purpose

This system automates the complete lead management lifecycle:

1. **Capture** — A professional web form collects lead information
2. **Validate** — Server-side validation ensures data quality
3. **Store** — Leads are stored in Google Sheets with unique IDs
4. **Notify** — Customer receives a confirmation email via Gmail
5. **Alert** — Internal team gets a Discord notification
6. **CRM** — Contact is created in HubSpot CRM
7. **Track** — Status of every service is tracked per lead

All integrations run through an **n8n automation workflow** with robust error handling — if one service fails, the others continue, and the failure is recorded.

---

## Architecture

```
                    ┌─────────────┐
                    │  Web Form   │
                    │  (Frontend) │
                    └──────┬──────┘
                           │ POST JSON
                    ┌──────▼──────┐
                    │   n8n       │
                    │  Webhook    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Validate   │
                    │  & Sanitize │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Generate ID │
                    │ + Timestamp │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Check     │
                    │  Duplicate  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Store Lead  │
                    │ (G. Sheets) │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼───┐ ┌──────▼──────┐
       │   Gmail     │ │ Disc │ │  HubSpot    │
       │ (Customer)  │ │ ord  │ │  (CRM)      │
       └──────┬──────┘ └──┬───┘ └──────┬──────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │   Update    │
                    │   Status    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Respond    │
                    │  to Client  │
                    └─────────────┘
```

For detailed architecture documentation, see [docs/architecture/architecture.md](docs/architecture/architecture.md).

---

## Features

| Feature | Implementation |
|---------|---------------|
| Lead capture form | HTML5 + CSS3 + Vanilla JS, clean light theme design |
| Client-side validation | Real-time field validation with visual feedback |
| Server-side validation | n8n Code node validates + sanitizes all fields |
| Unique lead ID | `LEAD-YYYYMMDD-XXXX` format with ISO timestamp |
| Duplicate detection | Email-based lookup in Google Sheets before storage |
| Data storage | Google Sheets with 14-column schema |
| Customer email | Professional HTML confirmation via Gmail |
| Team notification | Rich Discord embed with all lead details |
| CRM integration | HubSpot contact creation via REST API |
| Status tracking | Per-service status columns (sent/failed/pending) |
| Error handling | Graceful degradation — services fail independently |
| Error logging | Specific error messages recorded per lead |

---

## Prerequisites

| Tool | Version | Required |
|------|---------|----------|
| Modern web browser | Chrome/Firefox/Edge | Yes |
| n8n | v1.0+ (Cloud or Docker) | Yes |
| Google Account | Free | Yes |
| Discord Account + Server | Free | Yes |
| HubSpot Account | Free CRM tier | Yes |
| Node.js | 18+ (optional, for local dev server) | Optional |
| Docker | 20+ (optional, for self-hosted n8n) | Optional |

---

## Project Structure

```
Lead-management-system/
├── index.html                  # Root landing page (GitHub Pages ready)
├── frontend/
│   ├── index.html              # Lead capture form
│   ├── css/
│   │   └── styles.css          # Design system & styles
│   ├── js/
│   │   ├── config.js           # Frontend configuration (no secrets)
│   │   └── app.js              # Validation & submission logic
│   └── assets/                 # Images and static assets
├── automation/
│   └── workflows/
│       ├── lead-management-workflow.json  # n8n workflow (importable)
│       └── workflow-diagram.md            # Visual workflow documentation
├── database/
│   ├── google-sheets-template.md  # Google Sheets column headers & schema
│   └── schema.sql                 # Optional PostgreSQL schema
├── docs/
│   ├── architecture/
│   │   └── architecture.md     # System architecture documentation
│   ├── api-documentation.md    # Webhook API specification
│   ├── test-cases.md           # 20 test cases (server + client)
│   └── setup-guide.md          # Step-by-step service setup
├── screenshots/                # Screenshots for documentation
├── demo/                       # Demo script and materials
│   └── demo-script.md
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
└── README.md                   # Project README
```

---

## Installation

### 1. Clone or Download

```bash
git clone https://github.com/Raffy0-1/Automated-Lead-Management-System.git
cd Automated-Lead-Management-System
```

### 2. Copy Environment Template

```bash
cp .env.example .env
```

### 3. Import n8n Workflow

1. Open your n8n instance
2. Go to **Workflows** -> **Import from File**
3. Select `automation/workflows/lead-management-workflow.json`
4. Configure credentials (see sections below)

### 4. Set Up Google Sheets

Follow [Google Sheets Setup](#google-sheets-setup) below.

### 5. Configure All Services

Follow the [Setup Guide](docs/setup-guide.md) for detailed instructions.

---

## Configuration

All configuration is done through:

1. **n8n Credentials** — OAuth tokens, API keys (stored encrypted in n8n)
2. **n8n Environment Variables** — Service URLs, sheet IDs
3. **Frontend config.js** — Webhook URL (not a secret)

### Security Principles

- No secrets in frontend JavaScript
- No hardcoded API keys, tokens, or passwords
- All credentials in n8n's encrypted credential store
- Server-side validation is authoritative
- Input sanitization at both client and server level

---

## Environment Variables

See [`.env.example`](.env.example) for the complete list. Key variables:

| Variable | Description | Where Used |
|----------|-------------|------------|
| `GOOGLE_SHEETS_ID` | Spreadsheet ID from the Google Sheets URL | n8n env vars |
| `DISCORD_WEBHOOK_URL` | Discord channel webhook URL | n8n env vars |
| `HUBSPOT_BASE_URL` | HubSpot API base URL | n8n env vars |
| `APP_MODE` | `production` or `test` | n8n env vars |

> **Note:** Most credentials (OAuth tokens, API keys) are stored in n8n's built-in credential store, not in environment variables. The `.env.example` documents what's needed for reference.

---

## n8n Setup

See [docs/setup-guide.md -> Section 2](docs/setup-guide.md#2-n8n-setup) for full instructions.

**Quick start with n8n Cloud:**
1. Create a free account at [n8n.cloud](https://app.n8n.cloud/register)
2. Import the workflow JSON
3. Configure credentials for each service
4. Activate the workflow

---

## Google Sheets Setup

See [docs/setup-guide.md -> Section 4](docs/setup-guide.md#4-google-sheets-setup).

1. Create a new spreadsheet
2. Name the tab `Leads`
3. Add 14 column headers (see [database/google-sheets-template.md](database/google-sheets-template.md))
4. Connect via OAuth2 in n8n

---

## Gmail Setup

See [docs/setup-guide.md -> Section 5](docs/setup-guide.md#5-gmail-setup-in-n8n).

1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 credential in n8n
3. Authorize Gmail access

---

## Discord Setup

See [docs/setup-guide.md -> Section 6](docs/setup-guide.md#6-discord-webhook-setup).

1. Create a webhook in your Discord server
2. Add the URL as an n8n environment variable

---

## CRM Setup (HubSpot)

See [docs/setup-guide.md -> Section 7](docs/setup-guide.md#7-hubspot-crm-setup).

1. Create a free HubSpot account
2. Create a Private App with contacts.read/write scopes
3. Add the access token as a Header Auth credential in n8n

The CRM integration is **modular** — the workflow uses a generic HTTP Request node, so you can swap HubSpot for any CRM with a REST API by changing the URL and payload format.

---

## Running the System

### Start the Frontend

```bash
# Option 1: Python
python -m http.server 8080

# Option 2: Node.js
npx serve . -l 8080

# Option 3: GitHub Pages
# Visit https://raffy0-1.github.io/Automated-Lead-Management-System/
```

### Activate the n8n Workflow

1. Open the workflow in n8n
2. Toggle **Active** to ON
3. Note the production webhook URL

### Update Frontend Config

Edit `frontend/js/config.js` with your webhook URL:
```javascript
WEBHOOK_URL: "https://your-instance.app.n8n.cloud/webhook/lead-form",
```

---

## Testing

See [docs/test-cases.md](docs/test-cases.md) for 20 detailed test cases.

### Quick cURL Test

```bash
curl -X POST https://YOUR-INSTANCE/webhook/lead-form \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"+1 555-000-0000","company":"Test Corp","service":"AI Consulting","budget":"$1,000 – $5,000","message":"Test submission."}'
```

---

## API Documentation

See [docs/api-documentation.md](docs/api-documentation.md) for the complete webhook API specification.

**Endpoint:** `POST /webhook/lead-form`  
**Content-Type:** `application/json`  
**Response:** JSON with `lead_id`, `status`, and service statuses

---

## Troubleshooting

See [docs/setup-guide.md -> Section 10](docs/setup-guide.md#10-troubleshooting).

Common issues:
- **Failed to fetch** — Webhook URL wrong or workflow not active
- **CORS errors** — Use a local dev server instead of `file://`
- **Google Sheets errors** — Verify sheet ID and tab name `Leads`
- **Email not sending** — Re-authenticate Gmail credential in n8n

---

## Limitations

1. **Google Sheets** as a database is suitable for low-to-medium volume (< 1000 leads/day). For high volume, migrate to PostgreSQL using the included `schema.sql`.
2. **No rate limiting** on the webhook — add a reverse proxy for production.
3. **No CAPTCHA** — add hCaptcha or reCAPTCHA for production forms.
4. **Single email template** — customization requires editing the n8n Gmail node.
5. **No webhook authentication** — configure Basic Auth or Header Auth in n8n for production.
6. **Free Gmail** has a 500 emails/day limit.

---

## Future Improvements

1. **Rate limiting** via reverse proxy (Nginx/Caddy)
2. **CAPTCHA** integration (hCaptcha)
3. **Webhook authentication** (HMAC signature verification)
4. **PostgreSQL** database for production scale
5. **Lead scoring** using AI/ML classification
6. **Dashboard** for lead analytics and pipeline visualization
7. **Multi-language** email templates
8. **SMS notifications** via Twilio
9. **Calendar booking** integration
10. **A/B testing** on form design
11. **File attachments** in the form
12. **Lead assignment** rules for sales team routing

---

## License

This project was created as part of the DigiHust AI & Automation internship assignment.

---

## Author

DigiHust AI & Automation Intern  
September 2026
