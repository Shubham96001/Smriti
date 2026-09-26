# Local Demo

1. Install PostgreSQL locally and create a developer database.
2. If `backend/.env` does not already exist, copy `backend/.env.example` to it. Set a local PostgreSQL URL and a long random JWT secret without replacing existing local credentials. Keep this file private.
3. Install backend dependencies with `python -m pip install -r backend/requirements.txt`.
4. From `backend/`, run `python sql/run_migrations.py`, then `python -m uvicorn main:app --reload --port 8000`.
5. In another terminal, run `npm install` and `npm run dev` from `frontend/`.
6. Register a patient, complete the six explicitly marked development placeholders, then try Memory Match, notes, reminders, and caregiver approval.

The UI does not provide medical diagnosis, treatment, or clinical scoring. Hindi and Marathi dictionaries are scaffolding with English fallback, not validated translations.