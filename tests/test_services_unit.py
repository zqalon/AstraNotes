"""
Unit Tests for AstraNotes Service Layer

Tests individual business logic functions in isolation:
- Password validation and hashing (SEC-001b)
- User creation and retrieval (F-001a)
- Note CRUD operations (F-002)
- Search functionality (F-003b)
- Soft delete and restore (F-002d)
"""

import pytest
from datetime import datetime, timedelta
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from astranotes.db import init_db
from astranotes.models import User, Note
from astranotes.services import (
    create_user,
    authenticate_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_id,
    verify_password,
    get_password_hash,
    create_note,
    get_note_by_id,
    get_notes_for_user,
    update_note,
    delete_note,
    restore_note,
    search_notes,
)


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    # Initialize database schema
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestPasswordHandling:
    """Tests for password hashing and verification (SEC-001b)."""

    def test_password_hashing_creates_different_hashes(self):
        """Same password should produce different hashes (due to salt)."""
        password = "SecurePassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2

    def test_verify_password_with_correct_password(self):
        """verify_password should return True for correct password."""
        password = "TestPass123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_with_incorrect_password(self):
        """verify_password should return False for incorrect password."""
        password = "TestPass123"
        wrong_password = "WrongPass456"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False

    def test_password_hash_is_not_plaintext(self):
        """Password hash should not contain the plaintext password."""
        password = "PlainTextPassword"
        hashed = get_password_hash(password)
        assert password not in hashed


class TestUserCreation:
    """Tests for user registration and retrieval (F-001a)."""

    def test_create_user_with_valid_data(self, session):
        """Should successfully create user with valid email and password."""
        user = create_user("test@example.com", "testuser", "SecurePass123")
        assert user is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.hashed_password is not None
        assert user.created_at is not None

    def test_create_user_with_invalid_email_format(self, session):
        """Should reject invalid email formats."""
        with pytest.raises(ValueError, match="Invalid email"):
            create_user("invalid-email", "testuser", "SecurePass123")

    def test_create_user_with_weak_password(self, session):
        """Should reject passwords shorter than 8 characters."""
        with pytest.raises(ValueError, match="Password must be at least 8"):
            create_user("test@example.com", "testuser", "weak")

    def test_create_duplicate_email(self, session):
        """Should reject duplicate email addresses."""
        create_user("duplicate@example.com", "user1", "SecurePass123")
        with pytest.raises(ValueError, match="Email already registered"):
            create_user("duplicate@example.com", "user2", "SecurePass123")

    def test_create_duplicate_username(self, session):
        """Should reject duplicate usernames."""
        create_user("test1@example.com", "sameuser", "SecurePass123")
        with pytest.raises(ValueError, match="Username already taken"):
            create_user("test2@example.com", "sameuser", "SecurePass123")

    def test_get_user_by_email(self, session):
        """Should retrieve user by email address."""
        created_user = create_user("findme@example.com", "finduser", "SecurePass123")
        found_user = get_user_by_email("findme@example.com")
        assert found_user is not None
        assert found_user.username == "finduser"

    def test_get_user_by_username(self, session):
        """Should retrieve user by username."""
        created_user = create_user("test@example.com", "findbyname", "SecurePass123")
        found_user = get_user_by_username("findbyname")
        assert found_user is not None
        assert found_user.email == "test@example.com"

    def test_get_user_by_id(self, session):
        """Should retrieve user by ID."""
        created_user = create_user("test@example.com", "testuser", "SecurePass123")
        found_user = get_user_by_id(created_user.id)
        assert found_user is not None
        assert found_user.username == "testuser"

    def test_get_nonexistent_user_returns_none(self, session):
        """Should return None for non-existent user."""
        assert get_user_by_email("nonexistent@example.com") is None
        assert get_user_by_username("nonexistent") is None
        assert get_user_by_id(99999) is None


class TestAuthentication:
    """Tests for user authentication (F-001b)."""

    def test_authenticate_with_email_and_password(self, session):
        """Should authenticate user with email and password."""
        create_user("auth@example.com", "authuser", "SecurePass123")
        user = authenticate_user("auth@example.com", "SecurePass123")
        assert user is not None
        assert user.email == "auth@example.com"

    def test_authenticate_with_username_and_password(self, session):
        """Should authenticate user with username and password."""
        create_user("test@example.com", "authuser", "SecurePass123")
        user = authenticate_user("authuser", "SecurePass123")
        assert user is not None
        assert user.username == "authuser"

    def test_authenticate_with_wrong_password(self, session):
        """Should reject authentication with wrong password."""
        create_user("test@example.com", "user", "CorrectPass123")
        user = authenticate_user("user", "WrongPass123")
        assert user is None

    def test_authenticate_nonexistent_user(self, session):
        """Should reject authentication for non-existent user."""
        user = authenticate_user("nonexistent", "AnyPass123")
        assert user is None


class TestNoteCRUD:
    """Tests for note CRUD operations (F-002)."""

    @pytest.fixture
    def test_user(self, session):
        """Create a test user for note operations."""
        return create_user("notes@example.com", "noteuser", "SecurePass123")

    def test_create_note_with_valid_data(self, test_user):
        """Should successfully create note with title and content (F-002a)."""
        note = create_note(test_user.id, "Test Title", "Test content here")
        assert note is not None
        assert note.title == "Test Title"
        assert note.content == "Test content here"
        assert note.user_id == test_user.id
        assert note.created_at is not None
        assert note.updated_at is not None
        assert note.is_deleted is False

    def test_create_note_with_empty_title(self, test_user):
        """Should create note even with empty title."""
        note = create_note(test_user.id, "", "Some content")
        assert note is not None
        assert note.title == ""

    def test_create_note_with_empty_content(self, test_user):
        """Should create note even with empty content."""
        note = create_note(test_user.id, "Just a title", "")
        assert note is not None
        assert note.content == ""

    def test_get_note_by_id(self, test_user):
        """Should retrieve note by ID (F-002b)."""
        created_note = create_note(test_user.id, "Retrieval Test", "Content")
        retrieved_note = get_note_by_id(created_note.id, test_user.id)
        assert retrieved_note is not None
        assert retrieved_note.title == "Retrieval Test"

    def test_get_note_by_wrong_user(self, test_user):
        """Should not retrieve note when requesting as different user."""
        created_note = create_note(test_user.id, "Private Note", "Content")
        other_user = create_user("other@example.com", "otheruser", "SecurePass123")
        retrieved_note = get_note_by_id(created_note.id, other_user.id)
        assert retrieved_note is None

    def test_get_notes_for_user(self, test_user):
        """Should retrieve all notes for a user (F-002b)."""
        create_note(test_user.id, "Note 1", "Content 1")
        create_note(test_user.id, "Note 2", "Content 2")
        create_note(test_user.id, "Note 3", "Content 3")
        notes = get_notes_for_user(test_user.id, include_deleted=False)
        assert len(notes) == 3

    def test_get_notes_excludes_deleted_by_default(self, test_user):
        """Should exclude deleted notes by default (F-002d)."""
        note1 = create_note(test_user.id, "Active Note", "Content")
        note2 = create_note(test_user.id, "To Delete", "Content")
        delete_note(note2.id, test_user.id)
        
        notes = get_notes_for_user(test_user.id, include_deleted=False)
        assert len(notes) == 1
        assert notes[0].title == "Active Note"

    def test_get_notes_includes_deleted_when_requested(self, test_user):
        """Should include deleted notes when requested (F-002d)."""
        note1 = create_note(test_user.id, "Active Note", "Content")
        note2 = create_note(test_user.id, "Deleted Note", "Content")
        delete_note(note2.id, test_user.id)
        
        notes = get_notes_for_user(test_user.id, include_deleted=True)
        assert len(notes) == 2

    def test_update_note_title(self, test_user):
        """Should update note title (F-002c)."""
        note = create_note(test_user.id, "Original Title", "Content")
        original_timestamp = note.updated_at
        
        updated_note = update_note(note.id, test_user.id, title="Updated Title")
        assert updated_note is not None
        assert updated_note.title == "Updated Title"
        assert updated_note.content == "Content"
        assert updated_note.updated_at >= original_timestamp

    def test_update_note_content(self, test_user):
        """Should update note content (F-002c)."""
        note = create_note(test_user.id, "Title", "Original content")
        
        updated_note = update_note(note.id, test_user.id, content="Updated content")
        assert updated_note is not None
        assert updated_note.title == "Title"
        assert updated_note.content == "Updated content"

    def test_update_note_title_and_content(self, test_user):
        """Should update both title and content (F-002c)."""
        note = create_note(test_user.id, "Title", "Content")
        
        updated_note = update_note(
            note.id, test_user.id, title="New Title", content="New Content"
        )
        assert updated_note.title == "New Title"
        assert updated_note.content == "New Content"

    def test_update_note_wrong_user(self, test_user):
        """Should not update note when requested by wrong user."""
        note = create_note(test_user.id, "Title", "Content")
        other_user = create_user("other@example.com", "otheruser", "SecurePass123")
        
        result = update_note(note.id, other_user.id, title="Hacked")
        assert result is None

    def test_soft_delete_note(self, test_user):
        """Should soft delete note (mark is_deleted=True) (F-002d)."""
        note = create_note(test_user.id, "To Delete", "Content")
        assert note.is_deleted is False
        
        deleted_note = delete_note(note.id, test_user.id)
        assert deleted_note is not None
        assert deleted_note.is_deleted is True

    def test_restore_deleted_note(self, test_user):
        """Should restore soft-deleted note (F-002d)."""
        note = create_note(test_user.id, "Temporary Delete", "Content")
        delete_note(note.id, test_user.id)
        
        restored_note = restore_note(note.id, test_user.id)
        assert restored_note is not None
        assert restored_note.is_deleted is False

    def test_restore_note_wrong_user(self, test_user):
        """Should not restore note when requested by wrong user."""
        note = create_note(test_user.id, "Title", "Content")
        delete_note(note.id, test_user.id)
        other_user = create_user("other@example.com", "otheruser", "SecurePass123")
        
        result = restore_note(note.id, other_user.id)
        assert result is None


class TestSearchFunctionality:
    """Tests for search functionality (F-003b)."""

    @pytest.fixture
    def test_user_with_notes(self, session):
        """Create a test user with multiple notes."""
        user = create_user("search@example.com", "searchuser", "SecurePass123")
        create_note(user.id, "Python Tutorial", "Learn Python basics and advanced topics")
        create_note(user.id, "JavaScript Guide", "Complete JS guide for web development")
        create_note(user.id, "Shopping List", "Buy milk, eggs, and bread for baking")
        create_note(user.id, "Meeting Notes", "Discuss project progress and milestones")
        return user

    def test_search_by_title(self, test_user_with_notes):
        """Should find notes by title (F-003b)."""
        results = search_notes(test_user_with_notes.id, q="Python")
        assert len(results) >= 1
        assert any("Python" in note.title for note in results)

    def test_search_by_content(self, test_user_with_notes):
        """Should find notes by content (F-003b)."""
        results = search_notes(test_user_with_notes.id, q="baking")
        assert len(results) >= 1
        assert any("baking" in note.content for note in results)

    def test_search_case_insensitive(self, test_user_with_notes):
        """Should perform case-insensitive search (F-003b)."""
        results_lower = search_notes(test_user_with_notes.id, q="python")
        results_upper = search_notes(test_user_with_notes.id, q="PYTHON")
        assert len(results_lower) == len(results_upper)
        assert len(results_lower) >= 1

    def test_search_no_results(self, test_user_with_notes):
        """Should return empty list when no matches found."""
        results = search_notes(test_user_with_notes.id, q="nonexistent")
        assert len(results) == 0

    def test_search_empty_query(self, test_user_with_notes):
        """Should return all notes when search query is empty (F-003b)."""
        results = search_notes(test_user_with_notes.id, q="")
        assert len(results) == 4

    def test_search_excludes_deleted_by_default(self, test_user_with_notes):
        """Should exclude deleted notes from search results (F-002d)."""
        notes = get_notes_for_user(test_user_with_notes.id)
        if len(notes) > 0:
            delete_note(notes[0].id, test_user_with_notes.id)
        
        results = search_notes(test_user_with_notes.id, q="", include_deleted=False)
        assert len(results) == 3

    def test_search_includes_deleted_when_requested(self, test_user_with_notes):
        """Should include deleted notes when requested (F-002d)."""
        notes = get_notes_for_user(test_user_with_notes.id)
        if len(notes) > 0:
            delete_note(notes[0].id, test_user_with_notes.id)
        
        results = search_notes(test_user_with_notes.id, q="", include_deleted=True)
        assert len(results) == 4

    def test_search_multiple_matches(self, test_user_with_notes):
        """Should return multiple matching notes."""
        results = search_notes(test_user_with_notes.id, q="and")
        assert len(results) >= 2

    def test_search_isolated_to_user(self, test_user_with_notes):
        """Search should only return current user's notes."""
        other_user = create_user("other@example.com", "other", "SecurePass123")
        create_note(other_user.id, "Secret Note", "Contains 'Python'")
        
        results = search_notes(test_user_with_notes.id, q="Python")
        for note in results:
            assert note.user_id == test_user_with_notes.id

    def test_search_by_date_range(self, test_user_with_notes):
        """Should filter notes by date range (F-003b)."""
        now = datetime.utcnow()
        future = now + timedelta(days=1)
        past = now - timedelta(days=1)
        
        # Search within date range that includes all notes
        results = search_notes(
            test_user_with_notes.id,
            q="",
            date_from=past,
            date_to=future,
            include_deleted=False
        )
        assert len(results) == 4

    def test_search_date_from_filter(self, test_user_with_notes):
        """Should filter notes created after date_from."""
        now = datetime.utcnow()
        future = now + timedelta(days=1)
        
        results = search_notes(
            test_user_with_notes.id,
            q="",
            date_from=future,
            include_deleted=False
        )
        # Should have no results since all notes were created before future date
        assert len(results) == 0

    def test_search_date_to_filter(self, test_user_with_notes):
        """Should filter notes created before date_to."""
        now = datetime.utcnow()
        past = now - timedelta(days=1)
        
        results = search_notes(
            test_user_with_notes.id,
            q="",
            date_to=past,
            include_deleted=False
        )
        # Should have no results since all notes were created after past date
        assert len(results) == 0


class TestNoteEdgeCases:
    """Tests for edge cases in note operations."""

    @pytest.fixture
    def test_user(self, session):
        """Create a test user for note operations."""
        return create_user("edge@example.com", "edgeuser", "SecurePass123")

    def test_create_note_with_very_long_title(self, test_user):
        """Should create note with very long title."""
        long_title = "A" * 10000
        note = create_note(test_user.id, long_title, "Content")
        assert note is not None
        assert len(note.title) == 10000

    def test_create_note_with_very_long_content(self, test_user):
        """Should create note with very long content."""
        long_content = "Lorem ipsum " * 10000
        note = create_note(test_user.id, "Title", long_content)
        assert note is not None
        assert len(note.content) == len(long_content)

    def test_create_note_with_special_characters(self, test_user):
        """Should create note with special characters."""
        special_title = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        special_content = "émojis: 🎉 🚀 ✨ | symbols: © ® ™"
        note = create_note(test_user.id, special_title, special_content)
        assert note is not None
        assert note.title == special_title
        assert note.content == special_content

    def test_create_note_with_unicode(self, test_user):
        """Should create note with unicode characters."""
        unicode_title = "Привет мир 你好世界 مرحبا بالعالم"
        unicode_content = "日本語、中文、한글、العربية"
        note = create_note(test_user.id, unicode_title, unicode_content)
        assert note is not None
        assert note.title == unicode_title
        assert note.content == unicode_content

    def test_create_note_with_newlines(self, test_user):
        """Should create note preserving newlines."""
        content_with_newlines = "Line 1\nLine 2\nLine 3\n\nMultiple\n\n\nNewlines"
        note = create_note(test_user.id, "Multiline", content_with_newlines)
        assert note is not None
        assert note.content == content_with_newlines

    def test_update_note_removes_content(self, test_user):
        """Should allow clearing note content."""
        note = create_note(test_user.id, "Title", "Original content")
        updated = update_note(note.id, test_user.id, content="")
        assert updated is not None
        assert updated.content == ""

    def test_multiple_operations_on_same_note(self, test_user):
        """Should handle multiple create, update, delete, restore operations."""
        note = create_note(test_user.id, "Title", "Content")
        note_id = note.id
        
        # Update
        update_note(note_id, test_user.id, title="Updated")
        updated = get_note_by_id(note_id, test_user.id)
        assert updated.title == "Updated"
        
        # Delete
        delete_note(note_id, test_user.id)
        deleted = get_note_by_id(note_id, test_user.id)
        assert deleted.is_deleted is True
        
        # Restore
        restore_note(note_id, test_user.id)
        restored = get_note_by_id(note_id, test_user.id)
        assert restored.is_deleted is False

    def test_note_timestamps_are_set(self, test_user):
        """Note timestamps should be set automatically."""
        before = datetime.utcnow()
        note = create_note(test_user.id, "Title", "Content")
        after = datetime.utcnow()
        
        assert note.created_at is not None
        assert note.updated_at is not None
        assert before <= note.created_at <= after
        assert before <= note.updated_at <= after

    def test_note_updated_at_changes_on_update(self, test_user):
        """Note updated_at should change when note is modified."""
        note = create_note(test_user.id, "Title", "Content")
        original_updated_at = note.updated_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        updated_note = update_note(note.id, test_user.id, title="New Title")
        assert updated_note.updated_at >= original_updated_at

    def test_delete_preserves_timestamps(self, test_user):
        """Deleting note should not change created_at."""
        note = create_note(test_user.id, "Title", "Content")
        created_at = note.created_at
        
        deleted_note = delete_note(note.id, test_user.id)
        assert deleted_note.created_at == created_at

    def test_get_nonexistent_note_returns_none(self, test_user):
        """Should return None for non-existent note."""
        result = get_note_by_id(99999, test_user.id)
        assert result is None

    def test_delete_nonexistent_note_returns_false(self, test_user):
        """Should return False when deleting non-existent note."""
        result = delete_note(99999, test_user.id)
        assert result is False

    def test_restore_nonexistent_note_returns_false(self, test_user):
        """Should return False when restoring non-existent note."""
        result = restore_note(99999, test_user.id)
        assert result is False
