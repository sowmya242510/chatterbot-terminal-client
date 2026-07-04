"""
WSGI config for chatterbot_terminal project.
Not actually used for the terminal client, but kept so the project behaves
like a normal Django project (manage.py runserver, migrate, etc. all work).
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatterbot_terminal.settings")

application = get_wsgi_application()
