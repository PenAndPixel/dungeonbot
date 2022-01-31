from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bardbot.char"
    verbose_name = _("Characters")

    def ready(self):
        try:
            import bardbot.char.signals  # noqa F401
        except ImportError:
            pass
