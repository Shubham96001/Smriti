from conftest import auth_headers


def test_patient_can_create_and_list_memory(api, patient):
    headers = auth_headers(patient)
    created = api.post("/api/memory", headers=headers, json={"title": "Garden", "body": "Water the basil"})
    assert created.status_code == 201
    listed = api.get("/api/memory", headers=headers)
    assert any(item["title"] == "Garden" for item in listed.json())