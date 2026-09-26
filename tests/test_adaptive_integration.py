from conftest import auth_headers


def test_adaptive_route_returns_bounded_decision(api, patient):
    response = api.post("/api/ai/difficulty", headers=auth_headers(patient), json={
        "current_level": 3,
        "recent_accuracies": [0.2, 0.4],
        "recent_hints": [3, 3],
    })
    assert response.status_code == 200
    assert response.json()["level"] == 2