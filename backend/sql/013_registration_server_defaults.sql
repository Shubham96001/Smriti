UPDATE users SET is_active = TRUE WHERE is_active IS NULL;
UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;
UPDATE users SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP) WHERE updated_at IS NULL;
ALTER TABLE users ALTER COLUMN is_active SET DEFAULT TRUE;
ALTER TABLE users ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE users ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

UPDATE patient_profiles SET preferred_language = 'en' WHERE preferred_language IS NULL;
UPDATE patient_profiles SET consent_acknowledged = FALSE WHERE consent_acknowledged IS NULL;
UPDATE patient_profiles SET baseline_completed = FALSE WHERE baseline_completed IS NULL;
UPDATE patient_profiles SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;
UPDATE patient_profiles SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP) WHERE updated_at IS NULL;
ALTER TABLE patient_profiles ALTER COLUMN preferred_language SET DEFAULT 'en';
ALTER TABLE patient_profiles ALTER COLUMN consent_acknowledged SET DEFAULT FALSE;
ALTER TABLE patient_profiles ALTER COLUMN baseline_completed SET DEFAULT FALSE;
ALTER TABLE patient_profiles ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE patient_profiles ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

UPDATE caregiver_profiles SET consent_acknowledged = FALSE WHERE consent_acknowledged IS NULL;
UPDATE caregiver_profiles SET invitation_code = UPPER(SUBSTRING(REPLACE(gen_random_uuid()::TEXT, '-', '') FROM 1 FOR 8)) WHERE invitation_code IS NULL OR invitation_code = '';
UPDATE caregiver_profiles SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;
ALTER TABLE caregiver_profiles ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ;
UPDATE caregiver_profiles SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP) WHERE updated_at IS NULL;
ALTER TABLE caregiver_profiles ALTER COLUMN consent_acknowledged SET DEFAULT FALSE;
ALTER TABLE caregiver_profiles ALTER COLUMN invitation_code SET DEFAULT UPPER(SUBSTRING(REPLACE(gen_random_uuid()::TEXT, '-', '') FROM 1 FOR 8));
ALTER TABLE caregiver_profiles ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE caregiver_profiles ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE caregiver_profiles ALTER COLUMN updated_at SET NOT NULL;
DROP TRIGGER IF EXISTS caregiver_profiles_set_updated_at ON caregiver_profiles;
CREATE TRIGGER caregiver_profiles_set_updated_at BEFORE UPDATE ON caregiver_profiles
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

UPDATE hcw_profiles SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;
ALTER TABLE hcw_profiles ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;