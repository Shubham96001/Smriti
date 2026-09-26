# Changelog

## Migration
- Added `backend/main.py`; authentication and assessment now have flat domain modules, direct parameterized SQL, a psycopg pool, and numbered SQL migrations.
- Added game sessions, adaptive difficulty, memory notes, reminders, caregiver approval/scope checks, analytics, and offline sync modules.
- Split the frontend authentication and baseline assessment screens; added role dashboards, patient tools, locale/auth contexts, game sessions, and offline scaffolding.
- Added root tests, project docs, a security audit, and a combined local verification script.
- Removed the old frontend combined auth/assessment/dashboard pages, legacy API helper, and old CSS entry files after replacing their callers.

## Notes
- The six seeded assessment prompts and Hindi/Marathi dictionaries are clearly marked scaffolding. They are not validated clinical content or translations.
- Existing ignored `backend/.env` values were preserved; update credentials locally if needed.
- The requested recursive cleanup of the retired backend package, migration-tool files, and local database files was skipped and remains pending; the final workspace therefore still contains legacy paths.