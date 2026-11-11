"""Celery tasks of users and sessions."""

import logging

from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger(__name__)  # "users.tasks"


@shared_task
def clear_expired_sessions():
    """Every night: delete expired sessions (python manage.py clearsessions).

    SESSION_ENGINE is cached_db: every session is also a row of the
    django_session table. Django never deletes a row by itself when the
    session expires, so without this the table only grows (a row for every
    visitor who put something into the session, e.g. a guest cart).
    The Redis copies expire by themselves (they have a timeout).
    """
    call_command("clearsessions")
    logger.info("Expired sessions cleared")
