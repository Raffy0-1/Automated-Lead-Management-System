-- ============================================================
-- Lead Management System — PostgreSQL Schema (Optional)
-- ============================================================
-- This schema mirrors the Google Sheets structure.
-- Use this if you later migrate from Google Sheets to PostgreSQL.
-- ============================================================

CREATE TABLE IF NOT EXISTS leads (
    id                  SERIAL PRIMARY KEY,
    lead_id             VARCHAR(25) UNIQUE NOT NULL,    -- LEAD-YYYYMMDD-XXXX
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    name                VARCHAR(100) NOT NULL,
    email               VARCHAR(255) NOT NULL,
    phone               VARCHAR(30) NOT NULL,
    company             VARCHAR(200) NOT NULL,
    service             VARCHAR(200) NOT NULL,
    budget              VARCHAR(100) NOT NULL,
    message             TEXT NOT NULL,
    status              VARCHAR(20) NOT NULL DEFAULT 'new'
                        CHECK (status IN ('new', 'duplicate', 'contacted', 'qualified', 'closed')),
    email_status        VARCHAR(20) NOT NULL DEFAULT 'pending'
                        CHECK (email_status IN ('pending', 'sent', 'failed')),
    notification_status VARCHAR(20) NOT NULL DEFAULT 'pending'
                        CHECK (notification_status IN ('pending', 'sent', 'failed')),
    crm_status          VARCHAR(30) NOT NULL DEFAULT 'pending'
                        CHECK (crm_status IN ('pending', 'synced', 'failed', 'mock', 'duplicate_in_crm')),
    error_message       TEXT DEFAULT ''
);

-- Index for duplicate detection by email
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads (email);

-- Index for lead_id lookups (used by status updates)
CREATE INDEX IF NOT EXISTS idx_leads_lead_id ON leads (lead_id);

-- Index for status filtering
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads (status);
