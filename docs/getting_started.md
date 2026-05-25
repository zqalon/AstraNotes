# Getting Started with AstraNotes

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the development server:
   ```bash
   uvicorn astranotes.main:app --reload
   ```

## Local development

- Access the health endpoint at `http://127.0.0.1:8000/api/health`
- Add application routes under `src/astranotes/routes.py`
- Add models and persistence logic in `src/astranotes/models.py` and `src/astranotes/db.py`

## Testing

Run tests with:

```bash
pytest tests
```
