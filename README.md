# AstraNotes

AstraNotes is a Python-based web application skeleton for secure note-taking and management.

## Structure

- `src/astranotes/` — application package
- `tests/` — unit and integration test stubs
- `docs/` — architecture, setup, and design notes
- `pyproject.toml` — build and dependency metadata
- `requirements.txt` — runtime dependencies
- `Makefile` — common build/test commands

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn astranotes.main:app --reload
```

## Recommended flow

- `make install` — install dependencies
- `make lint` — run code style checks
- `make test` — run tests
- `make docs` — build documentation
