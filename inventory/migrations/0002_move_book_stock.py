"""Data migration: Book.stock (a column of the book) -> inventory.Stock rows.

Doesn't change tables, only data. The tables are made by 0001 (before),
the column books_book.stock is dropped by books 0009 (after).

The same 3 steps as the move of the authors (books 0004 / 0005 / 0006):
new table, copy the data, remove the old column.
"""

from django.db import migrations

# Copies of the values from inventory.models: a migration must keep working
# the same way even if the app code changes later
DEFAULT_WAREHOUSE_NAME = "General"
DEFAULT_WAREHOUSE_SLUG = "general"


def move_stock(apps, schema_editor):
    # Historical models: exactly as they are at THIS migration, so Book
    # still has the stock column here (books 0009 runs after this one)
    Book = apps.get_model("books", "Book")
    Stock = apps.get_model("inventory", "Stock")
    Warehouse = apps.get_model("inventory", "Warehouse")

    warehouse, _ = Warehouse.objects.get_or_create(
        is_default=True,
        defaults={"name": DEFAULT_WAREHOUSE_NAME, "slug": DEFAULT_WAREHOUSE_SLUG},
    )
    # One row per book, the books with 0 too: every book has a row that
    # orders can lock (see inventory.signals). One INSERT for all of them;
    # values_list: only two columns, not whole Book objects.
    Stock.objects.bulk_create(
        Stock(book_id=book_id, warehouse=warehouse, quantity=quantity)
        for book_id, quantity in Book.objects.values_list("pk", "stock")
    )


def move_stock_back(apps, schema_editor):
    """Reverse (python manage.py migrate inventory 0001): numbers back to Book.stock.

    Only the default warehouse: the column held one number per book. Then
    the rows and the warehouse are deleted, so running forward again
    starts from an empty table and doesn't hit the unique constraints.
    """
    Book = apps.get_model("books", "Book")
    Stock = apps.get_model("inventory", "Stock")
    Warehouse = apps.get_model("inventory", "Warehouse")

    quantities = dict(
        Stock.objects.filter(warehouse__is_default=True).values_list("book_id", "quantity")
    )
    books = list(Book.objects.only("pk"))
    for book in books:
        book.stock = quantities.get(book.pk, 0)
    # One UPDATE ... CASE for all books instead of one per book
    Book.objects.bulk_update(books, ["stock"], batch_size=500)

    Stock.objects.all().delete()
    Warehouse.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(move_stock, move_stock_back),
    ]
