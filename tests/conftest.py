"""Pytest configuration and fixtures for AstraNotes tests."""
import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from astranotes.models import User, Note, Tag, NoteTag


@pytest.fixture(name="db_session")
def db_session_fixture(monkeypatch):
    """Create a test database session and monkeypatch get_engine to use it."""
    # Create an in-memory SQLite database for testing
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    SQLModel.metadata.create_all(test_engine)
    
    # Monkeypatch get_engine to return test engine
    import astranotes.services
    monkeypatch.setattr(astranotes.services, "get_engine", lambda: test_engine)
    
    with Session(test_engine) as session:
        yield session
