import uuid

from fastapi.testclient import TestClient

from astranotes.main import app
from astranotes.services import create_note, get_user_by_username


def test_note_search():
    client = TestClient(app)
    unique_id = uuid.uuid4().hex[:8]
    username = f"user_{unique_id}"
    email = f"{unique_id}@example.com"
    password = "SecurePass123"

    # register user
    response = client.post(
        "/register",
        data={"username": username, "email": email, "password": password},
        allow_redirects=False,
    )
    assert response.status_code == 302

    user = get_user_by_username(username)
    assert user is not None

    # create notes
    create_note(user.id, "Shopping list", "Buy milk and eggs")
    create_note(user.id, "Work notes", "Discuss project milestones")

    # search for a term present in first note
    response = client.get("/api/notes", params={"q": "milk"})
    assert response.status_code == 200
    data = response.json()
    assert "notes" in data
    titles = [n["title"] for n in data["notes"]]
    assert any("Shopping" in t for t in titles)
