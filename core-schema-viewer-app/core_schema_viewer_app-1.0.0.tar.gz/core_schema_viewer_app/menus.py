""" Add View Schema in main menu
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

Menu.add_item(
    "main", MenuItem("Schema Viewer", reverse("core_schema_viewer_index"))
)

schema_viewer_children = (
    MenuItem("Templates Visibility", reverse("admin:core_schema_viewer_app_template"), icon="list"),
)

Menu.add_item(
    "admin", MenuItem("SCHEMA VIEWER", None, children=schema_viewer_children)
)
