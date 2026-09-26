# Architecture

## Runtime boundaries

The React/Vite client communicates with FastAPI only through `/api/*`. FastAPI exposes OpenAPI at `/docs` and uses a bounded `psycopg` connection pool for PostgreSQL. SQL changes are applied by the lexical SQL runner.

## Backend domains

`auth` signs HS256 access tokens and hashes passwords with bcrypt. `users` reads the current public account data. `assessments`, `games`, `memory`, `reminders`, `caregivers`, `ai`, and `sync` own their route/schema/query boundaries. Protected requests reload the user from PostgreSQL. Cross-account caregiver reads require an approved relationship and return 404 outside that scope.

## Persistence

`backend/sql/001_users.sql` through `011_offline_sync.sql` define the PostgreSQL schema and development seed. The runner records each completed migration in `schema_migrations`; each migration is applied in its own transaction and is safe to rerun.

## Client state

Auth state is held in `AuthContext`; locale selection uses the English/Hindi/Marathi dictionaries. The offline provider stores queued records in IndexedDB and submits them when connectivity returns. The service worker caches the application shell only and bypasses `/api/*`.

## Assessment status

The six English prompts are generic development placeholders under `placeholder-v1`. They are not the real RUDAS, and no clinical interpretation is provided.