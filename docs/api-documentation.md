# API Documentation — Lead Management System

## Webhook Endpoint

### `POST /webhook/lead-form`

Receives lead form submissions and processes them through the automation pipeline.

**Base URL:** Your n8n instance URL (e.g., `https://your-instance.app.n8n.cloud`)

**Full URL:** `{BASE_URL}/webhook/lead-form`

---

## Request

### Headers

| Header | Value | Required |
|--------|-------|----------|
| `Content-Type` | `application/json` | ✅ Yes |

### Body

```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "company": "string",
  "service": "string",
  "budget": "string",
  "message": "string"
}
```

### Field Specifications

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | ✅ | 2–100 characters |
| `email` | string | ✅ | Valid email format |
| `phone` | string | ✅ | 7–20 characters, digits/spaces/dashes/parens/plus |
| `company` | string | ✅ | 1–200 characters |
| `service` | string | ✅ | Non-empty |
| `budget` | string | ✅ | Non-empty |
| `message` | string | ✅ | 1–2000 characters |

### Example Request

```bash
curl -X POST https://your-instance.app.n8n.cloud/webhook/lead-form \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@acme.com",
    "phone": "+1 555-123-4567",
    "company": "Acme Inc.",
    "service": "AI & Automation Consulting",
    "budget": "$5,000 – $10,000",
    "message": "We need help automating our sales pipeline."
  }'
```

---

## Responses

### 200 OK — Success

Returned when the lead is processed successfully (even if some downstream services fail).

```json
{
  "success": true,
  "lead_id": "LEAD-20260910-A3F2",
  "status": "new",
  "is_duplicate": false,
  "message": "Thank you! Your inquiry has been received.",
  "services": {
    "email": "sent",
    "notification": "sent",
    "crm": "synced"
  }
}
```

### 200 OK — Duplicate Lead

```json
{
  "success": true,
  "lead_id": "LEAD-20260910-B7C1",
  "status": "duplicate",
  "is_duplicate": true,
  "message": "Lead received (duplicate detected — previously submitted)",
  "services": {
    "email": "sent",
    "notification": "sent",
    "crm": "duplicate_in_crm"
  }
}
```

### 200 OK — Partial Failure

When one or more downstream services fail, the lead is still stored and a 200 is returned with the service statuses indicating which services failed.

```json
{
  "success": true,
  "lead_id": "LEAD-20260910-D4E9",
  "status": "new",
  "is_duplicate": false,
  "message": "Thank you! Your inquiry has been received.",
  "services": {
    "email": "sent",
    "notification": "failed",
    "crm": "failed"
  }
}
```

### 400 Bad Request — Validation Error

Returned when one or more required fields fail validation.

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    "A valid email address is required",
    "Phone number is required"
  ]
}
```

---

## Response Fields

### Success Response

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Always `true` for 200 responses |
| `lead_id` | string | Unique identifier: `LEAD-YYYYMMDD-XXXX` |
| `status` | string | `new` or `duplicate` |
| `is_duplicate` | boolean | Whether the email was previously submitted |
| `message` | string | Human-readable status message |
| `services` | object | Status of each downstream service |
| `services.email` | string | `sent` / `failed` / `pending` |
| `services.notification` | string | `sent` / `failed` / `pending` |
| `services.crm` | string | `synced` / `failed` / `pending` / `duplicate_in_crm` |

### Error Response

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Always `false` for 400 responses |
| `message` | string | `"Validation failed"` |
| `errors` | string[] | Array of specific validation error messages |

---

## Error Codes

| HTTP Status | Meaning | When |
|-------------|---------|------|
| `200` | Success | Lead processed (check `services` for partial failures) |
| `400` | Bad Request | Validation failed (missing/invalid fields) |
| `500` | Internal Server Error | n8n workflow error (unexpected) |

---

## Rate Limiting

The webhook endpoint does not natively enforce rate limiting. For production deployments:

1. Use a reverse proxy (Nginx/Caddy) with rate limiting
2. Recommended: 10 requests per minute per IP
3. Add CAPTCHA (e.g., hCaptcha) to the frontend form

---

## CORS

The webhook is configured with `allowedOrigins: "*"` for development. For production:

```
allowedOrigins: "https://your-frontend-domain.com"
```

---

## Testing with cURL

### Valid Submission
```bash
curl -X POST http://localhost:5678/webhook-test/lead-form \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1 555-000-0000",
    "company": "Test Corp",
    "service": "AI Consulting",
    "budget": "$1,000 – $5,000",
    "message": "This is a test submission."
  }'
```

### Missing Required Field
```bash
curl -X POST http://localhost:5678/webhook-test/lead-form \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "phone": "+1 555-000-0000"
  }'
```

### Invalid Email
```bash
curl -X POST http://localhost:5678/webhook-test/lead-form \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "not-an-email",
    "phone": "+1 555-000-0000",
    "company": "Test Corp",
    "service": "AI Consulting",
    "budget": "$1,000 – $5,000",
    "message": "Test."
  }'
```
