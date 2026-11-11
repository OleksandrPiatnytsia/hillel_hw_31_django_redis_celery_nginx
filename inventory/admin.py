from django.contrib import admin

from .models import Stock, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_default"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """All stock rows: the quick way to change many quantities at once.

    list_editable here instead of the old "stock" column of the book list:
    the quantity is a field of Stock now, not of Book.
    """

    list_display = ["book", "warehouse", "quantity"]
    list_editable = ["quantity"]
    list_filter = ["warehouse"]
    search_fields = ["book__title", "book__author__name"]
    # Search-as-you-type for the book (BookAdmin has search_fields)
    autocomplete_fields = ["book"]
    # book + author for str(book), warehouse: JOINs instead of queries per row
    list_select_related = ["book__author", "warehouse"]
