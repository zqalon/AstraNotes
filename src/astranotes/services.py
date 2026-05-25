"""Service layer for AstraNotes authentication and user data."""
import re

from passlib.context import CryptContext
from sqlmodel import Session, select

from astranotes.db import get_engine
from astranotes.models import User, Note

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
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
    include_deleted: bool = False,
) -> list[Note]:
    """Search notes for a user with simple filtering options.

    - q: substring match against title and content (case-insensitive)
    - date_from / date_to: filter by `created_at` range (inclusive)
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

        statement = statement.order_by(Note.created_at.desc())
        return session.exec(statement).all()
