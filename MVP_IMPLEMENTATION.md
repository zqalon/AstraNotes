# AstraNotes MVP Implementation

## Overview

This document describes the Minimum Viable Product (MVP) implementation of AstraNotes for a college software development class (CSEN 296). The MVP implements core note-taking functionality with user authentication, CRUD operations, and a web interface.

## Scope

The MVP fulfills the following requirements from the project scope:

### Functional Requirements (Implemented)

#### F-001: User Authentication & Authorization ✓
- User registration with email/username and password
- Secure login/logout functionality
- Session management with 24-hour timeout
- Password validation (minimum 8 characters)
- Email validation

#### F-002: Note CRUD Operations ✓
- Create new notes with title and content
- Read/view notes (individual and list views)
- Update/edit existing notes
- Delete notes (soft delete with recovery option)
- Automatic timestamp management (created_at, updated_at)

#### F-003: Note Organization & Discovery ✓
- Full-text search across note titles and content (case-insensitive)
- Search results displayed with relevant metadata
- Sorting by creation/modification date (most recent first)

#### F-004: Command Line Interface (Stub) ⧗
- Infrastructure in place for future CLI development
- Not implemented in MVP

#### F-005: Web Interface ✓
- Browser-based note management interface
- Intuitive note editor with title and content fields
- List view showing all user notes
- Search functionality with real-time filtering
- Modal-based note creation and editing
- Responsive design

### Non-Functional Requirements (Implemented)

#### NF-001: User Experience ✓
- Intuitive interface design with clean UI/UX
- Responsive layout that adapts to different screen sizes
- Fast, interactive note management
- Clear visual feedback for actions

#### NF-002: Maintainability ✓
- Modular architecture (services, routes, models layers)
- Comprehensive code organization
- Automated testing framework (pytest)
- Code quality standards with type hints

### Security Requirements (Implemented)

#### SEC-001: Data Protection ✓
- Secure password hashing using bcrypt
- Protection against SQL injection via SQLModel ORM
- Protection against XSS via template escaping
- Protection against CSRF via session-based authentication
- Input validation for email and password

#### SEC-002: Privacy & Compliance ✓
- Session-based authentication (secure cookies)
- User data isolated per authenticated user
- Soft delete (recovery-friendly data management)
- Audit trail via timestamps

## Architecture

### Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite (development-friendly, self-contained)
- **ORM**: SQLModel (combines SQLAlchemy and Pydantic)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Authentication**: Session-based (Starlette SessionMiddleware)
- **Password Hashing**: bcrypt via passlib
- **Testing**: pytest + TestClient

### Project Structure

```
src/astranotes/
├── main.py          # FastAPI application setup
├── config.py        # Configuration (DB URL, secrets)
├── models.py        # SQLModel database schemas
├── db.py            # Database initialization
├── services.py      # Business logic (authentication, notes CRUD)
├── routes.py        # API endpoints and page routes
├── templates/       # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── ...
└── static/          # CSS and static assets
    └── style.css

tests/
├── test_auth.py     # Authentication tests
├── test_health.py   # API health check tests
└── test_notes.py    # Note CRUD tests
```

### Data Models

#### User
```python
class User(SQLModel, table=True):
    id: int (Primary Key)
    username: str (unique)
    email: str (unique)
    hashed_password: str
    created_at: datetime
```

#### Note
```python
class Note(SQLModel, table=True):
    id: int (Primary Key)
    user_id: int (Foreign Key → User.id)
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool (soft delete flag)
```

## API Endpoints

### Authentication Routes
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Registration page
- `POST /register` - Process registration
- `GET /logout` - Logout and clear session

### Page Routes
- `GET /` - Main workspace (requires authentication)
- `GET /profile` - User profile page
- `GET /settings` - Settings page
- `GET /architecture` - Architecture documentation page

### API Endpoints (JSON)
- `GET /api/health` - Health check
- `GET /api/notes` - List user's notes (supports search)
  - Query parameters: `q` (search term), `date_from`, `date_to`, `include_deleted`
- `POST /api/notes` - Create note
  - Form data: `title`, `content`
- `GET /api/notes/{id}` - Get specific note
- `PUT /api/notes/{id}` - Update note
  - Form data: `title`, `content` (optional)
- `DELETE /api/notes/{id}` - Soft-delete note
- `POST /api/notes/{id}/restore` - Restore deleted note

## Key Features

### 1. User Authentication
- Registration with validation (email format, password strength)
- Login with email or username
- Secure password hashing with bcrypt
- Session-based authentication (24-hour expiration)
- Logout functionality

### 2. Note Management
- Create notes with title and content
- Edit notes with automatic timestamp updates
- Soft delete (recoverable)
- View individual notes with metadata
- List all notes for the user

### 3. Search & Discovery
- Real-time search across note titles and content
- Case-insensitive text matching
- Date range filtering (for future enhancement)
- Results ordered by most recent first

### 4. User Interface
- Clean, responsive design
- Modal-based note editing
- Interactive note list with preview
- Action buttons (Edit, Delete)
- Search box with debounced input
- Navigation sidebar

## Running the Application

### Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Development Server
```bash
uvicorn astranotes.main:app --reload
```

Access the application at `http://127.0.0.1:8000`

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=astranotes tests/
```

## Implementation Details

### Service Layer (services.py)

The service layer provides business logic and database operations:

```python
# Authentication
create_user(email, username, password)
authenticate_user(identifier, password)
get_user_by_id(user_id)

# Note Management
create_note(user_id, title, content)
get_notes_for_user(user_id, include_deleted=False)
get_note_by_id(note_id, user_id)
update_note(note_id, user_id, title=None, content=None)
delete_note(note_id, user_id)  # Soft delete
restore_note(note_id, user_id)  # Restore soft-deleted

# Search
search_notes(user_id, q=None, date_from=None, date_to=None, include_deleted=False)
```

### Frontend Interaction

The index.html implements a single-page application that:
1. Loads notes on page load via `/api/notes`
2. Displays notes in a card-based list
3. Provides a modal for creating/editing notes
4. Handles search with 500ms debounce
5. Manages CRUD operations via REST API calls
6. Provides user feedback through alerts and UI updates

## Testing

### Test Coverage

- **test_auth.py**: Registration, login, authentication flows
- **test_health.py**: API health check endpoint
- **test_notes.py**: Note creation, search, and CRUD operations

### Running Tests
```bash
pytest tests/ -v
```

All tests pass successfully, validating core MVP functionality.

## Deployment Considerations

For production deployment:

1. **Configuration**: Update `SECRET_KEY` in config.py
2. **Database**: Switch from SQLite to PostgreSQL
3. **HTTPS**: Enable TLS/SSL termination
4. **Environment Variables**: Use .env files for secrets
5. **Session Security**: Configure session cookie settings
6. **CORS**: Configure if serving SPA from different origin
7. **Logging**: Add structured logging
8. **Error Handling**: Implement comprehensive error handling

## Future Enhancements

Based on the requirements spec, these features can be added:

1. **CLI Interface** (F-004)
   - Command-line tool for note management
   - Interactive menus and keyboard shortcuts

2. **Advanced Organization** (F-003a, F-003e)
   - Folder/category system
   - Tags for notes
   - Favorites/bookmarking

3. **Version History** (F-003d)
   - Track note changes over time
   - Ability to view and restore previous versions

4. **Bulk Operations** (F-002e)
   - Batch delete multiple notes
   - Bulk tag assignment

5. **Advanced Search** (F-003c)
   - Filter by date range
   - Filter by category/tags
   - Search result highlighting

6. **Desktop GUI** (F-005)
   - Cross-platform application
   - Rich text editor
   - Tree view for organization

7. **Encryption** (SEC-001a)
   - End-to-end encryption
   - Zero-knowledge architecture

## Conclusion

This MVP provides a solid foundation for AstraNotes, implementing core functionality needed for a secure note-taking application. The architecture is modular and extensible, allowing for easy addition of planned features. All code is well-tested and documented, making it suitable for classroom learning and demonstration.

---

**Implementation Date**: June 2025  
**Target Audience**: CSEN 296 Software Development Class  
**Status**: Ready for demonstration and testing
