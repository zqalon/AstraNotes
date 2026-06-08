from pathlib import Path
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

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
    create_or_get_tag,
    get_tags_for_user,
    get_tags_for_note,
    add_tag_to_note,
    remove_tag_from_note,
    delete_tag,
)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
router = APIRouter()


def render_template(
    name: str, context: dict[str, Any], status_code: int = 200
) -> Response:
    """
    Safe wrapper for template rendering to prevent API misuse.
    
    Manually renders templates using Jinja2 to avoid Starlette 0.37.2 API issues.
    
    Args:
        name: Template filename (e.g., "index.html")
        context: Context dict (must include 'request' from FastAPI)
        status_code: HTTP status code (default 200)
    
    Returns:
        HTMLResponse with the rendered template
    """
    if not isinstance(name, str):
        raise TypeError(f"Template name must be str, got {type(name).__name__}")
    if not isinstance(context, dict):
        raise TypeError(f"Context must be dict, got {type(context).__name__}")
    if "request" not in context:
        raise ValueError("Context must include 'request' key")
    
    # Get the template and render it manually
    template = templates.get_template(name)
    content = template.render(context)
    return HTMLResponse(content, status_code=status_code)


def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


@router.get("/", response_class=HTMLResponse)
async def workspace(request: Request):
    current_user = get_current_user(request)
    return render_template(
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
    return render_template(
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
    return render_template(
        "settings.html",
        {
            "request": request,
            "title": "Settings",
            "user": current_user,
        },
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return render_template(
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
        return render_template(
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
    return render_template(
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
        return render_template(
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
    return render_template(
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
    tag_ids: str | None = None,
    sort_by: str = "created_at",
    include_deleted: bool = False,
):
    """Return notes for the current user with filtering and sorting (F-003b, F-003c).

    Query params:
    - `q`: substring search on title and content (case-insensitive)
    - `date_from`, `date_to`: ISO date strings to filter `created_at`
    - `tag_ids`: comma-separated list of tag IDs to filter by
    - `sort_by`: sort order - "created_at" (default), "updated_at", or "title"
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

    # Parse tag_ids
    parsed_tag_ids = None
    if tag_ids:
        try:
            parsed_tag_ids = [int(tid) for tid in tag_ids.split(",") if tid.strip()]
        except ValueError:
            parsed_tag_ids = None

    notes = search_notes(
        current_user.id,
        q=q,
        date_from=dt_from,
        date_to=dt_to,
        tag_ids=parsed_tag_ids,
        sort_by=sort_by,
        include_deleted=include_deleted,
    )

    result = []
    for n in notes:
        tags = get_tags_for_note(n.id)
        result.append(
            {
                "id": n.id,
                "user_id": n.user_id,
                "title": n.title,
                "content": n.content,
                "created_at": n.created_at.isoformat(),
                "updated_at": n.updated_at.isoformat(),
                "is_deleted": bool(n.is_deleted),
                "tags": [{"id": t.id, "name": t.name} for t in tags],
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


# Tag API Endpoints (F-003a - Categorization)

@router.get("/api/tags")
async def api_get_tags(request: Request):
    """Get all tags for the current user."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    tags = get_tags_for_user(current_user.id)
    return {
        "tags": [{"id": t.id, "name": t.name} for t in tags]
    }


@router.post("/api/tags")
async def api_create_tag(request: Request, name: str = Form(...)):
    """Create or get a tag for the current user."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    if not name or not name.strip():
        return {"error": "Tag name cannot be empty"}, 400

    tag = create_or_get_tag(current_user.id, name)
    return {"tag": {"id": tag.id, "name": tag.name}}


@router.delete("/api/tags/{tag_id}")
async def api_delete_tag(request: Request, tag_id: int):
    """Delete a tag."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    success = delete_tag(tag_id, current_user.id)
    if not success:
        return {"error": "Tag not found"}, 404

    return {"message": "Tag deleted successfully"}


@router.post("/api/notes/{note_id}/tags")
async def api_add_tag_to_note(request: Request, note_id: int, tag_id: int = Form(...)):
    """Add a tag to a note."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    success = add_tag_to_note(note_id, tag_id, current_user.id)
    if not success:
        return {"error": "Note or tag not found"}, 404

    return {"message": "Tag added successfully"}


@router.delete("/api/notes/{note_id}/tags/{tag_id}")
async def api_remove_tag_from_note(request: Request, note_id: int, tag_id: int):
    """Remove a tag from a note."""
    current_user = get_current_user(request)
    if not current_user:
        return {"error": "Unauthorized"}, 401

    success = remove_tag_from_note(note_id, tag_id, current_user.id)
    if not success:
        return {"error": "Note not found"}, 404

    return {"message": "Tag removed successfully"}
