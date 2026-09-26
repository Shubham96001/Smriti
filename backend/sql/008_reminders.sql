CREATE TABLE IF NOT EXISTS reminders (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient_profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    remind_at TIMESTAMPTZ NOT NULL,
    recurrence TEXT NOT NULL DEFAULT 'once' CHECK (recurrence IN ('once', 'daily', 'weekly')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);