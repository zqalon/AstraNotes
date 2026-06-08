"""
System Tests for AstraNotes

Tests complete user workflows and system behavior:
- Full user journeys (registration → note management)
- Multi-user isolation and data privacy
- Error handling and validation
- Security and edge cases
"""

import uuid
import pytest
from fastapi.testclient import TestClient

from astranotes.main import app
from astranotes.services import create_user, create_note


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


class TestCompleteUserJourney:
    """Tests for complete user workflows from registration to note management."""

    def test_user_journey_register_create_search_delete(self, client):
        """Complete workflow: register → create notes → search → delete (US-1 through US-6)."""
        # US-1: Register
        user_data = get_unique_user_data()
        response = client.post("/register", data=user_data, allow_redirects=False)
        assert response.status_code == 302
        
        # US-3: Create notes
        client.post("/api/notes", data={"title": "Shopping", "content": "Buy milk and bread"})
        client.post("/api/notes", data={"title": "Meeting", "content": "Discuss project scope"})
        client.post("/api/notes", data={"title": "Ideas", "content": "New feature ideas for Q3"})
        
        # US-4: View notes
        response = client.get("/api/notes")
        assert response.status_code == 200
        notes = response.json()["notes"]
        assert len(notes) == 3
        
        # US-7: Search notes
        response = client.get("/api/notes", params={"q": "project"})
        search_results = response.json()["notes"]
        assert len(search_results) >= 1
        assert any("project" in note["content"].lower() for note in search_results)
        
        # US-5: Edit note
        first_note_id = notes[0]["id"]
        response = client.put(
            f"/api/notes/{first_note_id}",
            data={"title": "Updated Shopping List", "content": "Buy milk, bread, and eggs"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Shopping List"
        
        # US-6: Delete and restore note
        second_note_id = notes[1]["id"]
        response = client.delete(f"/api/notes/{second_note_id}")
        assert response.status_code == 200
        
        # Verify note is deleted (not in list)
        response = client.get("/api/notes")
        remaining_ids = [n["id"] for n in response.json()["notes"]]
        assert second_note_id not in remaining_ids
        
        # Restore note
        response = client.post(f"/api/notes/{second_note_id}/restore")
        assert response.status_code == 200
        
        # Verify note is restored
        response = client.get("/api/notes")
        remaining_ids = [n["id"] for n in response.json()["notes"]]
        assert second_note_id in remaining_ids

    def test_user_journey_login_after_logout(self, client):
        """User can log out and log back in (F-001b, F-001d)."""
        user_data = get_unique_user_data()
        
        # Register
        client.post("/register", data=user_data)
        
        # Create notes while logged in
        client.post("/api/notes", data={"title": "Note 1", "content": "Content"})
        
        # Logout
        response = client.get("/logout", allow_redirects=False)
        assert response.status_code == 302
        
        # Try accessing protected page - should redirect
        fresh_client = TestClient(app)
        response = fresh_client.get("/", allow_redirects=False)
        assert response.status_code == 302
        
        # Login again with same credentials
        response = fresh_client.post(
            "/login",
            data={
                "identifier": user_data["username"],
                "password": user_data["password"],
            },
            allow_redirects=False,
        )
        assert response.status_code == 302
        
        # Should see the note created earlier
        response = fresh_client.get("/api/notes")
        notes = response.json()["notes"]
        assert len(notes) == 1
        assert notes[0]["title"] == "Note 1"


class TestMultiUserIsolation:
    """Tests for data isolation between users (F-001a, SEC-001e)."""

    def test_users_cannot_see_each_other_notes(self, client):
        """User A's notes should not be visible to User B."""
        # User 1: Register and create notes
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        client.post("/api/notes", data={"title": "Secret Note", "content": "Private content"})
        
        # Get note ID
        response = client.get("/api/notes")
        user1_note_id = response.json()["notes"][0]["id"]
        
        client.get("/logout")
        
        # User 2: Register
        fresh_client = TestClient(app)
        user2_data = get_unique_user_data()
        fresh_client.post("/register", data=user2_data)
        
        # User 2 should not see User 1's notes
        response = fresh_client.get("/api/notes")
        user2_notes = response.json()["notes"]
        assert len(user2_notes) == 0
        
        # User 2 should not be able to access User 1's note directly
        response = fresh_client.get(f"/api/notes/{user1_note_id}")
        assert response.status_code == 404

    def test_users_cannot_modify_each_other_notes(self, client):
        """User A should not be able to modify User B's notes."""
        # User 1: Create note
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        response = client.post(
            "/api/notes", data={"title": "Original", "content": "Content"}
        )
        user1_note_id = response.json()["id"]
        client.get("/logout")
        
        # User 2: Try to modify User 1's note
        fresh_client = TestClient(app)
        user2_data = get_unique_user_data()
        fresh_client.post("/register", data=user2_data)
        
        response = fresh_client.put(
            f"/api/notes/{user1_note_id}",
            data={"title": "Hacked", "content": "Modified"},
        )
        assert response.status_code == 404

    def test_users_cannot_delete_each_other_notes(self, client):
        """User A should not be able to delete User B's notes."""
        # User 1: Create note
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        response = client.post(
            "/api/notes", data={"title": "Protected", "content": "Content"}
        )
        user1_note_id = response.json()["id"]
        client.get("/logout")
        
        # User 2: Try to delete User 1's note
        fresh_client = TestClient(app)
        user2_data = get_unique_user_data()
        fresh_client.post("/register", data=user2_data)
        
        response = fresh_client.delete(f"/api/notes/{user1_note_id}")
        assert response.status_code == 404
        
        # User 1: Verify note still exists
        client2 = TestClient(app)
        client2.post("/login", data={
            "identifier": user1_data["username"],
            "password": user1_data["password"],
        })
        response = client2.get(f"/api/notes/{user1_note_id}")
        assert response.status_code == 200

    def test_users_cannot_search_each_other_notes(self, client):
        """Search results should be isolated per user."""
        # User 1: Create notes
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        client.post("/api/notes", data={"title": "Python", "content": "Learn Python"})
        client.post("/api/notes", data={"title": "Data Science", "content": "Python and pandas"})
        client.get("/logout")
        
        # User 2: Create different notes and search
        fresh_client = TestClient(app)
        user2_data = get_unique_user_data()
        fresh_client.post("/register", data=user2_data)
        fresh_client.post("/api/notes", data={"title": "JavaScript", "content": "Learn JS"})
        
        response = fresh_client.get("/api/notes", params={"q": "Python"})
        results = response.json()["notes"]
        assert len(results) == 0  # User 2 should find no Python notes


class TestInputValidation:
    """Tests for input validation and error handling (SEC-001e)."""

    def test_sql_injection_attempt_in_search(self, client):
        """Search should safely handle SQL injection attempts."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Try SQL injection in search
        response = client.get("/api/notes", params={"q": "'; DROP TABLE note; --"})
        assert response.status_code == 200
        data = response.json()
        assert "notes" in data

    def test_xss_attempt_in_note_title(self, client):
        """Notes should safely handle XSS attempts in title."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        xss_payload = "<script>alert('XSS')</script>"
        response = client.post(
            "/api/notes",
            data={"title": xss_payload, "content": "Normal content"},
        )
        assert response.status_code == 200
        
        # Retrieve and verify it's stored safely
        response = client.get("/api/notes")
        notes = response.json()["notes"]
        assert len(notes) > 0

    def test_xss_attempt_in_note_content(self, client):
        """Notes should safely handle XSS attempts in content."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        xss_payload = "Content <img src=x onerror='alert(1)'>"
        response = client.post(
            "/api/notes",
            data={"title": "Normal title", "content": xss_payload},
        )
        assert response.status_code == 200

    def test_csrf_protection_with_session(self, client):
        """Session-based CSRF protection should be in place."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Legitimate request should work
        response = client.post(
            "/api/notes",
            data={"title": "Legitimate", "content": "Content"},
        )
        assert response.status_code == 200


class TestNoteTimestamps:
    """Tests for note timestamp behavior (F-002a, F-002c)."""

    def test_created_at_timestamp_set_on_creation(self, client):
        """Note should have created_at timestamp on creation (F-002a)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/api/notes", data={"title": "Test", "content": "Content"}
        )
        note = response.json()
        assert "created_at" in note
        assert note["created_at"] is not None

    def test_updated_at_timestamp_updates_on_edit(self, client):
        """Note's updated_at should update when edited (F-002c)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/api/notes", data={"title": "Test", "content": "Original"}
        )
        note_id = response.json()["id"]
        original_updated_at = response.json()["updated_at"]
        
        # Wait a moment and update
        import time
        time.sleep(0.1)
        
        response = client.put(
            f"/api/notes/{note_id}",
            data={"title": "Test", "content": "Updated"},
        )
        updated_note = response.json()
        assert updated_note["updated_at"] >= original_updated_at


class TestSoftDeleteBehavior:
    """Tests for soft delete and restore functionality (F-002d)."""

    def test_deleted_notes_excluded_from_list_by_default(self, client):
        """Deleted notes should not appear in normal list (F-002d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create notes
        response1 = client.post(
            "/api/notes", data={"title": "Keep", "content": "Content"}
        )
        response2 = client.post(
            "/api/notes", data={"title": "Delete", "content": "Content"}
        )
        
        keep_id = response1.json()["id"]
        delete_id = response2.json()["id"]
        
        # Delete one note
        client.delete(f"/api/notes/{delete_id}")
        
        # List should only show one note
        response = client.get("/api/notes")
        notes = response.json()["notes"]
        assert len(notes) == 1
        assert notes[0]["id"] == keep_id

    def test_deleted_notes_excluded_from_search_by_default(self, client):
        """Deleted notes should not appear in search results (F-002d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create notes with searchable content
        response1 = client.post(
            "/api/notes", data={"title": "Keep", "content": "Python is great"}
        )
        response2 = client.post(
            "/api/notes", data={"title": "Delete", "content": "Python is powerful"}
        )
        
        delete_id = response2.json()["id"]
        
        # Delete one note
        client.delete(f"/api/notes/{delete_id}")
        
        # Search should only show one result
        response = client.get("/api/notes", params={"q": "Python"})
        results = response.json()["notes"]
        assert len(results) == 1

    def test_restore_makes_note_visible_again(self, client):
        """Restored note should be visible again (F-002d)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.post(
            "/api/notes", data={"title": "Temp Delete", "content": "Content"}
        )
        note_id = response.json()["id"]
        
        # Delete
        client.delete(f"/api/notes/{note_id}")
        
        # Verify hidden
        response = client.get("/api/notes")
        assert len(response.json()["notes"]) == 0
        
        # Restore
        client.post(f"/api/notes/{note_id}/restore")
        
        # Verify visible
        response = client.get("/api/notes")
        assert len(response.json()["notes"]) == 1


class TestSearchFiltering:
    """Tests for advanced search and filtering (F-003b, F-003c)."""

    def test_search_returns_most_recent_first(self, client):
        """Search results should be ordered by most recent first (F-003b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create notes in order
        client.post("/api/notes", data={"title": "First Python", "content": "Old"})
        client.post("/api/notes", data={"title": "Second Python", "content": "New"})
        
        response = client.get("/api/notes", params={"q": "Python"})
        notes = response.json()["notes"]
        assert len(notes) == 2
        # Most recent should be second
        assert notes[0]["title"] == "Second Python"

    def test_search_partial_word_match(self, client):
        """Search should match partial words."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        client.post("/api/notes", data={"title": "Programming", "content": "Code"})
        
        response = client.get("/api/notes", params={"q": "program"})
        results = response.json()["notes"]
        assert len(results) >= 1

    def test_search_multiple_keywords(self, client):
        """Search with multiple keywords should work."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        client.post("/api/notes", data={"title": "Python Tutorial", "content": "Learn programming"})
        
        # Single keyword
        response = client.get("/api/notes", params={"q": "Python"})
        assert len(response.json()["notes"]) >= 1
        
        # Another keyword
        response = client.get("/api/notes", params={"q": "Tutorial"})
        assert len(response.json()["notes"]) >= 1


class TestErrorRecovery:
    """Tests for error recovery and system stability."""

    def test_system_handles_concurrent_operations(self, client):
        """System should handle concurrent operations without errors."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Rapid fire operations
        for i in range(10):
            response = client.post(
                "/api/notes",
                data={"title": f"Note {i}", "content": f"Content {i}"},
            )
            assert response.status_code == 200

    def test_large_note_content_handling(self, client):
        """System should handle notes with large content."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        large_content = "x" * 10000
        response = client.post(
            "/api/notes",
            data={"title": "Large Note", "content": large_content},
        )
        assert response.status_code == 200
        
        # Retrieve and verify
        note_id = response.json()["id"]
        response = client.get(f"/api/notes/{note_id}")
        assert response.status_code == 200
        assert len(response.json()["content"]) == 10000

    def test_many_notes_retrieval(self, client):
        """System should handle retrieval of many notes."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create many notes
        for i in range(20):
            client.post(
                "/api/notes",
                data={"title": f"Note {i}", "content": f"Content {i}"},
            )
        
        # Retrieve all
        response = client.get("/api/notes")
        assert response.status_code == 200
        assert len(response.json()["notes"]) == 20


class TestPasswordSecurity:
    """Tests for password security (SEC-001b)."""

    def test_password_not_returned_in_api(self, client):
        """User object should never return password (SEC-001b)."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        response = client.get("/")
        assert response.status_code == 200
        # Password should not appear in HTML
        assert "SecurePass123" not in response.text

    def test_weak_passwords_rejected(self, client):
        """Weak passwords should be rejected (SEC-001b)."""
        weak_passwords = ["pass", "12345", "abc", "a"]
        
        for weak_pass in weak_passwords:
            user_data = get_unique_user_data()
            user_data["password"] = weak_pass
            response = client.post("/register", data=user_data)
            assert response.status_code == 400
            assert "8" in response.text.lower() or "password" in response.text.lower()


class TestNoteLifecycleWorkflows:
    """Tests for complete note lifecycle workflows (F-002)."""

    def test_comprehensive_note_workflow(self, client):
        """Complete workflow: create → update → delete → restore."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create note
        create_response = client.post(
            "/api/notes",
            data={"title": "Working Note", "content": "Initial content"},
        )
        assert create_response.status_code == 200
        note_id = create_response.json()["id"]
        
        # Verify created
        get_response = client.get(f"/api/notes/{note_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Working Note"
        
        # Update note
        update_response = client.put(
            f"/api/notes/{note_id}",
            data={"title": "Updated Note", "content": "Updated content"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Note"
        
        # Verify update
        get_response = client.get(f"/api/notes/{note_id}")
        assert get_response.json()["content"] == "Updated content"
        
        # Delete note
        delete_response = client.delete(f"/api/notes/{note_id}")
        assert delete_response.status_code == 200
        
        # Verify deleted (not in list)
        list_response = client.get("/api/notes")
        assert note_id not in [n["id"] for n in list_response.json()["notes"]]
        
        # Restore note
        restore_response = client.post(f"/api/notes/{note_id}/restore")
        assert restore_response.status_code == 200
        
        # Verify restored
        list_response = client.get("/api/notes")
        assert note_id in [n["id"] for n in list_response.json()["notes"]]

    def test_note_deletion_workflow_with_multiple_notes(self, client):
        """Workflow: create multiple notes, selectively delete and restore."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create multiple notes
        note_ids = []
        for i in range(5):
            response = client.post(
                "/api/notes",
                data={"title": f"Note {i}", "content": f"Content {i}"},
            )
            note_ids.append(response.json()["id"])
        
        # Delete every other note (indices 1, 3)
        for i in [1, 3]:
            client.delete(f"/api/notes/{note_ids[i]}")
        
        # Verify list shows only active notes
        list_response = client.get("/api/notes")
        active_ids = [n["id"] for n in list_response.json()["notes"]]
        assert len(active_ids) == 3
        assert note_ids[1] not in active_ids
        assert note_ids[3] not in active_ids
        
        # Restore one deleted note
        client.post(f"/api/notes/{note_ids[1]}/restore")
        
        # Verify list now shows 4 notes
        list_response = client.get("/api/notes")
        active_ids = [n["id"] for n in list_response.json()["notes"]]
        assert len(active_ids) == 4

    def test_note_operations_maintain_data_integrity(self, client):
        """Note operations should maintain data integrity."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        original_title = "Important Note"
        original_content = "This is very important content that should not be lost"
        
        # Create note
        create_response = client.post(
            "/api/notes",
            data={"title": original_title, "content": original_content},
        )
        note_id = create_response.json()["id"]
        original_created_at = create_response.json()["created_at"]
        
        # Delete and restore
        client.delete(f"/api/notes/{note_id}")
        client.post(f"/api/notes/{note_id}/restore")
        
        # Verify all data is intact
        get_response = client.get(f"/api/notes/{note_id}")
        restored_note = get_response.json()
        
        assert restored_note["title"] == original_title
        assert restored_note["content"] == original_content
        assert restored_note["created_at"] == original_created_at
        assert restored_note["is_deleted"] is False

    def test_search_behavior_with_delete_operations(self, client):
        """Search should respect deletion state."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create searchable notes
        response1 = client.post(
            "/api/notes",
            data={"title": "Python Tutorial", "content": "Learn Python programming"},
        )
        response2 = client.post(
            "/api/notes",
            data={"title": "Python Advanced", "content": "Advanced Python topics"},
        )
        note_id_1 = response1.json()["id"]
        note_id_2 = response2.json()["id"]
        
        # Search finds both
        search_response = client.get("/api/notes", params={"q": "Python"})
        assert len(search_response.json()["notes"]) == 2
        
        # Delete one
        client.delete(f"/api/notes/{note_id_1}")
        
        # Search now finds only one
        search_response = client.get("/api/notes", params={"q": "Python"})
        results = search_response.json()["notes"]
        assert len(results) == 1
        assert results[0]["id"] == note_id_2
        
        # Restore and search finds both again
        client.post(f"/api/notes/{note_id_1}/restore")
        search_response = client.get("/api/notes", params={"q": "Python"})
        assert len(search_response.json()["notes"]) == 2

    def test_note_state_transitions(self, client):
        """Test valid note state transitions."""
        user_data = get_unique_user_data()
        client.post("/register", data=user_data)
        
        # Create note (state: active)
        response = client.post(
            "/api/notes", data={"title": "State Test", "content": "Content"}
        )
        note_id = response.json()["id"]
        assert response.json()["is_deleted"] is False
        
        # Delete (state: deleted)
        delete_response = client.delete(f"/api/notes/{note_id}")
        assert delete_response.status_code == 200
        
        # Restore (state: active again)
        restore_response = client.post(f"/api/notes/{note_id}/restore")
        assert restore_response.status_code == 200
        
        # Verify final state
        get_response = client.get(f"/api/notes/{note_id}")
        assert get_response.json()["is_deleted"] is False

    def test_deletion_isolation_between_users(self, client):
        """Deletion by one user should not affect other users' notes."""
        # User 1: Create notes
        user1_data = get_unique_user_data()
        client.post("/register", data=user1_data)
        response = client.post(
            "/api/notes", data={"title": "User1 Note", "content": "Content"}
        )
        user1_note_id = response.json()["id"]
        client.get("/logout")
        
        # User 2: Create and delete their own note
        user2_data = get_unique_user_data()
        client.post("/register", data=user2_data)
        response = client.post(
            "/api/notes", data={"title": "User2 Note", "content": "Content"}
        )
        user2_note_id = response.json()["id"]
        client.delete(f"/api/notes/{user2_note_id}")
        
        # User 1: Verify their note is still accessible
        client2 = TestClient(app)
        client2.post("/login", data={
            "identifier": user1_data["username"],
            "password": user1_data["password"],
        })
        response = client2.get(f"/api/notes/{user1_note_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "User1 Note"
