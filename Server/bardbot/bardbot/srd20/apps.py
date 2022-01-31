from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bardbot.srd20"
    verbose_name = _("SRD20")

    def ready(self):
        try:
            import bardbot.srd20.signals  # noqa F401
        except ImportError:
            pass
