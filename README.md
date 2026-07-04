# ChatterBot Terminal Client (Django + ChatterBot)

A terminal-based chat client built with **Django** and **ChatterBot**. The bot
learns from a built-in English corpus and a short custom conversation, then
chats with you interactively in the terminal.

```
user: Good morning! How are you doing?
bot: I am doing very well, thank you for asking.
user: You're welcome.
bot: Do you like hats?
```

## Project layout

```
chatterbot_terminal/
├── manage.py
├── requirements.txt
├── chatterbot_terminal/        # Django project (settings, urls, wsgi)
│   ├── settings.py             # CHATTERBOT config lives here
│   ├── urls.py
│   └── wsgi.py
└── chatapp/                    # Django app
    └── management/
        └── commands/
            └── chat.py         # <-- the actual terminal chat loop
```

## ⚠️ Important: Python version compatibility

ChatterBot (last released in 2020) depends on older versions of spaCy,
SQLAlchemy, and PyYAML. **It will fail to install on Python 3.9+** (spaCy's
`blis`/`preshed` C-extensions won't build) with errors like:

```
error: command '/usr/bin/x86_64-linux-gnu-gcc' failed with exit code 1
Failed to build preshed thinc blis
```

**Use Python 3.7 or 3.8 in a dedicated virtual environment.** This is the
single most common source of setup pain with this assignment, so don't skip
it.

## Setup

```bash
# 1. Make sure you have Python 3.8 available. If not, install it via
#    pyenv, deadsnakes PPA (Linux), or python.org (Windows/Mac).
python3.8 -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply Django migrations (creates db.sqlite3, including ChatterBot's
#    tables since chatterbot.ext.django_chatterbot is in INSTALLED_APPS)
python manage.py migrate

# 4. Run the terminal chat client
python manage.py chat
```

The first run will take a little while because it downloads/trains on the
English corpus. Subsequent runs are faster; pass `--no-train` to skip
retraining once you're happy with the bot's responses:

```bash
python manage.py chat --no-train
```

Type `quit`, `exit`, or `bye` to end the session.

## How it works

- **`chatterbot_terminal/settings.py`** registers `chatterbot.ext.django_chatterbot`
  as an installed app and configures a `CHATTERBOT` dict that tells ChatterBot
  to use Django's ORM (`DjangoStorageAdapter`) to persist learned statements
  in the same SQLite database Django already uses.
- **`chatapp/management/commands/chat.py`** is a Django management command
  (`python manage.py chat`). It builds a `ChatBot` instance, trains it (corpus
  + a short custom list), then runs a simple `input()`/`print()` loop that
  sends each line the user types to `chatbot.get_response()` and prints the
  reply.

## Pushing to GitHub

```bash
cd chatterbot_terminal
git init
git add .
git commit -m "Terminal chat client with Django + ChatterBot"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Add a `.gitignore` (venv/, `__pycache__/`, `db.sqlite3`) before committing if
you don't want the virtual environment or local database checked in.

## Deliverables checklist

- [x] Python source code (this repository)
- [x] Manifest file (`requirements.txt`)
- [ ] Screenshot of a terminal conversation with the bot — take this after
      running `python manage.py chat` locally, then paste it into your Word
      document
- [ ] GitHub repository URL — paste into your Word document after pushing
