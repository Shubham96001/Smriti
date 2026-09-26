# SmritiSaathi

## 1. Project overview
SmritiSaathi is an elderly-friendly platform for cognitive games, memory notes, routine reminders, and consent-based caregiver support.

## 2. Intended use
The application provides supportive activities and organization tools. It is not a diagnostic medical system.

## 3. Current scope
The repository includes account registration, login, placeholder baseline flow, Memory Match, memory notes, reminders, caregiver approvals, and offline record scaffolding.

## 4. Technology
The client uses React, Vite, and plain CSS. The API uses Python, FastAPI, Pydantic, psycopg, and PostgreSQL. Passwords use bcrypt and access tokens use signed HS256 JWTs.

## 5. Repository map
New backend modules are flat domain packages under `backend/`; PostgreSQL migrations are in `backend/sql/`. Frontend routes, contexts, games, services, offline support, and styles are under `frontend/src/`. Project documentation is in `docs/`; tests are in `tests/`. The retired nested backend files and local database files remain pending cleanup.

## 6. Requirements
Use Python 3.10 or newer, Node.js 20.19+ or 22.12+, npm, and a local PostgreSQL server. Use a current browser with IndexedDB support for offline scaffolding.

## 7. Backend environment
From the repository root, create and activate a virtual environment, then install `backend/requirements.txt`. If `backend/.env` does not already exist, copy `backend/.env.example` to it. Set a local database URL and a private random JWT secret without replacing existing local credentials.

## 8. Configuration
`DATABASE_URL` accepts a PostgreSQL libpq URL. `JWT_SECRET_KEY`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, and `FRONTEND_ORIGIN` configure authentication and browser access. Never commit the local `.env`.

## 9. Database migrations
Run `python sql/run_migrations.py` from `backend/`. The runner applies numbered SQL files in lexical order and tracks successful versions.

## 10. Start the API
From `backend/`, run `python -m uvicorn main:app --reload --port 8000`. Health is available at `/api/health`; interactive OpenAPI docs are at `/docs`.

## 11. Frontend setup
From `frontend/`, run `npm install` and `npm run dev`. Vite serves the app on port 5173 and proxies `/api` to the local API.

## 12. Authentication
Register at `/register` as a patient, caregiver, or healthcare worker. Sign in at `/login`. The client stores the signed access token locally and sends it as a Bearer token.

## 13. Patient onboarding
Patient accounts go to `/assessment/rudas`. Each response is persisted when advancing. The baseline is complete after all six placeholder items have responses; the dashboard directs incomplete accounts back to the assessment.

## 14. Assessment notice
The seeded English items are generic development placeholders under `placeholder-v1`, not the real RUDAS. They have no clinical scoring or diagnostic interpretation.

## 15. Patient tools
The patient dashboard links to Memory Match, memory notes, reminders, and caregiver approvals. Activity summary values are fetched from the API.

## 16. Caregiver access
Caregivers request a connection by patient email. Patients approve or decline requests. Caregiver reads require an approved relationship; requests outside the relationship return not found.

## 17. Adaptive difficulty
The adaptive engine is a pure conservative rule. It changes at most one level per decision, needs more evidence to increase than to decrease, and includes unit tests.

## 18. Localization and accessibility
English is the fallback locale. Hindi and Marathi files contain a small scaffold only; they are not validated translations. Controls use large touch targets, keyboard focus indicators, and optional speech output where supported.

## 19. Offline behavior
The client queues sync records in IndexedDB and flushes when online. The service worker handles only static application content and never caches API responses.

## 20. Verification and limitations
Run `pytest -q`, `python scripts/security_audit.py`, and `cd frontend && npm run build`. Integration tests create and remove only a loopback `<database>_test` database; they skip if the test database already exists or local PostgreSQL is unavailable. Placeholder content, translations, offline replay, healthcare-worker access, and the remaining legacy-file cleanup are not complete production workflows.

See [docs/architecture.md](docs/architecture.md), [docs/api.md](docs/api.md), [docs/security.md](docs/security.md), and [docs/demo.md](docs/demo.md) for implementation details.