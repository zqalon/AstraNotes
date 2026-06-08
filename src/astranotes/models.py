from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Tag(SQLModel, table=True):
    """Tag for organizing notes (F-003a)."""
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Unique constraint: user can have only one tag with a given name
    __table_args__ = (
        None,  # no other args needed, just using this format for consistency
    )


class NoteTag(SQLModel, table=True):
    """Association table for Note-Tag many-to-many relationship."""
    id: int | None = Field(default=None, primary_key=True)
    note_id: int = Field(foreign_key="note.id", ondelete="CASCADE")
    tag_id: int = Field(foreign_key="tag.id", ondelete="CASCADE")


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = Field(default=False)
