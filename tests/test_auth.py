import uuid

from fastapi.testclient import TestClient
from astranotes.main import app


def test_register_and_login_flow():
    client = TestClient(app)
    unique_id = uuid.uuid4().hex[:8]
    username = f"user_{unique_id}"
    email = f"{unique_id}@example.com"
    password = "SecurePass123"

    response = client.post(
        "/register",
        data={"username": username, "email": email, "password": password},
        allow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["location"] == "/"

    response = client.get("/")
    assert response.status_code == 200
    assert username in response.text

    client = TestClient(app)
    response = client.post(
        "/login",
        data={"identifier": username, "password": password},
        allow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["location"] == "/"
