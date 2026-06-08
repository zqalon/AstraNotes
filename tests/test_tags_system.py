"""System/E2E tests for tag feature workflows (F-003a Note Organization)."""
import pytest

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
    return create_user(
        email="systest@example.com",
        username="systestuser",
        password="TestPassword123"
    )


class TestCompleteTaggingWorkflow:
    """Test complete tagging workflows."""
    
    def test_workflow_create_and_organize_notes_with_tags(self, test_user):
        """
        System Test: User creates notes and organizes them with tags.
        
        Workflow:
        1. User creates multiple notes
        2. User creates tags
        3. User assigns tags to notes
        4. User filters notes by tags
        5. User removes tags
        """
        # Step 1: User creates notes
        python_note = create_note(test_user.id, "Python Basics", "Python fundamentals...")
        database_note = create_note(test_user.id, "Database Design", "Database patterns...")
        fullstack_note = create_note(test_user.id, "Full Stack Development", "End-to-end development...")
        
        # Step 2: User creates tags
        python_tag = create_or_get_tag(test_user.id, "python")
        database_tag = create_or_get_tag(test_user.id, "database")
        fullstack_tag = create_or_get_tag(test_user.id, "fullstack")
        tutorial_tag = create_or_get_tag(test_user.id, "tutorial")
        
        assert len(get_tags_for_user(test_user.id)) == 4
        
        # Step 3: User assigns tags to notes
        add_tag_to_note(python_note.id, python_tag.id, test_user.id)
        add_tag_to_note(python_note.id, tutorial_tag.id, test_user.id)
        
        add_tag_to_note(database_note.id, database_tag.id, test_user.id)
        add_tag_to_note(database_note.id, tutorial_tag.id, test_user.id)
        
        add_tag_to_note(fullstack_note.id, python_tag.id, test_user.id)
        add_tag_to_note(fullstack_note.id, database_tag.id, test_user.id)
        add_tag_to_note(fullstack_note.id, fullstack_tag.id, test_user.id)
        
        assert len(get_tags_for_note(python_note.id)) == 2
        assert len(get_tags_for_note(database_note.id)) == 2
        assert len(get_tags_for_note(fullstack_note.id)) == 3
        
        # Step 4: User filters notes by tags
        python_notes = search_notes(test_user.id, tag_ids=[python_tag.id])
        assert len(python_notes) == 2
        assert {n.id for n in python_notes} == {python_note.id, fullstack_note.id}
        
        tutorial_notes = search_notes(test_user.id, tag_ids=[tutorial_tag.id])
        assert len(tutorial_notes) == 2
        assert {n.id for n in tutorial_notes} == {python_note.id, database_note.id}
        
        # Step 5: User removes tags from a note
        remove_tag_from_note(fullstack_note.id, fullstack_tag.id, test_user.id)
        assert len(get_tags_for_note(fullstack_note.id)) == 2

    def test_workflow_sorting_notes(self, test_user):
        """
        System Test: User sorts notes by various criteria.
        
        Workflow:
        1. User creates notes with different titles
        2. User sorts by title
        3. User sorts by creation date
        """
        # Step 1: Create notes with specific titles
        zebra_note = create_note(test_user.id, "Zebra Language", "Content...")
        apple_note = create_note(test_user.id, "Apple Framework", "Content...")
        mango_note = create_note(test_user.id, "Mango Database", "Content...")
        
        # Step 2: Sort by title
        sorted_by_title = search_notes(test_user.id, sort_by="title")
        titles = [n.title for n in sorted_by_title]
        assert titles == ["Apple Framework", "Mango Database", "Zebra Language"]
        
        # Step 3: Sort by created_at (default, newest first)
        sorted_by_date = search_notes(test_user.id, sort_by="created_at")
        ids = [n.id for n in sorted_by_date]
        assert ids == [mango_note.id, apple_note.id, zebra_note.id]

    def test_workflow_combined_search_and_filter(self, test_user):
        """
        System Test: User searches and filters notes simultaneously.
        
        Workflow:
        1. User creates notes with different content
        2. User creates tags
        3. User searches by text AND filters by tag
        """
        # Step 1: Create notes
        python_api = create_note(test_user.id, "Python API", "REST API in Python...")
        python_web = create_note(test_user.id, "Python Web", "Web framework...")
        java_api = create_note(test_user.id, "Java API", "REST API in Java...")
        
        # Step 2: Create tags
        python_tag = create_or_get_tag(test_user.id, "python")
        api_tag = create_or_get_tag(test_user.id, "api")
        
        add_tag_to_note(python_api.id, python_tag.id, test_user.id)
        add_tag_to_note(python_api.id, api_tag.id, test_user.id)
        add_tag_to_note(python_web.id, python_tag.id, test_user.id)
        add_tag_to_note(java_api.id, api_tag.id, test_user.id)
        
        # Step 3: Search by text with tag filter
        # Search for "API" notes tagged with "python"
        results = search_notes(test_user.id, q="API", tag_ids=[python_tag.id])
        assert len(results) == 1
        assert results[0].id == python_api.id

    def test_workflow_manage_tags(self, test_user):
        """
        System Test: User manages their tag library.
        
        Workflow:
        1. User creates several tags
        2. User views all tags
        3. User deletes unused tags
        """
        # Step 1: Create tags
        python_tag = create_or_get_tag(test_user.id, "python")
        javascript_tag = create_or_get_tag(test_user.id, "javascript")
        ruby_tag = create_or_get_tag(test_user.id, "ruby")
        
        # Step 2: View all tags
        all_tags = get_tags_for_user(test_user.id)
        assert len(all_tags) == 3
        tag_names = {t.name for t in all_tags}
        assert tag_names == {"python", "javascript", "ruby"}
        
        # Step 3: Delete unused tag (ruby)
        delete_tag(ruby_tag.id, test_user.id)
        remaining_tags = get_tags_for_user(test_user.id)
        assert len(remaining_tags) == 2
        remaining_names = {t.name for t in remaining_tags}
        assert remaining_names == {"python", "javascript"}

    def test_workflow_retagging_notes(self, test_user):
        """
        System Test: User retags notes as their understanding evolves.
        
        Workflow:
        1. User creates a note and tags it
        2. User adds more tags
        3. User removes incorrect tags
        4. User verifies final state
        """
        # Step 1: Create and tag a note
        note = create_note(test_user.id, "Learning Journey", "Started learning web dev...")
        frontend_tag = create_or_get_tag(test_user.id, "frontend")
        add_tag_to_note(note.id, frontend_tag.id, test_user.id)
        
        assert len(get_tags_for_note(note.id)) == 1
        
        # Step 2: Add more tags
        backend_tag = create_or_get_tag(test_user.id, "backend")
        fullstack_tag = create_or_get_tag(test_user.id, "fullstack")
        add_tag_to_note(note.id, backend_tag.id, test_user.id)
        add_tag_to_note(note.id, fullstack_tag.id, test_user.id)
        
        assert len(get_tags_for_note(note.id)) == 3
        
        # Step 3: Remove incorrect tag
        remove_tag_from_note(note.id, frontend_tag.id, test_user.id)
        
        # Step 4: Verify final state
        final_tags = get_tags_for_note(note.id)
        assert len(final_tags) == 2
        final_tag_names = {t.name for t in final_tags}
        assert final_tag_names == {"backend", "fullstack"}


class TestEdgeCasesAndBoundaries:
    """Test edge cases and boundary conditions."""
    
    def test_many_tags_per_note(self, test_user):
        """Test adding many tags to a single note."""
        note = create_note(test_user.id, "Multi-tagged Note", "Content...")
        
        # Add 10 tags
        tags = []
        for i in range(10):
            tag = create_or_get_tag(test_user.id, f"tag{i}")
            add_tag_to_note(note.id, tag.id, test_user.id)
            tags.append(tag)
        
        note_tags = get_tags_for_note(note.id)
        assert len(note_tags) == 10

    def test_note_with_no_tags_in_filtered_search(self, test_user):
        """Test that untagged notes don't appear in tag-filtered searches."""
        tagged_note = create_note(test_user.id, "Tagged", "Content...")
        untagged_note = create_note(test_user.id, "Untagged", "Content...")
        
        tag = create_or_get_tag(test_user.id, "tagged")
        add_tag_to_note(tagged_note.id, tag.id, test_user.id)
        
        results = search_notes(test_user.id, tag_ids=[tag.id])
        assert len(results) == 1
        assert results[0].id == tagged_note.id

    def test_special_characters_in_tag_names(self, test_user):
        """Test tags with special characters."""
        tag = create_or_get_tag(test_user.id, "c++/rust#1")
        assert tag.name == "c++/rust#1"

    def test_unicode_in_tag_names(self, test_user):
        """Test tags with Unicode characters."""
        tag = create_or_get_tag(test_user.id, "Python 🐍")
        note = create_note(test_user.id, "Note", "Content...")
        add_tag_to_note(note.id, tag.id, test_user.id)
        
        note_tags = get_tags_for_note(note.id)
        assert len(note_tags) == 1
        assert note_tags[0].name == "python 🐍"  # lowercased but unicode preserved

    def test_very_long_tag_name(self, test_user):
        """Test very long tag names."""
        long_name = "a" * 255  # Very long tag name
        tag = create_or_get_tag(test_user.id, long_name)
        assert tag.name == long_name

    def test_sorting_with_empty_results(self, test_user):
        """Test sorting when no results match."""
        create_note(test_user.id, "Only Note", "Content...")
        tag = create_or_get_tag(test_user.id, "unused-tag")
        
        results = search_notes(test_user.id, tag_ids=[tag.id], sort_by="title")
        assert len(results) == 0
