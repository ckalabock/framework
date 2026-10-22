"""WSGI config for the visitor accounting web application."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visitor_project.settings")
application = get_wsgi_application()
