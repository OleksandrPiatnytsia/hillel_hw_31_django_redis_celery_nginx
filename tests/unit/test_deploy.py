"""Settings for running behind nginx with DEBUG=False (hw_31, stage 4)."""

from django.test import RequestFactory
from django.views.defaults import server_error
from rest_framework.request import Request
from rest_framework.throttling import AnonRateThrottle


# Generated with AI
def test_anonymous_api_limit_ignores_a_made_up_x_forwarded_for():
    """The limit of anonymous clients is counted per REMOTE_ADDR.

    A client that sends its own X-Forwarded-For (a new fake address with
    every request) must still be the same client for the throttle.
    """
    http_request = RequestFactory().get(
        "/api/books/", REMOTE_ADDR="203.0.113.7", HTTP_X_FORWARDED_FOR="10.9.8.7"
    )

    ident = AnonRateThrottle().get_ident(Request(http_request))

    assert ident == "203.0.113.7"


# Generated with AI
def test_500_page_renders_without_the_request_context():
    """server_error renders templates/500.html with no context processors:
    the page must not depend on the user, the cart or the database."""
    response = server_error(RequestFactory().get("/"))

    assert response.status_code == 500
    html = response.content.decode()
    assert "<!DOCTYPE html>" in html
    assert 'href="/"' in html
