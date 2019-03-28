# Copyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>

from pathlib import Path

from . import slides, tables


__version__ = "0.3.0"  # sig: str


_template_path = Path(Path(__file__).parent, "templates")


def get_path():
    """Get the base path for templates."""
    return str(_template_path)


def setup(app):
    """Register this extension with Sphinx."""
    tables.setup(app)
    slides.setup(app)
    app.add_html_theme("kirlent_revealjs", str(Path(_template_path, "kirlent_revealjs")))
    app.add_html_theme("kirlent_impressjs", str(Path(_template_path, "kirlent_impressjs")))
    return {"version": __version__}
