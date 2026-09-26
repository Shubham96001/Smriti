CREATE TABLE IF NOT EXISTS assessment_items (
    id UUID PRIMARY KEY,
    assessment_key TEXT NOT NULL,
    item_number INTEGER NOT NULL,
    prompt TEXT NOT NULL,
    response_options JSONB NOT NULL DEFAULT '[]'::JSONB,
    version TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT 'en',
    UNIQUE (assessment_key, item_number, version, language)
);
CREATE TABLE IF NOT EXISTS assessment_sessions (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient_profiles(id) ON DELETE CASCADE,
    assessment_key TEXT NOT NULL DEFAULT 'rudas',
    version TEXT NOT NULL DEFAULT 'placeholder-v1',
    status TEXT NOT NULL DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed')),
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS assessment_responses (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    item_id UUID NOT NULL REFERENCES assessment_items(id),
    response_text TEXT,
    score INTEGER,
    saved_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (session_id, item_id)
);