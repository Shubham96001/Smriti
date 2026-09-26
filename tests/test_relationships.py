from conftest import auth_headers


def test_patient_controls_caregiver_approval(api, patient, caregiver):
    caregiver_email = caregiver["user"]["email"]
    request = api.post("/api/caregivers/relationships/request", headers=auth_headers(caregiver), json={"patient_email": patient["user"]["email"]})
    assert request.status_code == 201
    pending = api.get("/api/caregivers/approvals", headers=auth_headers(patient))
    relationship_id = pending.json()[0]["id"]
    decision = api.post(f"/api/caregivers/approvals/{relationship_id}", headers=auth_headers(patient), json={"approved": True})
    assert decision.status_code == 200
    listing = api.get("/api/caregivers/relationships", headers=auth_headers(caregiver))
    assert any(link["status"] == "approved" for link in listing.json())
    assert caregiver_email