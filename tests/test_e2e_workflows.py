from conftest import auth_headers


def test_patient_onboarding_completes_baseline(api, patient):
    headers = auth_headers(patient)
    started = api.post("/api/assessments/rudas/start", headers=headers).json()
    for item in started["items"]:
        result = api.post("/api/assessments/rudas", headers=headers, json={
            "session_id": started["session_id"],
            "item_id": item["id"],
            "response_text": item["response_options"][0],
        })
        assert result.status_code == 200
    status = api.get("/api/assessments/rudas/status", headers=headers)
    assert status.json()["baseline_completed"] is True