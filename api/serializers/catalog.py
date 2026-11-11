"""Serializers of the catalog: Python objects <-> JSON, plus validation.

A serializer works in two directions:
    reading   Book object  -> serializer.data (dict)  -> JSON answer
    writing   JSON request -> serializer.is_valid()   -> serializer.save()

Nested serializers: a book shows its author and categories as objects,
not only as numbers, so a client builds a catalog page from one request:

    {"id": 7, "title": "Kobzar",
     "author": {"id": 3, "name": "Taras Shevchenko"},
     "categories": [{"id": 1, "name": "Poetry", "slug": "poetry"}], ...}

For writing the client sends only the ids: "author_id": 3,
"category_ids": [1, 2]. Writable nested objects ("create the author
together with the book") would need our own create()/update(); authors
and categories have their own endpoints for that.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from books.models import Author, Book, Category
from inventory.services import set_stock


class BooksCountMixin(serializers.Serializer):
    """books_count: the number of books of an author / a category.

    Lists and single objects come from the queryset of the ViewSet with
    .annotate(books_count=Count("books")): one query for the whole page
    instead of a COUNT for every row. An object made by POST is not from
    that queryset and has no such attribute: then one COUNT for it.
    """

    books_count = serializers.SerializerMethodField()

    def get_books_count(self, obj) -> int:
        if hasattr(obj, "books_count"):
            return obj.books_count
        return obj.books.count()


class CategorySerializer(BooksCountMixin, serializers.ModelSerializer):
    """/api/categories/: a category with the number of its books."""

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "books_count"]


class AuthorSerializer(BooksCountMixin, serializers.ModelSerializer):
    """/api/authors/: an author with the number of their books."""

    class Meta:
        model = Author
        fields = ["id", "name", "bio", "books_count"]


class AuthorShortSerializer(serializers.ModelSerializer):
    """The author inside a book: only what a list of books needs."""

    class Meta:
        model = Author
        fields = ["id", "name"]


class CategoryShortSerializer(serializers.ModelSerializer):
    """A category inside a book."""

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BookSerializer(serializers.ModelSerializer):
    """/api/books/: read with nested author and categories, write with ids.

    Writing the stock is allowed only with the permission
    inventory.change_stock (group "Managers"), like in BookForm on the
    site: an editor may create and edit books, the stock stays as it is.

    "stock" is not a field of Book (inventory.Stock, the default
    warehouse): declared here, read from book.stock (the with_stock()
    annotation of the ViewSet), written in create() / update().
    """

    # Reading: nested objects (read_only: they are never parsed from a request)
    author = AuthorShortSerializer(read_only=True)
    categories = CategoryShortSerializer(many=True, read_only=True)

    # Writing: ids. source= points to the model field; the serializer finds
    # the objects itself and answers 400 for an unknown id:
    #   {"author_id": ["Invalid pk \"999\" - object does not exist."]}
    author_id = serializers.PrimaryKeyRelatedField(
        source="author", queryset=Author.objects.all(), write_only=True
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        source="categories",
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    # Absolute URL of the uploaded cover, null without one. Read only:
    # covers are uploaded on the site (BookForm checks size and type)
    cover = serializers.SerializerMethodField()
    # max_value: the largest PositiveIntegerField value in PostgreSQL
    stock = serializers.IntegerField(min_value=0, max_value=2147483647, required=False)
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "author_id",
            "categories",
            "category_ids",
            "price",
            "description",
            "stock",
            "in_stock",
            "cover",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_cover(self, book) -> str | None:
        # The "-> str | None" hint: drf-spectacular takes the type for the
        # documentation from it (a method field has no model field behind it)
        if not book.cover:
            return None
        request = self.context.get("request")
        url = book.cover.url
        # http://host/media/covers/...: an API client is not on our site and
        # can't resolve "/media/..." by itself
        return request.build_absolute_uri(url) if request else url

    def get_in_stock(self, book) -> bool:
        return book.stock > 0

    def validate_stock(self, value):
        """Only users with inventory.change_stock may CHANGE the stock.

        Sending the current value is allowed: a client that edits a book
        with PUT sends back every field it has read, the stock too.
        New book: the current value is 0 (its new Stock row).
        """
        request = self.context.get("request")
        if request is None or request.user.has_perm("inventory.change_stock"):
            return value
        current = self.instance.stock if self.instance else 0
        if value != current:
            # 403, not 400: the value is fine, the user is not allowed
            raise PermissionDenied(
                _("Only users with the “manage stock” permission can change it.")
            )
        return value

    def create(self, validated_data):
        # Book(**validated_data) would only put the number into the object:
        # take it out and write it to the default warehouse after the book
        stock = validated_data.pop("stock", None)
        book = super().create(validated_data)
        if stock:  # None or 0: the row made by inventory.signals already has 0
            set_stock(book, stock)
        return book

    def update(self, instance, validated_data):
        stock = validated_data.pop("stock", None)
        book = super().update(instance, validated_data)
        # Only a value different from the current one is written: PUT sends
        # back every field it read, and an unchanged stock needs no UPDATE.
        # Like any PUT without a version check (ETag / If-Match), a stock
        # changed by an order between the client's GET and its PUT can
        # still be overwritten by the old number.
        if stock is not None and stock != book.stock:
            set_stock(book, stock)
        return book
