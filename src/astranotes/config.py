from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'data' / 'astranotes.db'}"
SECRET_KEY = "change-me-in-production"
SESSION_MAX_AGE = 60 * 60 * 24
