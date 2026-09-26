CREATE TABLE IF NOT EXISTS caregiver_alerts (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient_profiles(id) ON DELETE CASCADE,
    caregiver_id UUID REFERENCES caregiver_profiles(id) ON DELETE CASCADE,
    alert_type TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);