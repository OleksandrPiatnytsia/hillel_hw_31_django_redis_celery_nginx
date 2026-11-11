"""Data migration: the permission books.manage_stock -> inventory.change_stock.

The stock is not a field of the book any more, so the right to change it
belongs to the Stock model: its own standard permission change_stock
(Django makes add / change / delete / view for every model).

Who gets what:
- every group and user that had books.manage_stock ("Managers"):
  view_warehouse, view_stock, add_stock, change_stock;
- the group "Editors": view_warehouse, view_stock (they see the stock on
  the book page of the admin, read-only, as they saw it before).
Then books.manage_stock is deleted: Django never deletes permissions that
disappeared from Meta.permissions, it would stay in the lists forever.
"""

from django.contrib.auth.management import create_permissions
from django.db import migrations

STOCK_MANAGERS = ["view_warehouse", "view_stock", "add_stock", "change_stock"]
STOCK_VIEWERS = ["view_warehouse", "view_stock"]
VIEWER_GROUPS = ["Editors"]


def create_app_permissions(apps, app_label):
    """Create the permissions of an app now, not at post_migrate.

    post_migrate runs AFTER all migrations, so on a fresh database the
    permissions of the new app don't exist yet at this point (the same
    trick as users 0003). Uses the historical app config.
    """
    app_config = apps.get_app_config(app_label)
    app_config.models_module = True  # create_permissions() skips apps without it
    create_permissions(app_config, apps=apps, verbosity=0)
    app_config.models_module = None


def get_permissions(Permission, app_label, codenames):
    permissions = list(
        Permission.objects.filter(content_type__app_label=app_label, codename__in=codenames)
    )
    # Fail loudly on a typo instead of giving fewer rights
    missing = set(codenames) - {permission.codename for permission in permissions}
    if missing:
        raise RuntimeError(f"Unknown permissions in {app_label}: {sorted(missing)}")
    return permissions


def move_permission(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    User = apps.get_model("users", "User")

    create_app_permissions(apps, "inventory")
    managers = get_permissions(Permission, "inventory", STOCK_MANAGERS)
    viewers = get_permissions(Permission, "inventory", STOCK_VIEWERS)

    old = Permission.objects.filter(
        content_type__app_label="books", codename="manage_stock"
    ).first()
    if old is not None:
        # By the permission, not by the group name: a group made by hand
        # in the admin with this right keeps it too
        for group in Group.objects.filter(permissions=old):
            group.permissions.add(*managers)
        for user in User.objects.filter(user_permissions=old):
            user.user_permissions.add(*managers)
        # Deleting the permission also removes it from every group and user
        old.delete()

    for group in Group.objects.filter(name__in=VIEWER_GROUPS):
        group.permissions.add(*viewers)


def move_permission_back(apps, schema_editor):
    """Reverse: books.manage_stock back to those who have inventory.change_stock."""
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    User = apps.get_model("users", "User")

    # The historical Book here still has Meta.permissions with manage_stock
    # (books 0009, which removes it, is unapplied before this one)
    create_app_permissions(apps, "books")
    (old,) = get_permissions(Permission, "books", ["manage_stock"])
    change_stock = Permission.objects.filter(
        content_type__app_label="inventory", codename="change_stock"
    ).first()
    if change_stock is not None:
        for group in Group.objects.filter(permissions=change_stock):
            group.permissions.add(old)
        for user in User.objects.filter(user_permissions=change_stock):
            user.user_permissions.add(old)

    # The inventory rights given by move_permission(): taken away again
    added = Permission.objects.filter(
        content_type__app_label="inventory", codename__in=STOCK_MANAGERS
    )
    for group in Group.objects.filter(permissions__in=added).distinct():
        group.permissions.remove(*added)
    for user in User.objects.filter(user_permissions__in=added).distinct():
        user.user_permissions.remove(*added)


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0002_move_book_stock"),
        # The groups (Managers, Editors) and books.manage_stock are made there
        ("users", "0003_create_groups"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(move_permission, move_permission_back),
    ]
