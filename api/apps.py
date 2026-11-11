from django.apps import AppConfig


class ApiConfig(AppConfig):
    """The REST API layer over the existing apps (books, orders).

    No models of its own: serializers, ViewSets and permissions work with
    the models of books / orders and reuse their services
    (orders.services.create_order, ...), so the site and the API follow
    the same rules.
    """

    name = "api"
    verbose_name = "REST API"

    def ready(self):
        # Invalidation of the cached /api/authors/ and /api/categories/
        from . import signals  # noqa: F401
