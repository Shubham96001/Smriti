from conftest import auth_headers


def test_sync_is_idempotent(api, patient):
    headers = auth_headers(patient)
    record = {"client_record_id": "offline-1", "resource_type": "note", "payload": {"title": "Queued"}}
    first = api.post("/api/sync", headers=headers, json={"records": [record]})
    second = api.post("/api/sync", headers=headers, json={"records": [record]})
    assert first.status_code == second.status_code == 200
    assert first.json()["accepted"] == 1
    assert second.json()["accepted"] == 0