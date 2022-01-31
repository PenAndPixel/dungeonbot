from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bardbot.event"
    verbose_name = _("Evemts")

    def ready(self):
        try:
            import bardbot.event.signals  # noqa F401
        except ImportError:
            pass
