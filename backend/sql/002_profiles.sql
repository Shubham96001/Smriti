CREATE TABLE IF NOT EXISTS patient_profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    date_of_birth DATE,
    gender TEXT,
    preferred_language TEXT NOT NULL DEFAULT 'en',
    contact_phone TEXT,
    address TEXT,
    emergency_contact_name TEXT,
    emergency_contact_phone TEXT,
    consent_acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
    baseline_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS caregiver_profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    contact_phone TEXT,
    relationship_type TEXT,
    invitation_code TEXT NOT NULL UNIQUE DEFAULT UPPER(SUBSTRING(REPLACE(gen_random_uuid()::TEXT, '-', '') FROM 1 FOR 8)),
    consent_acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS hcw_profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    organization TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
DROP TRIGGER IF EXISTS patient_profiles_set_updated_at ON patient_profiles;
CREATE TRIGGER patient_profiles_set_updated_at BEFORE UPDATE ON patient_profiles
FOR EACH ROW EXECUTE FUNCTION set_updated_at();