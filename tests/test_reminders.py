from datetime import datetime, timedelta, timezone

from conftest import auth_headers


def test_patient_can_create_reminder(api, patient):
    response = api.post("/api/reminders", headers=auth_headers(patient), json={
        "title": "Water plants",
        "remind_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "recurrence": "daily",
    })
    assert response.status_code == 201
    assert response.json()["recurrence"] == "daily"