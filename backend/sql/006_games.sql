CREATE TABLE IF NOT EXISTS games (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
INSERT INTO games (id, name) VALUES ('memory_match', 'Memory Match') ON CONFLICT (id) DO NOTHING;
CREATE TABLE IF NOT EXISTS game_sessions (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient_profiles(id) ON DELETE CASCADE,
    game_id TEXT NOT NULL REFERENCES games(id),
    difficulty INTEGER NOT NULL DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 5),
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    result JSONB NOT NULL DEFAULT '{}'::JSONB
);
CREATE TABLE IF NOT EXISTS game_events (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES game_sessions(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::JSONB,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS difficulty_decisions (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patient_profiles(id) ON DELETE CASCADE,
    game_id TEXT NOT NULL REFERENCES games(id),
    previous_level INTEGER NOT NULL,
    new_level INTEGER NOT NULL,
    reason TEXT NOT NULL,
    metrics JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);