"""Test template rendering to prevent TemplateResponse API misuse."""

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from astranotes.main import app
from astranotes.routes import render_template


client = TestClient(app)


def test_render_template_requires_request_in_context():
    """Ensure render_template validates context includes request."""
    with pytest.raises(ValueError, match="Context must include 'request' key"):
        render_template("index.html", {"title": "Test"})


def test_render_template_requires_dict_context():
    """Ensure render_template validates context is a dict."""
    mock_request = None
    with pytest.raises(TypeError, match="Context must be dict"):
        render_template("index.html", "not a dict")


def test_render_template_requires_string_name():
    """Ensure render_template validates template name is a string."""
    mock_context = {"request": None}
    with pytest.raises(TypeError, match="Template name must be str"):
        render_template({"name": "index.html"}, mock_context)


def test_homepage_loads():
    """Test that homepage loads without template errors."""
    response = client.get("/")
    # Should either redirect to login (401) or load the page
    assert response.status_code in [200, 302]


def test_login_page_loads():
    """Test that login page loads without template errors."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text or "login" in response.text.lower()


def test_register_page_loads():
    """Test that register page loads without template errors."""
    response = client.get("/register")
    assert response.status_code == 200
    assert "Register" in response.text or "register" in response.text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
