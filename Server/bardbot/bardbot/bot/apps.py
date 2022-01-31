from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bardbot.bot"
    verbose_name = _("Bot")

    def ready(self):
        try:
            import bardbot.bot.signals  # noqa F401
        except ImportError:
            pass
