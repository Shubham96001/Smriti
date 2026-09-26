CREATE TABLE IF NOT EXISTS caregiver_relationships (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient_profiles(id) ON DELETE CASCADE,
    caregiver_id UUID NOT NULL REFERENCES caregiver_profiles(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'revoked')),
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMPTZ,
    UNIQUE (patient_id, caregiver_id)
);
CREATE TABLE IF NOT EXISTS hcw_scopes (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient_profiles(id) ON DELETE CASCADE,
    hcw_id UUID NOT NULL REFERENCES hcw_profiles(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'revoked')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (patient_id, hcw_id)
);