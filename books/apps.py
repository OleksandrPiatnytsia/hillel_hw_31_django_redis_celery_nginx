from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BooksConfig(AppConfig):
    name = "books"
    # Section title in the admin
    verbose_name = _("Books")

    def ready(self):
        # Connects the cache invalidation receivers (@receiver runs when
        # the module is imported)
        from . import signals  # noqa: F401
