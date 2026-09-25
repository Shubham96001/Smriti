from app.main import app


def test_app_exposes_baseline_and_auth_routes():
    routes = {route.path for route in app.routes if hasattr(route, "path")}

    assert "/api/auth/register/patient" in routes
    assert "/api/auth/register/caregiver" in routes
    assert "/api/assessments/baseline" in routes
