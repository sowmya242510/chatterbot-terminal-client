"""
Django settings for the chatterbot_terminal project.

This project exists to host a single management command (chatapp/management/
commands/chat.py) that runs an interactive, terminal-based chat session with
a ChatterBot instance. Django is used here mainly to satisfy the assignment
requirement of integrating ChatterBot with Django (ChatterBot ships with a
Django storage adapter), even though there is no web front end.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# For a class assignment this can stay as-is; for anything real, load this
# from an environment variable instead.
SECRET_KEY = "django-insecure-change-this-key-for-any-real-deployment"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    # Our app, which contains the "chat" management command
    "chatapp",
    # ChatterBot's Django storage adapter needs this app registered so its
    # models (Statement, Conversation, etc.) are created by migrate.
    "chatterbot.ext.django_chatterbot",
]

MIDDLEWARE = []

ROOT_URLCONF = "chatterbot_terminal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "chatterbot_terminal.wsgi.application"

# Database
# ChatterBot will store learned conversation data in this same SQLite
# database via its Django storage adapter.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# ChatterBot configuration
# ---------------------------------------------------------------------------
# Tells ChatterBot to persist learned statements/conversations using Django's
# ORM (into the same SQLite database configured above) instead of the default
# SQLStorageAdapter.
CHATTERBOT = {
    "name": "TerminalBot",
    "storage_adapter": "chatterbot.storage.DjangoStorageAdapter",
    "logic_adapters": [
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.MathematicalEvaluation",
    ],
    "read_only": False,
}
