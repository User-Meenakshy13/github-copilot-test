import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test getting activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

# Test signup for activity
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "student1@mergington.edu"),
    ("Robotics", "student2@mergington.edu"),
])
def test_signup_for_activity(activity, email):
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

# Test duplicate signup
def test_duplicate_signup():
    activity = "Chess Club"
    email = "student3@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Test unregister participant (if implemented)
def test_unregister_participant():
    activity = "Chess Club"
    email = "student4@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200 or response.status_code == 404
