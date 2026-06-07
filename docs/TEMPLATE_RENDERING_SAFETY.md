# Template Rendering Safety Guide

## Problem Fixed
The application was experiencing `TypeError` errors with `TemplateResponse` calls due to API misuse and version incompatibilities with Starlette 0.37.2.

### Original Errors
1. **`TypeError: unhashable type: 'dict'`** - Caused when dict was passed where string expected
2. **`TypeError: Jinja2Templates.TemplateResponse() missing 1 required positional argument: 'name'`** - Caused by incorrect parameter ordering

## Solution Implemented

### 1. Safe Wrapper Function (Updated)
Created `render_template()` wrapper in [src/astranotes/routes.py](src/astranotes/routes.py) that:
- **Validates template name is a string** - Prevents passing dicts or other types
- **Validates context is a dict** - Ensures correct type
- **Validates 'request' key exists** - Required by Jinja2 for template rendering
- **Has clear type hints** - IDE support and type checking
- **Manually renders templates** - Bypasses Starlette 0.37.2 TemplateResponse API issues
- **Returns HTMLResponse** - Direct rendering avoids API compatibility problems

```python
def render_template(
    name: str, context: dict[str, Any], status_code: int = 200
) -> Response:
    """Safe wrapper for template rendering to prevent API misuse."""
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
```

### 2. Updated All Template Calls
Replaced direct `templates.TemplateResponse()` calls with `render_template()`:

```python
# BEFORE (error-prone)
return templates.TemplateResponse(
    "index.html",
    {"request": request, "title": "Home"},
)

# AFTER (safe)
return render_template(
    "index.html",
    {"request": request, "title": "Home"},
)
```

### 3. Added Regression Tests
Created [tests/test_template_rendering.py](tests/test_template_rendering.py) with:
- Validation tests for the wrapper function
- Integration tests for page loads
- Prevents API misuse regressions

## Usage Guidelines

### ✅ Correct Usage
```python
return render_template(
    "page.html",
    {
        "request": request,        # Always required
        "title": "Page Title",
        "user": current_user,
        "data": some_data,
    },
)

# With custom status code
return render_template(
    "error.html",
    {"request": request, "error": "Not Found"},
    status_code=404,
)
```

### ❌ Common Mistakes to Avoid
```python
# ❌ Wrong: Missing request
render_template("page.html", {"title": "Page"})

# ❌ Wrong: Context as positional argument (old API)
templates.TemplateResponse("page.html", {"request": request})

# ❌ Wrong: Using context= keyword without proper wrapper
templates.TemplateResponse("page.html", context={...})

# ❌ Wrong: Context before template name
render_template({"request": request}, "page.html")
```

## Starlette 0.37.2 Compatibility

The wrapper function ensures compatibility with Starlette 0.37.2 by:
- Using the correct positional argument order: `(name, context, status_code)`
- Validating inputs before passing to Starlette
- Providing clear error messages for API misuse

## Testing

Run the regression tests:
```bash
pytest tests/test_template_rendering.py -v
```

These tests verify:
1. Template rendering doesn't crash with malformed inputs
2. Pages load successfully without errors
3. API usage is validated at development time
