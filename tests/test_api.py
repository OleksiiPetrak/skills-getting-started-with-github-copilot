from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    encoded_activity = quote(activity, safe="")
    email = "testuser+signup@example.com"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{encoded_activity}/signup?email={quote(email, safe='')}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{encoded_activity}/participants?email={quote(email, safe='')}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
