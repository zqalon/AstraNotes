# AstraNotes Architecture

## Overview

AstraNotes is built as a Python web application with FastAPI.
The app separates responsibilities into:

- `src/astranotes/main.py` — application startup and router registration
- `src/astranotes/routes.py` — API endpoints
- `src/astranotes/models.py` — data models and schema definitions
- `src/astranotes/db.py` — database engine and initialization
- `src/astranotes/services.py` — business logic layer

## Data model

- `User` stores authentication and account metadata.
- `Note` stores note content and timestamps, with basic soft-delete support.
