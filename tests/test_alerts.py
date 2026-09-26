from conftest import auth_headers


def test_alert_list_is_patient_protected(api, patient):
    response = api.get("/api/ai/alerts", headers=auth_headers(patient))
    assert response.status_code == 200
    assert isinstance(response.json(), list)