"""Unit tests for tag services (F-003a Note Organization)."""
import pytest
from datetime import datetime

from astranotes.models import User, Note, Tag, NoteTag
from astranotes.services import (
    create_user,
    create_note,
    create_or_get_tag,
    get_tags_for_user,
    get_tags_for_note,
    add_tag_to_note,
    remove_tag_from_note,
    delete_tag,
    search_notes,
)


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = create_user(
        email="tagtest@example.com",
        username="tagtestuser",
        password="TestPassword123"
    )
    return user


@pytest.fixture
def test_note(test_user):
    """Create a test note."""
    return create_note(
        user_id=test_user.id,
        title="Test Note",
        content="This is a test note"
    )


class TestTagCreation:
    """Test tag creation and retrieval."""
    
    def test_create_or_get_tag_creates_new_tag(self, test_user):
        """Test creating a new tag."""
        tag = create_or_get_tag(test_user.id, "python")
        assert tag.name == "python"
        assert tag.user_id == test_user.id
        assert tag.id is not None

    def test_create_or_get_tag_returns_existing_tag(self, test_user):
        """Test that getting an existing tag returns the same tag."""
        tag1 = create_or_get_tag(test_user.id, "python")
        tag2 = create_or_get_tag(test_user.id, "python")
        assert tag1.id == tag2.id
        assert tag1.name == tag2.name

    def test_create_or_get_tag_case_insensitive(self, test_user):
        """Test that tag names are case-insensitive."""
        tag1 = create_or_get_tag(test_user.id, "Python")
        tag2 = create_or_get_tag(test_user.id, "PYTHON")
        assert tag1.id == tag2.id

    def test_create_or_get_tag_trims_whitespace(self, test_user):
        """Test that tag names have whitespace trimmed."""
        tag = create_or_get_tag(test_user.id, "  python  ")
        assert tag.name == "python"

    def test_get_tags_for_user_returns_all_tags(self, test_user):
        """Test retrieving all tags for a user."""
        tag1 = create_or_get_tag(test_user.id, "python")
        tag2 = create_or_get_tag(test_user.id, "javascript")
        tag3 = create_or_get_tag(test_user.id, "database")
        
        tags = get_tags_for_user(test_user.id)
        assert len(tags) == 3
        tag_names = {t.name for t in tags}
        assert tag_names == {"python", "javascript", "database"}

    def test_get_tags_for_user_sorted_by_name(self, test_user):
        """Test that tags are returned sorted by name."""
        create_or_get_tag(test_user.id, "zebra")
        create_or_get_tag(test_user.id, "apple")
        create_or_get_tag(test_user.id, "banana")
        
        tags = get_tags_for_user(test_user.id)
        tag_names = [t.name for t in tags]
        assert tag_names == ["apple", "banana", "zebra"]


class TestNoteTagAssociation:
    """Test adding/removing tags from notes."""
    
    def test_add_tag_to_note(self, test_user, test_note):
        """Test adding a tag to a note."""
        tag = create_or_get_tag(test_user.id, "important")
        success = add_tag_to_note(test_note.id, tag.id, test_user.id)
        assert success is True
        
        note_tags = get_tags_for_note(test_note.id)
        assert len(note_tags) == 1
        assert note_tags[0].id == tag.id

    def test_add_multiple_tags_to_note(self, test_user, test_note):
        """Test adding multiple tags to a note."""
        tag1 = create_or_get_tag(test_user.id, "python")
        tag2 = create_or_get_tag(test_user.id, "tutorial")
        tag3 = create_or_get_tag(test_user.id, "important")
        
        add_tag_to_note(test_note.id, tag1.id, test_user.id)
        add_tag_to_note(test_note.id, tag2.id, test_user.id)
        add_tag_to_note(test_note.id, tag3.id, test_user.id)
        
        note_tags = get_tags_for_note(test_note.id)
        assert len(note_tags) == 3

    def test_add_tag_twice_is_idempotent(self, test_user, test_note):
        """Test that adding the same tag twice is idempotent."""
        tag = create_or_get_tag(test_user.id, "python")
        
        success1 = add_tag_to_note(test_note.id, tag.id, test_user.id)
        success2 = add_tag_to_note(test_note.id, tag.id, test_user.id)
        
        assert success1 is True
        assert success2 is True
        
        note_tags = get_tags_for_note(test_note.id)
        assert len(note_tags) == 1  # Only added once

    def test_add_tag_to_nonexistent_note_fails(self, test_user):
        """Test that adding a tag to a non-existent note fails."""
        tag = create_or_get_tag(test_user.id, "python")
        success = add_tag_to_note(999, tag.id, test_user.id)
        assert success is False

    def test_add_nonexistent_tag_fails(self, test_user, test_note):
        """Test that adding a non-existent tag fails."""
        success = add_tag_to_note(test_note.id, 999, test_user.id)
        assert success is False

    def test_add_tag_from_different_user_fails(self, test_user, test_note):
        """Test that adding a tag from a different user fails."""
        other_user = create_user(
            email="other@example.com",
            username="otheruser",
            password="OtherPassword123"
        )
        tag = create_or_get_tag(other_user.id, "python")
        
        success = add_tag_to_note(test_note.id, tag.id, test_user.id)
        assert success is False

    def test_remove_tag_from_note(self, test_user, test_note):
        """Test removing a tag from a note."""
        tag = create_or_get_tag(test_user.id, "important")
        add_tag_to_note(test_note.id, tag.id, test_user.id)
        
        success = remove_tag_from_note(test_note.id, tag.id, test_user.id)
        assert success is True
        
        note_tags = get_tags_for_note(test_note.id)
        assert len(note_tags) == 0

    def test_remove_tag_from_nonexistent_note_fails(self, test_user):
        """Test that removing a tag from a non-existent note fails."""
        tag = create_or_get_tag(test_user.id, "python")
        success = remove_tag_from_note(999, tag.id, test_user.id)
        assert success is False

    def test_remove_tag_that_wasnt_on_note(self, test_user, test_note):
        """Test that removing a tag that wasn't on the note is safe."""
        tag = create_or_get_tag(test_user.id, "python")
        success = remove_tag_from_note(test_note.id, tag.id, test_user.id)
        assert success is True  # Safe no-op


class TestTagDeletion:
    """Test tag deletion."""
    
    def test_delete_tag(self, test_user):
        """Test deleting a tag."""
        tag = create_or_get_tag(test_user.id, "python")
        success = delete_tag(tag.id, test_user.id)
        assert success is True
        
        tags = get_tags_for_user(test_user.id)
        assert len(tags) == 0

    def test_delete_tag_with_associated_notes(self, test_user, test_note):
        """Test deleting a tag removes associations."""
        tag = create_or_get_tag(test_user.id, "python")
        add_tag_to_note(test_note.id, tag.id, test_user.id)
        
        success = delete_tag(tag.id, test_user.id)
        assert success is True
        
        note_tags = get_tags_for_note(test_note.id)
        assert len(note_tags) == 0

    def test_delete_nonexistent_tag_fails(self, test_user):
        """Test that deleting a non-existent tag fails."""
        success = delete_tag(999, test_user.id)
        assert success is False

    def test_delete_tag_from_different_user_fails(self, test_user):
        """Test that deleting another user's tag fails."""
        other_user = create_user(
            email="other@example.com",
            username="otheruser",
            password="OtherPassword123"
        )
        tag = create_or_get_tag(other_user.id, "python")
        
        success = delete_tag(tag.id, test_user.id)
        assert success is False


class TestSearchWithTags:
    """Test searching notes with tag filtering."""
    
    def test_search_notes_by_single_tag(self, test_user):
        """Test searching notes by a single tag."""
        note1 = create_note(test_user.id, "Python Note", "Content 1")
        note2 = create_note(test_user.id, "JS Note", "Content 2")
        note3 = create_note(test_user.id, "Python Async", "Content 3")
        
        python_tag = create_or_get_tag(test_user.id, "python")
        js_tag = create_or_get_tag(test_user.id, "javascript")
        
        add_tag_to_note(note1.id, python_tag.id, test_user.id)
        add_tag_to_note(note2.id, js_tag.id, test_user.id)
        add_tag_to_note(note3.id, python_tag.id, test_user.id)
        
        results = search_notes(test_user.id, tag_ids=[python_tag.id])
        assert len(results) == 2
        result_ids = {r.id for r in results}
        assert result_ids == {note1.id, note3.id}

    def test_search_notes_by_multiple_tags(self, test_user):
        """Test searching notes by multiple tags (OR logic)."""
        note1 = create_note(test_user.id, "Note 1", "Content 1")
        note2 = create_note(test_user.id, "Note 2", "Content 2")
        note3 = create_note(test_user.id, "Note 3", "Content 3")
        
        python_tag = create_or_get_tag(test_user.id, "python")
        js_tag = create_or_get_tag(test_user.id, "javascript")
        
        add_tag_to_note(note1.id, python_tag.id, test_user.id)
        add_tag_to_note(note2.id, js_tag.id, test_user.id)
        
        results = search_notes(test_user.id, tag_ids=[python_tag.id, js_tag.id])
        assert len(results) == 2
        result_ids = {r.id for r in results}
        assert result_ids == {note1.id, note2.id}


class TestSortingNotes:
    """Test sorting functionality (F-003c)."""
    
    def test_sort_by_created_at_desc(self, test_user):
        """Test sorting by created_at descending (default)."""
        note1 = create_note(test_user.id, "First", "Content 1")
        note2 = create_note(test_user.id, "Second", "Content 2")
        note3 = create_note(test_user.id, "Third", "Content 3")
        
        results = search_notes(test_user.id, sort_by="created_at")
        assert [r.id for r in results] == [note3.id, note2.id, note1.id]

    def test_sort_by_title_asc(self, test_user):
        """Test sorting by title ascending."""
        note1 = create_note(test_user.id, "Zebra", "Content 1")
        note2 = create_note(test_user.id, "Apple", "Content 2")
        note3 = create_note(test_user.id, "Banana", "Content 3")
        
        results = search_notes(test_user.id, sort_by="title")
        assert [r.title for r in results] == ["Apple", "Banana", "Zebra"]

    def test_sort_by_updated_at(self, test_user):
        """Test sorting by updated_at."""
        note1 = create_note(test_user.id, "Note 1", "Content 1")
        note2 = create_note(test_user.id, "Note 2", "Content 2")
        note3 = create_note(test_user.id, "Note 3", "Content 3")
        
        results = search_notes(test_user.id, sort_by="updated_at")
        # All should have same updated_at (from creation), so order is insertion order desc
        assert [r.id for r in results] == [note3.id, note2.id, note1.id]
