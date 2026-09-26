from conftest import auth_headers


def test_patient_can_start_placeholder_assessment(api, patient):
    headers = auth_headers(patient)
    status = api.get("/api/assessments/rudas/status", headers=headers)
    assert status.status_code == 200
    assert status.json()["baseline_completed"] is False
    started = api.post("/api/assessments/rudas/start", headers=headers)
    assert started.status_code == 200
    assert started.json()["version"] == "placeholder-v1"
    assert len(started.json()["items"]) == 6


def test_non_patient_cannot_start_assessment(api, caregiver):
    response = api.post("/api/assessments/rudas/start", headers=auth_headers(caregiver))
    assert response.status_code == 403