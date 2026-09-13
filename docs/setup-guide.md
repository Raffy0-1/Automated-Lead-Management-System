# Setup Guide — Lead Management System

Step-by-step instructions to configure all external services.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [n8n Setup](#2-n8n-setup)
3. [Google Cloud Setup (Sheets + Gmail)](#3-google-cloud-setup)
4. [Google Sheets Setup](#4-google-sheets-setup)
5. [Gmail Setup in n8n](#5-gmail-setup-in-n8n)
6. [Discord Webhook Setup](#6-discord-webhook-setup)
7. [HubSpot CRM Setup](#7-hubspot-crm-setup)
8. [Frontend Configuration](#8-frontend-configuration)
9. [End-to-End Testing](#9-end-to-end-testing)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

- A Google account (free)
- A Discord account and a server you control (free)
- A HubSpot account (free CRM tier)
- n8n (self-hosted via Docker, or n8n Cloud free tier)
- A modern web browser
- (Optional) Node.js for local development server

---

## 2. n8n Setup

### Option A: n8n Cloud (Recommended for Quick Start)

1. Go to [https://app.n8n.cloud/register](https://app.n8n.cloud/register)
2. Create a free account (includes 5 active workflows)
3. After login, note your instance URL: `https://YOUR-NAME.app.n8n.cloud`

### Option B: Self-Hosted (Docker)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

Access at: `http://localhost:5678`

### Import the Workflow

1. In n8n, click **Workflows** → **Add Workflow** → **Import from File**
2. Select `automation/workflows/lead-management-workflow.json`
3. The workflow will import with all nodes connected
4. **Do not activate yet** — configure credentials first

---

## 3. Google Cloud Setup

You need a Google Cloud project with Sheets and Gmail APIs to connect n8n.

### 3.1 Create a Google Cloud Project

1. Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Click **Select a Project** → **New Project**
3. Name: `Lead Management System`
4. Click **Create**

### 3.2 Enable APIs

1. Go to **APIs & Services** → **Library**
2. Search and enable:
   - **Google Sheets API**
   - **Gmail API**

### 3.3 Create OAuth2 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth Client ID**
3. If prompted, configure the **OAuth Consent Screen**:
   - User Type: **External** (or Internal if using Google Workspace)
   - App Name: `Lead Management System`
   - Add your email as a test user
4. Back in Credentials → **Create OAuth Client ID**:
   - Application type: **Web Application**
   - Authorized redirect URIs:
     - For n8n Cloud: `https://YOUR-NAME.app.n8n.cloud/rest/oauth2-credential/callback`
     - For self-hosted: `http://localhost:5678/rest/oauth2-credential/callback`
5. Copy the **Client ID** and **Client Secret**

### 3.4 Configure in n8n

#### Google Sheets Credential
1. In n8n, go to **Credentials** → **Add Credential**
2. Search for **Google Sheets OAuth2 API**
3. Paste the Client ID and Client Secret
4. Click **Connect my account** → sign in with Google → grant permissions
5. Name it: `Google Sheets OAuth2`

---

## 4. Google Sheets Setup

1. Go to [Google Sheets](https://sheets.google.com/) and create a new spreadsheet
2. Rename it: **Lead Management Database**
3. Rename the first tab: **Leads**
4. In Row 1, enter these headers (one per cell, A1 through N1):

```
lead_id | timestamp | name | email | phone | company | service | budget | message | status | email_status | notification_status | crm_status | error_message
```

5. Copy the **Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit
   ```

6. In n8n, update all Google Sheets nodes:
   - Click each Google Sheets node (Check Duplicate, Store Lead, Update Status)
   - Set the **Document** to your spreadsheet (by ID or search)
   - Set the **Sheet** to `Leads`
   - Select your `Google Sheets OAuth2` credential

---

## 5. Gmail Setup in n8n

1. In n8n, go to **Credentials** → **Add Credential**
2. Search for **Gmail OAuth2 API**
3. Use the same Client ID and Client Secret from Step 3.3
4. Click **Connect my account** → sign in → grant Gmail permissions
5. Name it: `Gmail OAuth2`
6. In the workflow, click the **Send Customer Email** node:
   - Select the `Gmail OAuth2` credential
   - Verify the email template looks correct

---

## 6. Discord Webhook Setup

1. Open Discord and go to the server where you want notifications
2. Go to **Server Settings** → **Integrations** → **Webhooks**
3. Click **New Webhook**
4. Name it: `Lead Management Bot`
5. Select the channel for notifications
6. Click **Copy Webhook URL**
7. In n8n:
   - Click the **Send Discord Notification** node
   - The URL uses `$env.DISCORD_WEBHOOK_URL`
   - Go to **Settings** → **Environment Variables** and add:
     ```
     DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
     ```
   - Alternatively, replace the URL expression with the webhook URL directly in the node

---

## 7. HubSpot CRM Setup

### 7.1 Create a Free HubSpot Account

1. Go to [https://app.hubspot.com/signup-hubspot/crm](https://app.hubspot.com/signup-hubspot/crm)
2. Create a free account

### 7.2 Create a Private App (API Token)

1. In HubSpot, go to **Settings** (gear icon)
2. Navigate to **Integrations** → **Private Apps**
3. Click **Create a private app**
4. Name: `Lead Management System`
5. Under **Scopes**, add:
   - `crm.objects.contacts.write`
   - `crm.objects.contacts.read`
6. Click **Create App**
7. Copy the **Access Token** (starts with `pat-`)

### 7.3 Configure in n8n

1. In n8n, go to **Credentials** → **Add Credential**
2. Search for **Header Auth**
3. Configure:
   - Name: `HubSpot Bearer Token`
   - Header Name: `Authorization`
   - Header Value: `Bearer pat-YOUR-TOKEN-HERE`
4. In the workflow, click the **CRM Create Contact** node:
   - Select the `HubSpot Bearer Token` credential

---

## 8. Frontend Configuration

1. Open `frontend/js/config.js`
2. Update `WEBHOOK_URL` to your n8n webhook URL:
   ```javascript
   WEBHOOK_URL: "https://YOUR-NAME.app.n8n.cloud/webhook/lead-form",
   ```
3. This URL becomes active after you activate the workflow in n8n

### Serving the Frontend

#### Option A: Open directly
Double-click `frontend/index.html` to open in browser.

> ⚠️ Some browsers block `fetch()` from `file://` URLs. Use a local server instead.

#### Option B: Local development server
```bash
# Using Python
cd frontend
python -m http.server 3000

# Using Node.js
npx serve frontend -l 3000
```

Access at: `http://localhost:3000`

---

## 9. End-to-End Testing

### Step 1: Activate the n8n Workflow
1. In n8n, open the workflow
2. Click **Active** toggle (top-right) to enable it
3. Note the production webhook URL shown

### Step 2: Test with cURL
```bash
curl -X POST https://YOUR-INSTANCE/webhook/lead-form \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1 555-000-0000",
    "company": "Test Corp",
    "service": "AI Consulting",
    "budget": "$1,000 – $5,000",
    "message": "End-to-end test submission."
  }'
```

### Step 3: Verify Each Service
- [ ] **Google Sheets**: Check the Leads tab for the new row
- [ ] **Gmail**: Check test@example.com inbox for confirmation email
- [ ] **Discord**: Check the notification channel for the embed
- [ ] **HubSpot**: Check Contacts for the new contact

### Step 4: Test Frontend
1. Open `http://localhost:3000` (or your hosted URL)
2. Fill in the form and submit
3. Verify success message appears with lead ID

---

## 10. Troubleshooting

### "Failed to fetch" Error
- Check that the webhook URL in `config.js` is correct
- Ensure the n8n workflow is **activated**
- Check browser console for CORS errors

### Google Sheets Not Working
- Verify the Sheet ID is correct
- Ensure the tab is named exactly `Leads` (case-sensitive)
- Check that headers in Row 1 match exactly
- Re-authenticate the Google Sheets credential in n8n

### Gmail Not Sending
- Check that Gmail API is enabled in Google Cloud Console
- Re-authenticate the Gmail credential in n8n
- Check Gmail daily sending limits (500/day for free Gmail)
- Verify the email address in the credential matches the sender

### Discord Webhook Error
- Test the webhook URL directly:
  ```bash
  curl -X POST YOUR_DISCORD_WEBHOOK_URL \
    -H "Content-Type: application/json" \
    -d '{"content": "Test message"}'
  ```
- Ensure the webhook is not deleted in Discord

### HubSpot CRM Error
- Verify the access token is valid and not expired
- Ensure the Private App has `crm.objects.contacts.write` scope
- Check if the contact already exists (duplicate error)
- Test the token:
  ```bash
  curl https://api.hubapi.com/crm/v3/objects/contacts?limit=1 \
    -H "Authorization: Bearer pat-YOUR-TOKEN"
  ```

### n8n Workflow Not Triggering
- Ensure the workflow is **Active** (not just saved)
- Check n8n execution logs for errors
- Verify the webhook path matches the URL in `config.js`
