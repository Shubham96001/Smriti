# API

All application endpoints are prefixed with `/api`; interactive documentation is at `/docs`.

| Domain | Endpoint | Purpose |
| --- | --- | --- |
| System | `GET /api/health` | API and database status |
| Auth | `POST /api/auth/register` | Create patient, caregiver, or healthcare-worker account |
| Auth | `POST /api/auth/login` | Issue access token |
| Auth | `GET /api/auth/me` | Read current account |
| Assessment | `GET /api/assessments/rudas/status` | Read baseline state |
| Assessment | `POST /api/assessments/rudas/start` | Start or resume placeholder session |
| Assessment | `POST /api/assessments/rudas` | Save one response |
| Games | `GET /api/games` | List enabled games |
| Games | `POST /api/games/sessions` | Create game session |
| Games | `POST /api/games/sessions/{id}/events` | Submit event batch |
| Games | `POST /api/games/sessions/{id}/complete` | Finish a game session |
| Memory | `GET, POST /api/memory` | List or add memory notes |
| Reminders | `GET, POST /api/reminders` | List or add reminders |
| Caregivers | `/api/caregivers/*` | Request and approve scoped access |
| Activity | `GET /api/ai/summary` | Patient activity counts |
| Sync | `POST /api/sync` | Idempotently accept offline records |

Protected endpoints use `Authorization: Bearer <token>`. Login failures use one generic message. Ownership checks return 404 when the requested object is outside the caller's scope.