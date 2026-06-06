from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from astranotes.services import (
    authenticate_user,
    create_user,
    get_user_by_id,
    create_note,
    search_notes,
    get_note_by_id,
    update_note,
    delete_note,
    restore_note,
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
router = APIRouter()


def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


@router.get("/", response_class=HTMLResponse)
async def workspace(request: Request):
    current_user = get_current_user(request)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Workspace",
            "user": current_user,
        },
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    current_user = get_current_user(request)
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "title": "Profile",
            "user": current_user,
        },
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    current_user = get_current_user(request)
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "title": "Settings",
            "user": current_user,
        },
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "title": "Register", "error": None},
    )


@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    try:
        user = create_user(email=email, username=username, password=password)
        request.session["user_id"] = user.id
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    except ValueError as exc:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "title": "Register",
                "error": str(exc),
                "username": username,
                "email": email,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "Login", "error": None},
    )


@router.post("/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    identifier: str = Form(...),
    password: str = Form(...),
):
    user = authenticate_user(identifier=identifier, password=password)
    if user is None:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "title": "Login",
                "error": "Invalid username/email or password.",
                "identifier": identifier,
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@router.get("/architecture", response_class=HTMLResponse)
async def architecture(request: Request):
    current_user = get_current_user(request)
    return templates.TemplateResponse(
        "architecture.html",
        {
            "request": request,
            "title": "Architecture",
            "user": current_user,
        },
    )


@router.get("/api/notes")
async def api_get_notes(
    request: Request,
    q: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    include_deleted: bool = False,
):
    """Return notes for the current user with basic filtering.

    Query params:
    - `q`: substring search on title and content (case-insensitive)
    - `date_from`, `date_to`: ISO date strings to filter `created_at`
    - `include_deleted`: include soft-deleted notes
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    dt_from = None
    dt_to = None
    try:
        if date_from:
            dt_from = datetime.fromisoformat(date_from)
        if date_to:
            dt_to = datetime.fromisoformat(date_to)
    except ValueError:
        dt_from = None
        dt_to = None

    notes = search_notes(
        current_user.id, q=q, date_from=dt_from, date_to=dt_to, include_deleted=include_deleted
    )

    result = []
    for n in notes:
        result.append(
            {
                "id": n.id,
                "user_id": n.user_id,
                "title": n.title,
                "content": n.content,
                "created_at": n.created_at.isoformat(),
                "updated_at": n.updated_at.isoformat(),
                "is_deleted": bool(n.is_deleted),
            }
        )

    return {"notes": result}


@router.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "AstraNotes"}


@router.post("/api/notes")
async def api_create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
):
    """Create a new note for the current user."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    note = create_note(user_id=current_user.id, title=title, content=content)
    return {
        "id": note.id,
        "user_id": note.user_id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "is_deleted": bool(note.is_deleted),
    }


@router.get("/api/notes/{note_id}")
async def api_get_note(request: Request, note_id: int):
    """Get a specific note by ID."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    note = get_note_by_id(note_id=note_id, user_id=current_user.id)
    if not note:
        return {"error": "Note not found"}, 404

    return {
        "id": note.id,
        "user_id": note.user_id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "is_deleted": bool(note.is_deleted),
    }


@router.put("/api/notes/{note_id}")
async def api_update_note(
    request: Request,
    note_id: int,
    title: str | None = Form(None),
    content: str | None = Form(None),
):
    """Update a specific note."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    note = update_note(note_id=note_id, user_id=current_user.id, title=title, content=content)
    if not note:
        return {"error": "Note not found"}, 404

    return {
        "id": note.id,
        "user_id": note.user_id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
        "is_deleted": bool(note.is_deleted),
    }


@router.delete("/api/notes/{note_id}")
async def api_delete_note(request: Request, note_id: int):
    """Soft-delete a note."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    success = delete_note(note_id=note_id, user_id=current_user.id)
    if not success:
        return {"error": "Note not found"}, 404

    return {"message": "Note deleted successfully"}


@router.post("/api/notes/{note_id}/restore")
async def api_restore_note(request: Request, note_id: int):
    """Restore a soft-deleted note."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    success = restore_note(note_id=note_id, user_id=current_user.id)
    if not success:
        return {"error": "Note not found"}, 404

    return {"message": "Note restored successfully"}
