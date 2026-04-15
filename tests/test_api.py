import os
from fastapi.testclient import TestClient
from main import app

os.environ["USE_AUTH_STUB"] = "true"
client = TestClient(app)

def test_recommend_auth_validation():
    # Calling the endpoint without an Auth token should fail natively inside FastAPI middleware
    response = client.post("/api/recommendations", json={})
    assert response.status_code == 401

def test_recommend_schema_missing_fields():
    # Calling with valid auth but missing required fields (zone, nearbyPOIs) -> 422 Unprocessable Entity
    response = client.post(
        "/api/recommendations", 
        headers={"Authorization": "Bearer VALID_TOKEN"},
        json={"accessibilityPreferences": ["wheelchair_accessible"]}
    )
    assert response.status_code == 422
    assert "zone" in response.text
    assert "nearbyPOIs" in response.text

def test_recommend_schema_upper_bounds_security():
    # Calling with payload violating the protective max_items=20 bound inside Pydantic model
    mock_pois = [{"id": f"poi_{i}", "type": "restroom", "currentWaitMinutes": 5, "confidenceScore": 0.5} for i in range(25)]
    
    response = client.post(
        "/api/recommendations", 
        headers={"Authorization": "Bearer VALID_TOKEN"},
        json={
            "zone": "North Gate",
            "nearbyPOIs": mock_pois
        }
    )
    # Native FastAPI bounds checking blocks it without invoking external APIs or Firestore
    assert response.status_code == 422
    assert "at most 20 items" in response.text or "List should have at most 20 items" in response.text
