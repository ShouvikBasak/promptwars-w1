import os
from fastapi.testclient import TestClient
from main import app

# Securely bypass real JWT decryption layer for schema mock validation offline
os.environ["USE_AUTH_STUB"] = "true"
client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer VALID_TOKEN"}

def test_signals_rejects_invalid_wait_minutes():
    """
    Ensures impossible wait times fail immediately at the parameter validation layer.
    """
    # Over 120 minutes rejection
    response_large = client.post(
        "/api/signals",
        headers=AUTH_HEADER,
        json={
            "poiId": "R-101",
            "waitMinutes": 150,  # Rejected by FastAPI schema limit (le=120)
            "submitterRole": "attendee"
        }
    )
    assert response_large.status_code == 422
    assert "waitMinutes" in response_large.text
    
    # Negative time rejection
    response_neg = client.post(
        "/api/signals",
        headers=AUTH_HEADER,
        json={
            "poiId": "R-101",
            "waitMinutes": -10, # Rejected by FastAPI schema limit (ge=0)
            "submitterRole": "attendee"
        }
    )
    assert response_neg.status_code == 422

def test_broadcasts_rejects_long_message():
    """
    Ensures message sizes cannot be ballooned, enforcing the maximum constraints.
    """
    oversized_message = "A" * 201
    
    response = client.post(
        "/api/broadcasts",
        headers=AUTH_HEADER,
        json={
            "zone": "North Section",
            "type": "alert",
            "name": "Gate Alert",
            "message": oversized_message
        }
    )
    
    # Should crash immediately at the validation perimeter before invoking Firestore
    assert response.status_code == 422
    assert "message" in response.text

def test_recommendations_rejects_excess_pois():
    """
    Asserts security protections bounding arrays from overwhelming CPU parsing context limits.
    """
    # Construct 25 POIs violating the 20-bound limit
    overflow_pois = [{"id": f"p{i}", "type": "concession", "currentWaitMinutes": 5, "confidenceScore": 0.5} for i in range(25)]
    
    response = client.post(
        "/api/recommendations",
        headers=AUTH_HEADER,
        json={
            "zone": "North Section",
            "nearbyPOIs": overflow_pois
        }
    )
    
    assert response.status_code == 422
    assert "nearbyPOIs" in response.text
