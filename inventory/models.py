"""Warehouses and the stock of books in them.

Before hw_31 the stock was a column of the book (Book.stock). Now a book
keeps only the information about the book itself, and the number of copies
lives here:

    Warehouse  "General" (is_default=True)
    Stock      book + warehouse + quantity, one row per book per warehouse

Why: the data of a book (title, price, description) changes rarely and
can be cached for a long time (stage 2), while the stock changes with
every order. In one table every purchase would make the cached book stale.

The site sells from the default warehouse only. book.stock and
Book.objects.with_stock() (books.models) read the quantity of that
warehouse; inventory.services changes it.
"""

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# The warehouse made by the data migration 0002 and by get_default() on an
# empty database (tests)
DEFAULT_WAREHOUSE_NAME = "General"
DEFAULT_WAREHOUSE_SLUG = "general"


class WarehouseQuerySet(models.QuerySet):
    def get_default(self):
        """The warehouse the site sells from (is_default=True).

        get_or_create: on a database without it (made by hand, or emptied
        by a test with transaction=True) it is created again instead of
        every order failing with DoesNotExist.
        """
        warehouse, _ = self.get_or_create(
            is_default=True,
            defaults={"name": DEFAULT_WAREHOUSE_NAME, "slug": DEFAULT_WAREHOUSE_SLUG},
        )
        return warehouse


class Warehouse(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    is_default = models.BooleanField(
        _("default"),
        default=False,
        help_text=_("The site sells books from this warehouse. Only one can be the default."),
    )

    objects = WarehouseQuerySet.as_manager()

    class Meta:
        ordering = ["name"]
        verbose_name = _("warehouse")
        verbose_name_plural = _("warehouses")
        constraints = [
            # Partial unique index: unique only among the rows WHERE
            # is_default = true. Any number of warehouses with False, at most
            # one with True. A second default -> IntegrityError in the
            # database, and a validation error in the admin form.
            models.UniqueConstraint(
                fields=["is_default"],
                condition=Q(is_default=True),
                name="one_default_warehouse",
                violation_error_message=_("Another warehouse is already the default."),
            ),
        ]

    def __str__(self):
        return self.name


class Stock(models.Model):
    """How many copies of a book are in a warehouse."""

    book = models.ForeignKey(
        "books.Book",
        verbose_name=_("book"),
        # CASCADE: the stock of a deleted book means nothing. A book that
        # is in orders can't be deleted anyway (OrderItem.book is PROTECT)
        on_delete=models.CASCADE,
        related_name="stocks",  # book.stocks.all()
    )
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name=_("warehouse"),
        # PROTECT: a warehouse that still has stock rows can't be deleted
        on_delete=models.PROTECT,
        related_name="stocks",
    )
    # PositiveIntegerField: PostgreSQL gets CHECK (quantity >= 0) from
    # Django itself, so an UPDATE that would go below zero fails in the
    # database even if the Python check was skipped
    quantity = models.PositiveIntegerField(_("quantity"), default=0)

    class Meta:
        ordering = ["book__title", "warehouse__name"]
        verbose_name = _("stock")
        verbose_name_plural = _("stock")
        constraints = [
            # One row per book per warehouse: the quantity is never split
            # between two rows that would have to be added up
            models.UniqueConstraint(
                fields=["book", "warehouse"],
                name="unique_book_warehouse",
            ),
        ]

    def __str__(self):
        # book.title, not str(book): str(book) also needs the author
        return f"{self.book.title} — {self.warehouse.name}: {self.quantity}"
