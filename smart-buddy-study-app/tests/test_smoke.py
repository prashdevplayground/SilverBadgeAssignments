# This smoke test verifies that the API entry point can be imported without immediate errors.
# It is intentionally lightweight so it can run quickly in CI or local validation.

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint() -> None:
    # The root endpoint should return a simple success payload when the service is available.
    response = client.get("/")
    assert response.status_code == 200
    assert "Smart Buddy Study API is live" in response.json()["message"]
