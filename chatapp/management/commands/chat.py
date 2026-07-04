"""
Terminal chat client powered by ChatterBot.

Run with:
    python manage.py chat

This management command:
 1. Creates (or connects to) a ChatBot using the CHATTERBOT settings defined
    in chatterbot_terminal/settings.py (Django storage adapter -> SQLite).
 2. Trains the bot on a small starter corpus the first time it runs, so it
    has something to talk about immediately.
 3. Opens a simple read -> respond -> print loop in the terminal until the
    user types "quit", "exit", or "bye".
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

# Words that end the chat session when typed by the user.
EXIT_COMMANDS = {"quit", "exit", "bye", "goodbye"}


class Command(BaseCommand):
    help = "Start an interactive terminal chat session with the ChatterBot."

    def add_arguments(self, parser):
        # Optional flag to skip retraining on every run once the bot already
        # has data, which speeds up repeated testing.
        parser.add_argument(
            "--no-train",
            action="store_true",
            help="Skip corpus training and just start chatting.",
        )

    def handle(self, *args, **options):
        # Build the bot using the settings from settings.py so storage,
        # logic adapters, etc. stay in one place.
        chatbot = ChatBot(**django_settings.CHATTERBOT)

        if not options["no_train"]:
            self._train_bot(chatbot)

        self.stdout.write(self.style.SUCCESS(
            "TerminalBot is ready! Type 'quit' to end the conversation.\n"
        ))

        self._run_chat_loop(chatbot)

    def _train_bot(self, chatbot):
        """Train the bot on the general English corpus plus a few custom
        example exchanges so responses feel a bit more personal."""
        self.stdout.write("Training bot on the English corpus (first run may take a while)...")

        corpus_trainer = ChatterBotCorpusTrainer(chatbot)
        corpus_trainer.train("chatterbot.corpus.english")

        # A short custom conversation, trained with the ListTrainer, so the
        # bot has some deterministic exchanges to fall back on too.
        list_trainer = ListTrainer(chatbot)
        list_trainer.train([
            "Good morning! How are you doing?",
            "I am doing very well, thank you for asking.",
            "You're welcome.",
            "Do you like hats?",
        ])

        self.stdout.write(self.style.SUCCESS("Training complete.\n"))

    def _run_chat_loop(self, chatbot):
        """Read a line from the user, get the bot's response, print it, and
        repeat until the user asks to exit."""
        while True:
            try:
                user_input = input("user: ").strip()
            except (EOFError, KeyboardInterrupt):
                # Handle Ctrl+D / Ctrl+C gracefully instead of a stack trace.
                self.stdout.write("\nbot: Goodbye!")
                break

            if not user_input:
                # Ignore empty input rather than sending it to the bot.
                continue

            if user_input.lower() in EXIT_COMMANDS:
                self.stdout.write("bot: Goodbye!")
                break

            response = chatbot.get_response(user_input)
            self.stdout.write(f"bot: {response}")
