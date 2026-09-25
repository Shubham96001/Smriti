# SmritiSaathi

SmritiSaathi is a patient-centered digital support platform for older adults. It helps users stay engaged through cognitive activities, memory support, reminders, and caregiver-assisted monitoring while keeping the experience simple, accessible, and low-friction.

This project combines a FastAPI backend, a React + Vite frontend, and a relational database layer designed for local deployment. The current implementation includes patient and caregiver registration, JWT authentication, role-based access, and a one-time baseline RUDAS assessment flow for patients.

> This project is for supportive care and monitoring. It does not provide a medical diagnosis.

---

## Project overview

### Who this is for
- Patients who need a simplified digital companion for routine support, memory cues, and cognitive engagement
- Caregivers who need a secure way to support family members or dependents
- Developers who want a clean starter project with a backend, frontend, and database structure already modeled

### What is implemented
- FastAPI backend with JWT auth
- Patient and caregiver registration flows
- Role-based login and protected routes
- Patient baseline RUDAS assessment flow
- Local DB-ready model layer with SQLAlchemy
- React landing page and auth screens
- Vite frontend with routes for landing, registration, login, dashboard, and baseline assessment

### Tech stack
- Backend: Python, FastAPI, SQLAlchemy, Pydantic
- Frontend: React, Vite, React Router
- Database: PostgreSQL-ready SQLAlchemy configuration; SQLite fallback available for local development
- Auth: JWT + bcrypt password hashing

---

## Repository structure

```text
SmritiSarthi/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   ├── .env.example
│   └── smritisaathi.db
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── README.md
├── .gitignore
└── .env.example
```

---

## Local setup

### 1. Install prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ recommended for the intended local setup

### 2. Backend setup

From the project root:

```bash
cd backend
python -m venv .venv
```

On Windows:

```powershell
backend\.venv\Scripts\Activate.ps1
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file from the sample:

```bash
copy .env.example .env
```

Update the values in backend/.env with your local database credentials:

```env
APP_ENV=development
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/smritisaathi
DATABASE_URL_SYNC=postgresql://postgres:YOUR_PASSWORD@localhost:5432/smritisaathi
JWT_SECRET_KEY=replace_with_a_secure_development_secret
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

If Postgres is not available yet, the app keeps a SQLite fallback so local startup still works.

### 3. Start backend

```bash
cd backend
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Then open:
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### 4. Frontend setup

From the project root:

```bash
cd frontend
npm install
npm run dev
```

Then open:
- App: http://localhost:5173

---

## Important app flow

### Patient flow
1. User lands on the landing page
2. User chooses Register as Patient or Patient Login
3. New patient registers with basic profile information
4. If the patient is new, they complete the RUDAS baseline assessment
5. Baseline data is saved and the patient profile is marked complete
6. Future logins move them to the dashboard without repeating the baseline unless it is intentionally reset

### Caregiver flow
1. User lands on the landing page
2. User chooses Register as Caregiver or Caregiver Login
3. Caregiver account is created and linked to authorized support workflows
4. Caregiver can review support access and monitoring flows

### Authentication model
- Passwords are hashed using bcrypt
- JWT tokens are used for authenticated API access
- Protected endpoints enforce role-based access

---

## Database and model notes

The application is structured around a relational database model with these main concerns:

- users: login credentials and role
- patient_profiles: patient data and baseline completion flag
- caregiver_profiles: caregiver details and access metadata
- rudas_assessments / rudas_responses: baseline cognitive assessment and scoring
- game_sessions / game_events: activity tracking and adaptive behavior logs
- memory_items: saved memory support data
- reminders / reminder_events: routine and medicine support tracking
- audit_logs / caregiver_alerts: monitoring and support records

This is designed to support a local PostgreSQL deployment while staying easy to develop and test locally.

---

## Project status

### Completed
- Backend app scaffolding and routing
- Auth API and JWT flow
- Patient and caregiver registration
- Patient baseline RUDAS flow
- Frontend landing page and registration/login screens
- Vite project setup for React

### Planned / next steps
- Full caregiver-patient linking and authorization flows
- Database migrations via Alembic for production-safe schema evolution
- Real patient dashboard data from DB-backed services
- Cognitive games, reminders, and memory features tied to live records
- More advanced tests and validation coverage

---

## Testing

Run backend tests with:

```bash
cd backend
.venv\Scripts\python -m pytest
```

Run frontend build validation with:

```bash
cd frontend
npm run build
```

---

## Security notes
- Do not commit .env files to Git
- Keep secrets out of the repository
- Use local Postgres credentials only for local development
- Keep JWT secret keys unique and strong in production

---

## Contributing

1. Clone the repository
2. Create a local virtual environment and install backend dependencies
3. Set up Postgres credentials in backend/.env
4. Start the backend and frontend services
5. Create a feature branch before making changes
6. Run the relevant tests and build checks before pushing

This repository is intended to be easy for the next developer to understand, run, and extend without hidden setup steps.
