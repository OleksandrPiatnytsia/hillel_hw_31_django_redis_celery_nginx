from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InventoryConfig(AppConfig):
    name = "inventory"
    # Section title in the admin
    verbose_name = _("Inventory")

    def ready(self):
        # Connects the receivers (@receiver runs when the module is imported).
        # Here, not in models.py: signals.py imports books.models, and
        # models of different apps must not import each other at load time.
        from . import signals  # noqa: F401
