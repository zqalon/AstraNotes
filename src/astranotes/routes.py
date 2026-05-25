from pathlib import Path

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from astranotes.services import (
    authenticate_user,
    create_user,
    get_user_by_id,
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


@router.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "AstraNotes"}
