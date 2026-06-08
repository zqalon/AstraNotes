# AstraNotes

AstraNotes is a Python-based web application skeleton for secure note-taking and management.

## Structure

- `src/astranotes/` — application package
- `tests/` — unit and integration test stubs
- `docs/` — architecture, setup, and design notes
- `pyproject.toml` — build and dependency metadata
- `requirements.txt` — runtime dependencies
- `Makefile` — common build/test commands

## Requirements

- **Python 3.10+** (tested with Python 3.12)
- **pip** and **venv** (included with Python)
- **SQLite** (included with Python)

## Quick start

### 1. Clone and navigate to the project
```bash
cd AstraNotes
```

### 2. Create and activate a virtual environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Or on Windows:
# .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

This installs:
- **FastAPI** — web framework
- **Uvicorn** — ASGI server
- **SQLModel** — ORM and data validation
- **Passlib + Argon2** — password hashing with modern and legacy support
- **Jinja2** — template rendering

### 4. Run the development server
```bash
uvicorn astranotes.main:app --reload
```

The app will start at **http://127.0.0.1:8000**

### 5. Access the application

Open your browser and navigate to:
- **Home**: http://127.0.0.1:8000
- **Login**: http://127.0.0.1:8000/login
- **Register**: http://127.0.0.1:8000/register

### Test Credentials

If you want to test with an existing account:
- **Username**: `zalon`
- **Password**: `zach1010`

Or register a new account through the web interface.

## Development Commands

### Using Make (recommended)
```bash
make install    # Install dependencies
make lint       # Run code style checks
make test       # Run test suite
make docs       # Build documentation
make help       # Show all available commands
```

### Manual commands
```bash
# Run tests
pytest tests/

# Run linting
python -m pylint src/

# Run type checking
mypy src/
```

## Troubleshooting

### Port 8000 is already in use
```bash
# Kill the existing process
pkill -f uvicorn

# Then restart the server
uvicorn astranotes.main:app --reload
```

### Module not found errors
Make sure you've activated the virtual environment:
```bash
source .venv/bin/activate
```

### Password hashing errors
The app uses dual-scheme password hashing (Argon2 for new passwords, Bcrypt for legacy support). Both backends are automatically installed with `requirements.txt`. If you see hashing errors:
```bash
pip install argon2-cffi passlib
```

### Database issues
The app uses SQLite with the database file at `data/notes.db`. If you need to reset:
```bash
rm data/notes.db
# The database will be recreated on next app startup
```

## Project Structure

```
├── src/astranotes/          # Main application package
│   ├── main.py              # FastAPI app initialization
│   ├── routes.py            # Route handlers
│   ├── models.py            # SQLModel data models
│   ├── services.py          # Business logic & authentication
│   ├── db.py                # Database configuration
│   ├── config.py            # Settings
│   └── templates/           # HTML templates (Jinja2)
├── tests/                   # Test suite
├── docs/                    # Architecture and design docs
├── Planning/                # Project planning and status
├── requirements.txt         # Python dependencies
└── Makefile                 # Build and development tasks
```
