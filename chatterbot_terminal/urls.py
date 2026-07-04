"""
URL configuration for chatterbot_terminal project.

This project doesn't expose a web chat UI -- interaction happens through the
`chat` management command in a terminal -- so there are no real routes to
define. The file is kept minimal so Django's setup stays valid.
"""
from django.urls import path

urlpatterns = [
    # No views are needed for a terminal-only client.
]
