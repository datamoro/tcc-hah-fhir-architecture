import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_api_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_get_observation_unauthorized():
    response = client.get("/fhir/Observation")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_token_invalid_credentials():
    response = client.post(
        "/auth/token",
        data={"username": "wrong", "password": "user"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_get_token_success_and_access_fhir():
    response = client.post(
        "/auth/token",
        data={"username": "clinician", "password": "supersecure"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # We mock the DB or just test if route authorization passes.
    # We expect 200 OK since the auth barrier is cleared.
    fhir_response = client.get("/fhir/Observation", headers=headers)
    assert fhir_response.status_code == 200
    assert isinstance(fhir_response.json(), list)
