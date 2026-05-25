from pathlib import Path

from sqlalchemy import create_engine
from sqlmodel import SQLModel
from astranotes.config import DATABASE_URL
from astranotes.models import User, Note


def init_db() -> None:
    db_path = Path(DATABASE_URL.replace("sqlite://", ""))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)


def get_engine():
    return create_engine(DATABASE_URL, echo=False)
