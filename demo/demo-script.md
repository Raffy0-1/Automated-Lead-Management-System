# Demo Script — Lead Management System

## Duration: 1–2 Minutes

---

## Demo Outline

### 1. Introduction (15 seconds)

"This is the Automated Lead Management System built for DigiHust AI & Automation.
It captures leads from a web form and automatically processes them through validation,
storage in Google Sheets, email confirmation, Discord team notifications, and
HubSpot CRM integration — all orchestrated by n8n."

### 2. Show the Form (15 seconds)

- Open `http://localhost:3000` in browser
- Point out: responsive design, dark mode, form fields
- Show: dropdown options for Service and Budget

### 3. Demonstrate Validation (15 seconds)

- Click Submit with empty form → show validation errors
- Type invalid email → show real-time validation
- Fix errors → show green valid states

### 4. Submit a Lead (20 seconds)

- Fill in complete, valid data:
  - Name: "Demo User"
  - Email: "demo@digihust.com"
  - Phone: "+1 555-123-4567"
  - Company: "DigiHust Demo"
  - Service: "AI & Automation Consulting"
  - Budget: "$5,000 – $10,000"
  - Message: "Live demo of the lead management system"
- Click Submit → show loading state → show success with lead ID

### 5. Show Results (30 seconds)

- **Google Sheets**: Switch to spreadsheet, show new row with all data and status columns
- **Gmail**: Show confirmation email in inbox (professional HTML template)
- **Discord**: Show rich embed notification in the channel
- **HubSpot**: Show new contact in CRM

### 6. Show n8n Workflow (15 seconds)

- Switch to n8n
- Show the workflow diagram with all connected nodes
- Point out the execution log showing green checkmarks

### 7. Wrap Up (10 seconds)

"The system handles validation, duplicate detection, error handling per service,
and status tracking — all with zero hardcoded credentials. Thank you!"

---

## Preparation Checklist

Before recording:

- [ ] Frontend running on `localhost:3000`
- [ ] n8n workflow active
- [ ] Google Sheets open with headers
- [ ] Gmail inbox open
- [ ] Discord channel open
- [ ] HubSpot contacts page open
- [ ] Clear any test data from Google Sheets
- [ ] Browser in dark mode for consistency

## Recording Tips

- Use a screen recorder (OBS, Loom, or OS built-in)
- Resolution: 1920x1080
- Record browser tabs in order: Form → Sheets → Gmail → Discord → HubSpot → n8n
- Keep mouse movements smooth and deliberate
