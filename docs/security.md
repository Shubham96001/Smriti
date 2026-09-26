# Security

- Passwords are stored as bcrypt hashes using Passlib; password material is never returned by account APIs.
- HS256 JWTs carry a subject and expiration. Protected requests decode the token and reload the active user and role from PostgreSQL.
- SQL values are passed separately as psycopg parameters. Dynamic database identifiers in test setup use psycopg's identifier composition API.
- CORS allows only the configured frontend origin.
- Caregiver patient reads require an approved relationship; an inaccessible patient is reported as not found.
- Local `.env` files are ignored by Git. Only example values belong in `.env.example`.
- The static service worker bypasses all `/api/*` traffic.
- The assessment is a development scaffold, not a clinical instrument.

Run `python scripts/security_audit.py` to check these repository-level constraints.