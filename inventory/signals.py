from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Book

from .models import Stock, Warehouse


@receiver(post_save, sender=Book)
def create_stock_row(sender, instance, created, raw=False, **kwargs):
    """Every new book gets a row in the default warehouse, quantity 0.

    So the stock of a book is always a row that can be locked and changed
    (orders.services, the admin inline), never "no row = 0".
    raw=True: loaddata of a fixture; the fixture brings its own Stock rows.
    """
    if not created or raw:
        return
    Stock.objects.get_or_create(book=instance, warehouse=Warehouse.objects.get_default())
