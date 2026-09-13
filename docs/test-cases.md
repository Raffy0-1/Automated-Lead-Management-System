# Test Cases — Lead Management System

## Test Case Summary

| ID | Test Case | Type | Priority |
|----|-----------|------|----------|
| TC-01 | Valid lead submission | Happy path | P0 |
| TC-02 | Missing name | Validation | P0 |
| TC-03 | Invalid email | Validation | P0 |
| TC-04 | Missing required field | Validation | P0 |
| TC-05 | Duplicate email | Business logic | P0 |
| TC-06 | Gmail failure | Error handling | P1 |
| TC-07 | Google Sheets failure | Error handling | P1 |
| TC-08 | Discord failure | Error handling | P1 |
| TC-09 | CRM failure | Error handling | P1 |
| TC-10 | Malformed JSON | Validation | P0 |

---

## Detailed Test Cases

### TC-01: Valid Lead Submission

| Attribute | Value |
|-----------|-------|
| **Description** | Submit a complete, valid lead form |
| **Preconditions** | All services configured and active |
| **Input** | `{"name":"Jane Smith","email":"jane@acme.com","phone":"+1 555-123-4567","company":"Acme Inc.","service":"AI & Automation Consulting","budget":"$5,000 – $10,000","message":"We need an AI chatbot for customer support."}` |
| **Expected HTTP** | `200 OK` |
| **Expected Response** | `{"success":true,"lead_id":"LEAD-XXXXXXXX-XXXX","status":"new","is_duplicate":false,...}` |
| **Expected Side Effects** | ① New row in Google Sheets ② Confirmation email to jane@acme.com ③ Discord embed posted ④ HubSpot contact created |
| **Test Method** | cURL / Frontend form |
| **Status** | ⬜ Not yet tested (requires credentials) |

---

### TC-02: Missing Name

| Attribute | Value |
|-----------|-------|
| **Description** | Submit form without the `name` field |
| **Input** | `{"email":"test@example.com","phone":"+1 555-000-0000","company":"Test","service":"AI Consulting","budget":"$1,000","message":"Test."}` |
| **Expected HTTP** | `400 Bad Request` |
| **Expected Response** | `{"success":false,"message":"Validation failed","errors":["Name is required (min 2 characters)"]}` |
| **Test Method** | cURL |
| **Status** | ⬜ Not yet tested |

---

### TC-03: Invalid Email

| Attribute | Value |
|-----------|-------|
| **Description** | Submit form with an invalid email address |
| **Input** | `{"name":"Test User","email":"not-an-email","phone":"+1 555-000-0000","company":"Test","service":"AI Consulting","budget":"$1,000","message":"Test."}` |
| **Expected HTTP** | `400 Bad Request` |
| **Expected Response** | `{"success":false,"message":"Validation failed","errors":["A valid email address is required"]}` |
| **Test Method** | cURL |
| **Status** | ⬜ Not yet tested |

---

### TC-04: Missing Required Field (Multiple)

| Attribute | Value |
|-----------|-------|
| **Description** | Submit form with multiple missing required fields |
| **Input** | `{"name":"Test","email":"test@test.com"}` |
| **Expected HTTP** | `400 Bad Request` |
| **Expected Response** | `{"success":false,"message":"Validation failed","errors":["A valid phone number is required","Company is required","Service is required","Budget is required","Message is required"]}` |
| **Test Method** | cURL |
| **Status** | ⬜ Not yet tested |

---

### TC-05: Duplicate Email

| Attribute | Value |
|-----------|-------|
| **Description** | Submit the same email address twice |
| **Preconditions** | First submission (TC-01) already stored in Google Sheets |
| **Input** | Same as TC-01 (same email `jane@acme.com`) |
| **Expected HTTP** | `200 OK` |
| **Expected Response** | `{"success":true,"lead_id":"LEAD-XXXXXXXX-XXXX","status":"duplicate","is_duplicate":true,...}` |
| **Expected Side Effects** | ① Row stored with `status=duplicate` ② Email still sent ③ Discord notification still sent ④ CRM may return `duplicate_in_crm` |
| **Test Method** | cURL (submit twice) |
| **Status** | ⬜ Not yet tested (requires credentials) |

---

### TC-06: Gmail Failure

| Attribute | Value |
|-----------|-------|
| **Description** | Gmail fails to send (e.g., invalid credentials or quota exceeded) |
| **Preconditions** | Gmail credential removed or invalid |
| **Input** | Valid lead payload |
| **Expected HTTP** | `200 OK` (lead still stored) |
| **Expected Response** | `services.email = "failed"` |
| **Expected Side Effects** | ① Lead stored in Sheets ② `email_status = failed` ③ `error_message` contains Gmail error ④ Discord and CRM still attempted |
| **Test Method** | Remove Gmail credential, submit lead |
| **Status** | ⬜ Not yet tested |

---

### TC-07: Google Sheets Failure

| Attribute | Value |
|-----------|-------|
| **Description** | Google Sheets API fails (e.g., invalid sheet ID) |
| **Preconditions** | Google Sheets credential removed or sheet ID invalid |
| **Input** | Valid lead payload |
| **Expected HTTP** | `200 OK` or `500` depending on failure point |
| **Expected Behavior** | ① Error recorded ② Downstream services still attempted ③ Status update may fail (no row to update) |
| **Test Method** | Change sheet ID to invalid value |
| **Status** | ⬜ Not yet tested |

---

### TC-08: Discord Failure

| Attribute | Value |
|-----------|-------|
| **Description** | Discord webhook URL is invalid or unreachable |
| **Preconditions** | Discord webhook URL set to invalid value |
| **Input** | Valid lead payload |
| **Expected HTTP** | `200 OK` |
| **Expected Response** | `services.notification = "failed"` |
| **Expected Side Effects** | ① Lead stored ② Email sent ③ `notification_status = failed` ④ CRM still attempted |
| **Test Method** | Set invalid Discord webhook URL in env |
| **Status** | ⬜ Not yet tested |

---

### TC-09: CRM Failure

| Attribute | Value |
|-----------|-------|
| **Description** | HubSpot API call fails (e.g., invalid token) |
| **Preconditions** | HubSpot token invalid or empty |
| **Input** | Valid lead payload |
| **Expected HTTP** | `200 OK` |
| **Expected Response** | `services.crm = "failed"` |
| **Expected Side Effects** | ① Lead stored ② Email sent ③ Discord notified ④ `crm_status = failed` ⑤ Error message recorded |
| **Test Method** | Set invalid HubSpot token |
| **Status** | ⬜ Not yet tested |

---

### TC-10: Malformed JSON

| Attribute | Value |
|-----------|-------|
| **Description** | Send a request with invalid JSON body |
| **Input** | `{invalid json` |
| **Expected HTTP** | `400 Bad Request` or `500 Internal Server Error` |
| **Expected Behavior** | n8n returns error response; no data stored |
| **Test Method** | cURL with malformed body |
| **Status** | ⬜ Not yet tested |

---

## Client-Side Validation Tests

These tests verify the frontend JavaScript validation before any network request is made.

| ID | Test | Input | Expected Behavior |
|----|------|-------|-------------------|
| CS-01 | Empty form submission | All fields empty | All fields show validation errors, form not submitted |
| CS-02 | Short name | `name="A"` | Error: "Name must be at least 2 characters" |
| CS-03 | Invalid email format | `email="abc"` | Error: "Please enter a valid email address" |
| CS-04 | Invalid phone | `phone="123"` | Error: "Please enter a valid phone number" |
| CS-05 | No service selected | Service dropdown empty | Error: "Please select a service" |
| CS-06 | No budget selected | Budget dropdown empty | Error: "Please select a budget range" |
| CS-07 | Empty message | Message field empty | Error: "Please describe your project" |
| CS-08 | Valid form | All fields valid | Form submits, loading state shown |
| CS-09 | Character counter | Type in message field | Counter updates (e.g., "50 / 2000") |
| CS-10 | Real-time validation | Fill field, blur, fix | Error shown on blur, cleared on fix |

---

## Test Execution Log

_Fill in after running tests._

| Test ID | Date | Tester | Result | Notes |
|---------|------|--------|--------|-------|
| | | | | |
