from conftest import auth_headers


def test_patient_starts_memory_match(api, patient):
    response = api.post("/api/games/sessions", headers=auth_headers(patient), json={"game_id": "memory_match"})
    assert response.status_code == 201
    assert response.json()["game_id"] == "memory_match"


def test_unknown_game_returns_not_found(api, patient):
    response = api.post("/api/games/sessions", headers=auth_headers(patient), json={"game_id": "unknown"})
    assert response.status_code == 404