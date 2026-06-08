"""Service layer for AstraNotes authentication and user data."""
import re

from passlib.context import CryptContext
from sqlmodel import Session, select

from astranotes.db import get_engine
from astranotes.models import User, Note, Tag, NoteTag

# Use argon2 for password hashing (modern, no length limits)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storage using argon2."""
    return pwd_context.hash(password)


def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def get_user_by_email(email: str) -> User | None:
    with Session(get_engine()) as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()


def get_user_by_username(username: str) -> User | None:
    with Session(get_engine()) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()


def get_user_by_id(user_id: int) -> User | None:
    with Session(get_engine()) as session:
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()


def create_user(email: str, username: str, password: str) -> User:
    if not validate_email(email):
        raise ValueError("Invalid email address")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if get_user_by_email(email) is not None:
        raise ValueError("Email is already registered")
    if get_user_by_username(username) is not None:
        raise ValueError("Username is already taken")

    user = User(email=email, username=username, hashed_password=get_password_hash(password))
    with Session(get_engine()) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def authenticate_user(identifier: str, password: str) -> User | None:
    user = get_user_by_email(identifier) or get_user_by_username(identifier)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


from datetime import datetime
from sqlalchemy import func


def create_note(user_id: int, title: str, content: str) -> Note:
    """Create and persist a new note for a user."""
    note = Note(user_id=user_id, title=title, content=content)
    with Session(get_engine()) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return note


def get_notes_for_user(user_id: int, include_deleted: bool = False) -> list[Note]:
    """Return notes for a user, optionally including deleted notes."""
    with Session(get_engine()) as session:
        statement = select(Note).where(Note.user_id == user_id)
        if not include_deleted:
            statement = statement.where(Note.is_deleted == False)
        return session.exec(statement).all()


def search_notes(
    user_id: int,
    q: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    tag_ids: list[int] | None = None,
    sort_by: str = "created_at",
    include_deleted: bool = False,
) -> list[Note]:
    """Search notes for a user with filtering and sorting options (F-003b, F-003c).

    - q: substring match against title and content (case-insensitive)
    - date_from / date_to: filter by `created_at` range (inclusive)
    - tag_ids: filter by tags (returns notes with ANY of these tags)
    - sort_by: "created_at", "updated_at", or "title" (default: "created_at")
    - include_deleted: include notes marked as deleted
    """
    with Session(get_engine()) as session:
        statement = select(Note).where(Note.user_id == user_id)

        if not include_deleted:
            statement = statement.where(Note.is_deleted == False)

        if q:
            q_norm = q.strip().lower()
            title_cond = func.lower(Note.title).contains(q_norm)
            content_cond = func.lower(Note.content).contains(q_norm)
            statement = statement.where(title_cond | content_cond)

        if date_from:
            statement = statement.where(Note.created_at >= date_from)
        if date_to:
            statement = statement.where(Note.created_at <= date_to)

        # Filter by tags if provided
        if tag_ids:
            statement = statement.join(NoteTag).where(NoteTag.tag_id.in_(tag_ids)).distinct()

        # Apply sorting
        if sort_by == "updated_at":
            statement = statement.order_by(Note.updated_at.desc())
        elif sort_by == "title":
            statement = statement.order_by(Note.title.asc())
        else:  # default to created_at
            statement = statement.order_by(Note.created_at.desc())

        return session.exec(statement).all()


def get_note_by_id(note_id: int, user_id: int) -> Note | None:
    """Get a note by ID, ensuring it belongs to the specified user."""
    with Session(get_engine()) as session:
        statement = select(Note).where(Note.id == note_id).where(Note.user_id == user_id)
        return session.exec(statement).first()


def update_note(note_id: int, user_id: int, title: str | None = None, content: str | None = None) -> Note | None:
    """Update a note's title and/or content. Returns the updated note or None if not found."""
    with Session(get_engine()) as session:
        note = session.exec(select(Note).where(Note.id == note_id).where(Note.user_id == user_id)).first()
        if not note:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        note.updated_at = datetime.utcnow()
        session.add(note)
        session.commit()
        session.refresh(note)
        return note


def delete_note(note_id: int, user_id: int) -> bool:
    """Soft-delete a note by setting is_deleted flag. Returns True if successful."""
    with Session(get_engine()) as session:
        note = session.exec(select(Note).where(Note.id == note_id).where(Note.user_id == user_id)).first()
        if not note:
            return False
        note.is_deleted = True
        note.updated_at = datetime.utcnow()
        session.add(note)
        session.commit()
        return True


def restore_note(note_id: int, user_id: int) -> bool:
    """Restore a soft-deleted note. Returns True if successful."""
    with Session(get_engine()) as session:
        note = session.exec(select(Note).where(Note.id == note_id).where(Note.user_id == user_id)).first()
        if not note:
            return False
        note.is_deleted = False
        note.updated_at = datetime.utcnow()
        session.add(note)
        session.commit()
        return True


# Tag Management Functions (F-003a)

def create_or_get_tag(user_id: int, tag_name: str) -> Tag:
    """Create a tag or return it if it already exists for the user."""
    tag_name = tag_name.strip().lower()
    with Session(get_engine()) as session:
        statement = select(Tag).where(Tag.user_id == user_id).where(Tag.name == tag_name)
        existing_tag = session.exec(statement).first()
        if existing_tag:
            return existing_tag
        
        tag = Tag(user_id=user_id, name=tag_name)
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag


def get_tags_for_user(user_id: int) -> list[Tag]:
    """Get all tags for a user."""
    with Session(get_engine()) as session:
        statement = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        return session.exec(statement).all()


def get_tags_for_note(note_id: int) -> list[Tag]:
    """Get all tags for a specific note."""
    with Session(get_engine()) as session:
        statement = (
            select(Tag)
            .join(NoteTag)
            .where(NoteTag.note_id == note_id)
            .order_by(Tag.name)
        )
        return session.exec(statement).all()


def add_tag_to_note(note_id: int, tag_id: int, user_id: int) -> bool:
    """Add a tag to a note. Returns False if note doesn't belong to user or tag doesn't belong to user."""
    with Session(get_engine()) as session:
        # Verify note belongs to user
        note = session.exec(select(Note).where(Note.id == note_id).where(Note.user_id == user_id)).first()
        if not note:
            return False
        
        # Verify tag belongs to user
        tag = session.exec(select(Tag).where(Tag.id == tag_id).where(Tag.user_id == user_id)).first()
        if not tag:
            return False
        
        # Check if tag already added to note
        existing = session.exec(
            select(NoteTag).where(NoteTag.note_id == note_id).where(NoteTag.tag_id == tag_id)
        ).first()
        if existing:
            return True  # Already tagged, no-op
        
        # Add the tag
        note_tag = NoteTag(note_id=note_id, tag_id=tag_id)
        session.add(note_tag)
        session.commit()
        return True


def remove_tag_from_note(note_id: int, tag_id: int, user_id: int) -> bool:
    """Remove a tag from a note. Returns False if note doesn't belong to user."""
    with Session(get_engine()) as session:
        # Verify note belongs to user
        note = session.exec(select(Note).where(Note.id == note_id).where(Note.user_id == user_id)).first()
        if not note:
            return False
        
        # Remove the tag association
        note_tag = session.exec(
            select(NoteTag).where(NoteTag.note_id == note_id).where(NoteTag.tag_id == tag_id)
        ).first()
        if note_tag:
            session.delete(note_tag)
            session.commit()
        return True


def delete_tag(tag_id: int, user_id: int) -> bool:
    """Delete a tag (and all its associations). Returns False if tag doesn't belong to user."""
    with Session(get_engine()) as session:
        tag = session.exec(select(Tag).where(Tag.id == tag_id).where(Tag.user_id == user_id)).first()
        if not tag:
            return False
        
        # Delete all associations
        note_tags = session.exec(select(NoteTag).where(NoteTag.tag_id == tag_id)).all()
        for nt in note_tags:
            session.delete(nt)
        
        session.delete(tag)
        session.commit()
        return True
