/**
 * Lead Management System — Frontend Configuration
 * 
 * This file contains non-secret configuration for the frontend.
 * The webhook URL is not a secret — it is a public endpoint.
 * Authentication is handled server-side via webhook secret validation.
 */

const APP_CONFIG = Object.freeze({

  // ── Webhook endpoint ───────────────────────────────────────
  // Update this to your n8n webhook URL after activating the workflow.
  // This URL is safe to include in frontend code — it is a public endpoint.
  // Server-side validation (webhook secret) prevents abuse.
  WEBHOOK_URL: "https://raffy1.app.n8n.cloud/webhook-test/lead-form",

  // ── Form settings ─────────────────────────────────────────
  SERVICES: [
    "AI & Automation Consulting",
    "Chatbot Development",
    "Process Automation (RPA)",
    "Data Analytics & BI",
    "Custom Software Development",
    "Cloud Infrastructure",
    "Digital Marketing Automation",
    "Other"
  ],

  BUDGETS: [
    "Under $1,000",
    "$1,000 – $5,000",
    "$5,000 – $10,000",
    "$10,000 – $25,000",
    "$25,000 – $50,000",
    "$50,000+",
    "Not sure yet"
  ],

  // ── Validation ─────────────────────────────────────────────
  VALIDATION: {
    NAME_MIN_LENGTH: 2,
    NAME_MAX_LENGTH: 100,
    EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    PHONE_REGEX: /^[+]?[\d\s\-().]{7,20}$/,
    MESSAGE_MAX_LENGTH: 2000,
    COMPANY_MAX_LENGTH: 200
  },

  // ── UI ─────────────────────────────────────────────────────
  SUBMIT_TIMEOUT_MS: 30000,   // 30 seconds
  SUCCESS_REDIRECT_DELAY_MS: 5000
});
