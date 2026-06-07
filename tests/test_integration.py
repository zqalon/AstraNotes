"""
Integration Tests for AstraNotes API Endpoints

Tests API endpoints with full request/response cycle:
- Authentication endpoints (F-001)
- Note CRUD endpoints (F-002)
- Search API (F-003b)
- Session management (F-001d)
"""

import uuid
import json
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
import pytest

from astranotes.main import app
from astranotes.services import create_note, get_user_by_username, create_user


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def get_unique_user_data():
    """Generate unique user data for test isolation."""
    unique_id = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{unique_id}",
        "email": f"{unique_id}@example.com",
        "password": "SecurePass123",
    }


class TestAuthenticationEndpoints:
    """Tests for authentication endpoints (F-001a, F-001b)."""

    def test_register_page_loads(self, client):
        """GET /register should return HTML form (F-001a)."""
        response = client.get("/register")
        assert response.status_code == 200
        assert "Register" in response.text

    def test_login_page_loads(self, client):
        """GET /login should return HTML form (F-001b)."""
        response = client.get("/login")
        assert response.status_code == 200
        assert "Login" in response.text

    def test_register_new_user_success(self, client):
        """POST /register should create new user and redirect (F-001a)."""
        user_data = get_unique_user_data()
        response = client.post(
            "/register",
            data=user_data,
            allow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/"

    def test_register_with_invalid_email_format(self, client):
        """POST /register should reject invalid email format."""
        user_data = get_unique_user_data()
        user_data["email"] = "invalid-email"
        response = client.post("/register", data=user_data)
        assert response.status_code == 400
        assert "Invalid email" in response.text

    def test_register_with_weak_password(self, client):
        """POST /register should reject password less than 8 characters."""
        user_data = get_unique_user_data()
        user_data["password"] = "weak"
        response = client.post("/register", data=user_data)
        assert response.status_code == 400
        assert "at least 8" in response.text.lower()

    def test_register_duplicate_email(self, client):
        """POST /register should reject duplicate email."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        user_data["username"] = "different_user"
        response = client.post("/register", data=user_data)
        assert response.status_code == 400
        assert "already registered" in response.text.lower()

    def test_register_duplicate_username(self, client):
        """POST /register should reject duplicate username."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        user_data["email"] = "different@example.com"
        response = client.post("/register", data=user_data)
        assert response.status_code == 400
        assert "already taken" in response.text.lower()

    def test_login_with_email_success(self, client):
        """POST /login should authenticate user with email (F-001b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/login",
            data={"identifier": user_data["email"], "password": user_data["password"]},
            allow_redirects=False,
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/"

    def test_login_with_username_success(self, client):
        """POST /login should authenticate user with username (F-001b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/login",
            data={"identifier": user_data["username"], "password": user_data["password"]},
            allow_redirects=False,
        )
        assert response.status_code == 302

    def test_login_with_wrong_password(self, client):
        """POST /login should reject wrong password (F-001b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/login",
            data={"identifier": user_data["username"], "password": "WrongPass123"},
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.text

    def test_login_nonexistent_user(self, client):
        """POST /login should reject non-existent user (F-001b)."""
        response = client.post(
            "/login",
            data={"identifier": "nonexistent", "password": "AnyPass123"},
        )
        assert response.status_code == 401

    def test_logout_clears_session(self, client):
        """GET /logout should clear session (F-001b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.get("/logout", allow_redirects=False)
        assert response.status_code == 302


class TestSessionManagement:
    """Tests for session management (F-001d)."""

    def test_authenticated_user_can_access_main_page(self, client):
        """Authenticated user should access main page (F-001d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.get("/")
        assert response.status_code == 200
        assert user_data["username"] in response.text

    def test_unauthenticated_user_redirected_from_main_page(self, client):
        """Unauthenticated user should be redirected (F-001d)."""
        fresh_client = TestClient(app)
        response = fresh_client.get("/", allow_redirects=False)
        assert response.status_code == 302

    def test_session_persists_across_requests(self, client):
        """Session should persist across multiple requests (F-001d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Make multiple requests
        for _ in range(3):
            response = client.get("/")
            assert response.status_code == 200
            assert user_data["username"] in response.text

    def test_session_cookie_set_on_login(self, client):
        """Session cookie should be set on login (F-001d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/login",
            data={"identifier": user_data["username"], "password": user_data["password"]},
        )
        assert "session" in client.cookies


class TestHealthCheckEndpoint:
    """Tests for API health check endpoint."""

    def test_health_check_endpoint(self, client):
        """GET /api/health should return 200."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestNoteCreationEndpoint:
    """Tests for note creation endpoint (F-002a)."""

    def test_create_note_authenticated(self, client):
        """POST /api/notes should create note for authenticated user (F-002a)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        note_data = {"title": "Test Note", "content": "This is a test"}
        response = client.post("/api/notes", data=note_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Note"
        assert data["content"] == "This is a test"
        assert data["id"] is not None

    def test_create_note_unauthenticated(self, client):
        """POST /api/notes should reject unauthenticated request."""
        fresh_client = TestClient(app)
        note_data = {"title": "Test Note", "content": "This is a test"}
        response = fresh_client.post("/api/notes", data=note_data)
        assert response.status_code == 302

    def test_create_note_with_empty_title(self, client):
        """Should allow creating note with empty title (F-002a)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        note_data = {"title": "", "content": "Content only"}
        response = client.post("/api/notes", data=note_data)
        assert response.status_code == 200

    def test_create_note_with_long_content(self, client):
        """Should handle notes with long content."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        long_content = "x" * 5000
        note_data = {"title": "Long Note", "content": long_content}
        response = client.post("/api/notes", data=note_data)
        assert response.status_code == 200


class TestNoteRetrievalEndpoint:
    """Tests for note retrieval endpoint (F-002b)."""

    def test_get_notes_list(self, client):
        """GET /api/notes should return list of notes (F-002b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        client.post("/api/notes", data={"title": "Note 1", "content": "Content 1"})
        client.post("/api/notes", data={"title": "Note 2", "content": "Content 2"})
        
        response = client.get("/api/notes")
        assert response.status_code == 200
        data = response.json()
        assert "notes" in data
        assert len(data["notes"]) == 2

    def test_get_single_note(self, client):
        """GET /api/notes/{id} should return single note (F-002b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        create_response = client.post(
            "/api/notes", data={"title": "Single", "content": "Content"}
        )
        note_id = create_response.json()["id"]
        
        response = client.get(f"/api/notes/{note_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Single"

    def test_get_nonexistent_note(self, client):
        """GET /api/notes/{id} should return 404 for non-existent note."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.get("/api/notes/99999")
        assert response.status_code == 404

    def test_cannot_access_other_users_note(self, client):
        """User should not access other user's notes."""
        # Create first user and note
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        create_response = client.post(
            "/api/notes", data={"title": "Private", "content": "Content"}
        )
        note_id = create_response.json()["id"]
        client.get("/logout")
        
        # Create second user and try to access first user's note
        user2_data = get_unique_user_data()
        client.post("/register", data=user2_data)
        response = client.get(f"/api/notes/{note_id}")
        assert response.status_code == 404


class TestNoteUpdateEndpoint:
    """Tests for note update endpoint (F-002c)."""

    def test_update_note_title(self, client):
        """PUT /api/notes/{id} should update note title (F-002c)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        create_response = client.post(
            "/api/notes", data={"title": "Original", "content": "Content"}
        )
        note_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/notes/{note_id}",
            data={"title": "Updated", "content": "Content"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"

    def test_update_note_content(self, client):
        """PUT /api/notes/{id} should update note content (F-002c)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        create_response = client.post(
            "/api/notes", data={"title": "Title", "content": "Original"}
        )
        note_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/notes/{note_id}",
            data={"title": "Title", "content": "Updated"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated"

    def test_update_nonexistent_note(self, client):
        """PUT /api/notes/{id} should return 404 for non-existent note."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.put(
            "/api/notes/99999",
            data={"title": "Updated", "content": "Content"},
        )
        assert response.status_code == 404

    def test_cannot_update_other_users_note(self, client):
        """User should not update other user's notes."""
        # Create first user and note
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        create_response = client.post(
            "/api/notes", data={"title": "Original", "content": "Content"}
        )
        note_id = create_response.json()["id"]
        client.get("/logout")
        
        # Create second user and try to update first user's note
        user2_data = get_unique_user_data()
        client.post("/register", data=user2_data)
        response = client.put(
            f"/api/notes/{note_id}",
            data={"title": "Hacked", "content": "Content"},
        )
        assert response.status_code == 404


class TestNoteDeleteEndpoint:
    """Tests for note deletion endpoint (F-002d)."""

    def test_soft_delete_note(self, client):
        """DELETE /api/notes/{id} should soft-delete note (F-002d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        create_response = client.post(
            "/api/notes", data={"title": "To Delete", "content": "Content"}
        )
        note_id = create_response.json()["id"]
        
        response = client.delete(f"/api/notes/{note_id}")
        assert response.status_code == 200
        
        # Note should not appear in list
        get_response = client.get("/api/notes")
        note_ids = [n["id"] for n in get_response.json()["notes"]]
        assert note_id not in note_ids

    def test_restore_deleted_note(self, client):
        """POST /api/notes/{id}/restore should restore deleted note (F-002d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        create_response = client.post(
            "/api/notes", data={"title": "Restore Test", "content": "Content"}
        )
        note_id = create_response.json()["id"]
        
        client.delete(f"/api/notes/{note_id}")
        
        response = client.post(f"/api/notes/{note_id}/restore")
        assert response.status_code == 200
        
        # Note should appear in list again
        get_response = client.get("/api/notes")
        note_ids = [n["id"] for n in get_response.json()["notes"]]
        assert note_id in note_ids

    def test_delete_nonexistent_note(self, client):
        """DELETE /api/notes/{id} should return 404 for non-existent note."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.delete("/api/notes/99999")
        assert response.status_code == 404

    def test_cannot_delete_other_users_note(self, client):
        """User should not delete other user's notes."""
        # Create first user and note
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        create_response = client.post(
            "/api/notes", data={"title": "Protected", "content": "Content"}
        )
        note_id = create_response.json()["id"]
        client.get("/logout")
        
        # Create second user and try to delete first user's note
        user2_data = get_unique_user_data()
        client.post("/register", data=user2_data)
        response = client.delete(f"/api/notes/{note_id}")
        assert response.status_code == 404


class TestSearchEndpoint:
    """Tests for search endpoint (F-003b)."""

    def test_search_notes_by_query(self, client):
        """GET /api/notes?q=query should search notes (F-003b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        client.post("/api/notes", data={"title": "Python Tutorial", "content": "Learn Python"})
        client.post("/api/notes", data={"title": "JavaScript Guide", "content": "Learn JS"})
        
        response = client.get("/api/notes", params={"q": "Python"})
        assert response.status_code == 200
        data = response.json()
        assert any("Python" in note["title"] for note in data["notes"])

    def test_search_by_content(self, client):
        """Search should match content (F-003b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        client.post("/api/notes", data={"title": "Shopping", "content": "Buy milk and eggs"})
        
        response = client.get("/api/notes", params={"q": "milk"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["notes"]) > 0

    def test_search_case_insensitive(self, client):
        """Search should be case-insensitive (F-003b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        client.post("/api/notes", data={"title": "Python", "content": "Content"})
        
        response_lower = client.get("/api/notes", params={"q": "python"})
        response_upper = client.get("/api/notes", params={"q": "PYTHON"})
        
        assert len(response_lower.json()["notes"]) == len(response_upper.json()["notes"])

    def test_search_no_results(self, client):
        """Search should return empty list for no matches."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        client.post("/api/notes", data={"title": "Existing", "content": "Content"})
        
        response = client.get("/api/notes", params={"q": "nonexistent"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["notes"]) == 0

    def test_search_returns_user_notes_only(self, client):
        """Search should return only current user's notes."""
        # Create first user and notes
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        client.post("/api/notes", data={"title": "User1 Secret", "content": "Python"})
        client.get("/logout")
        
        # Create second user and search
        user2_data = get_unique_user_data()
        client.post("/register", data=user2_data)
        client.post("/api/notes", data={"title": "User2 Public", "content": "JavaScript"})
        
        response = client.get("/api/notes", params={"q": "Python"})
        data = response.json()
        assert len(data["notes"]) == 0


class TestEdgeCases:
    """Tests for edge cases and error scenarios."""

    def test_concurrent_note_creation(self, client):
        """Should handle multiple note creation requests."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        note_ids = []
        for i in range(5):
            response = client.post(
                "/api/notes",
                data={"title": f"Note {i}", "content": f"Content {i}"},
            )
            note_ids.append(response.json()["id"])
        
        assert len(note_ids) == len(set(note_ids))  # All IDs unique

    def test_special_characters_in_notes(self, client):
        """Should handle special characters in notes."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        special_title = "Title with <script> & \"quotes\""
        special_content = "Content with émojis 🎉 and special chars: @#$%"
        
        response = client.post(
            "/api/notes",
            data={"title": special_title, "content": special_content},
        )
        assert response.status_code == 200

    def test_unicode_characters_in_notes(self, client):
        """Should handle unicode characters."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/api/notes",
            data={
                "title": "Título en Español",
                "content": "日本語のコンテンツ - Содержание на русском",
            },
        )
        assert response.status_code == 200
        assert "Español" in response.json()["title"]
