from conftest import auth_headers, register


def test_register_login_and_current_user(api):
    account = register(api)
    assert account["user"]["role"] == "patient"
    assert "password" not in account["user"]
    current = api.get("/api/auth/me", headers=auth_headers(account))
    assert current.status_code == 200
    assert current.json()["email"].endswith("@example.com")


def test_login_error_does_not_disclose_account(api):
    response = api.post("/api/auth/login", json={"email": "unknown@example.com", "password": "not-a-password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"