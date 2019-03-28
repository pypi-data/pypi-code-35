# Copyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>
#
# Derived from the sphinxjp.themes.revealjs project:
#   https://github.com/tell-k/sphinxjp.themes.revealjs
# Read the included LICENSE_sphinxjp.themes.revealjs.txt file for details.

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.roles import set_classes
from sphinx.writers.html5 import HTML5Translator


class Slide(nodes.General, nodes.Element):
    """Node for a slide."""


class SpeakerNotes(nodes.General, nodes.Element):
    """Node for speaker notes on a slide."""


class SlideDirective(Directive):
    """A directive for generating a slide."""

    has_content = True
    required_arguments = 0
    optional_arguments = 100
    final_argument_whitespace = False

    option_spec_base = {
        "id": directives.unchanged,
        "class": directives.class_option,
        "noheading": directives.flag,
        "title-heading": lambda t: directives.choice(t, ("h1", "h2", "h3", "h4", "h5", "h6")),
        "subtitle": directives.unchanged_required,
        "subtitle-heading": directives.unchanged,
    }

    option_spec_revealjs = {
        "data-autoslide": directives.unchanged,
        "data-transition": directives.unchanged,
        "data-transition-speed": directives.unchanged,
        "data-background": directives.unchanged,
        "data-background-repeat": directives.unchanged,
        "data-background-size": directives.unchanged,
        "data-background-transition": directives.unchanged,
        "data-state": directives.unchanged,
        "data-separator": directives.unchanged,
        "data-separator-vertical": directives.unchanged,
        "data-separator-notes": directives.unchanged,
        "data-charset": directives.unchanged,
    }

    option_spec_impressjs = {
        "data-x": directives.unchanged,
        "data-y": directives.unchanged,
        "data-z": directives.unchanged,
        "data-rel-x": directives.unchanged,
        "data-rel-y": directives.unchanged,
        "data-rel-z": directives.unchanged,
        "data-rel-to": directives.unchanged,
        "data-rotate": directives.unchanged,
        "data-rotate-x": directives.unchanged,
        "data-rotate-y": directives.unchanged,
        "data-rotate-z": directives.unchanged,
        "data-scale": directives.unchanged,
        "data-autoplay": directives.unchanged,
        "data-transition-duration": directives.unchanged,
        "data-views": directives.unchanged,
    }

    option_spec = {**option_spec_base, **option_spec_revealjs, **option_spec_impressjs}

    def run(self):
        """Build a slide node from this directive."""
        self.assert_has_content()

        set_classes(self.options)

        text = "\n".join(self.content)
        node = Slide(text, **self.options)
        self.add_name(node)

        self.state.nested_parse(self.content, self.content_offset, node)

        if self.arguments:
            node["title"] = " ".join(self.arguments)

        node["noheading"] = "noheading" in self.options

        return [node]


class SpeakerNotesDirective(Directive):
    """A directive for generating speaker notes."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {"class": directives.class_option}

    def run(self):
        """Build a speaker notes node from this directive."""
        self.assert_has_content()

        set_classes(self.options)

        text = "\n".join(self.content)
        node = SpeakerNotes(text, **self.options)
        self.add_name(node)

        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class KirlentTranslator(HTML5Translator):
    """Base translator to generate Kirlent markup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        theme = self.builder.env.config.html_theme
        self.revealjs = theme == "kirlent_revealjs"
        self.impressjs = theme == "kirlent_impressjs"

        if self.impressjs:
            self.dx, self.dy, self.dz = 0, 0, 0
            self.next_dx, self.next_dy, self.next_dz = 0, 0, 0
            self.views = []

    def visit_container(self, node):
        """Build start tag for a container node.

        Note that this leaves out the container class normally added by docutils.
        """
        classes = node.attributes["classes"]

        if self.revealjs and ("substep" in classes) and ("fragment" not in classes):
            classes.append("fragment")
        if self.impressjs and ("fragment" in classes) and ("substep" not in classes):
            classes.append("substep")

        self.body.append(self.starttag(node, "div", CLASS="docutils"))


VIEW_TEMPLATE = "".join(
    [
        '<section class="slide step view"',
        ' data-rel-x="%s" data-rel-y="%s" data-rel-z="%s" data-scale="%s">\n',
        "</section>\n",
    ]
)


def visit_slide(self, node):
    """Build start tag for a slide node."""
    section_attrs = {}

    if node.get("id"):
        section_attrs.update({"ids": [node.get("id")]})

    data_attrs = [a for a in SlideDirective.option_spec if a.startswith("data-")]
    for attr in data_attrs:
        attr_value = node.get(attr)
        if attr_value is not None:
            if (self.revealjs and (attr in SlideDirective.option_spec_revealjs)) or (
                self.impressjs and (attr in SlideDirective.option_spec_impressjs)
            ):
                section_attrs.update({attr: attr_value})

    if self.impressjs:
        data_rel_x = node.get("data-rel-x")
        if data_rel_x is not None:
            self.dx = int(data_rel_x)
        else:
            section_attrs["data-rel-x"] = self.next_dx

        data_rel_y = node.get("data-rel-y")
        if data_rel_y is not None:
            self.dy = int(data_rel_y)
        else:
            section_attrs["data-rel-y"] = self.next_dy

        data_rel_z = node.get("data-rel-z")
        if data_rel_z is not None:
            self.dz = int(data_rel_z)
        else:
            section_attrs["data-rel-z"] = self.next_dz

        self.next_dx, self.next_dy, self.next_dz = self.dx, self.dy, self.dz

    title = node.get("title") if (not node.get("noheading")) else None
    title_tag = node.get("title-heading", "h2")

    subtitle = node.get("subtitle")
    subtitle_tag = node.get("subtitle-heading", "h3")

    template = "<%(tag)s>%(text)s</%(tag)s>\n"
    title_text = (template % {"tag": title_tag, "text": title}) if title else None
    subtitle_text = (template % {"tag": subtitle_tag, "text": subtitle}) if subtitle else None

    classes = node.attributes["classes"]

    if self.impressjs:
        if "slide" not in classes:
            classes.append("slide")
        if "step" not in classes:
            classes.append("step")

        views = section_attrs.pop("data-views", None)
        if views is not None:
            for view_data in views[1:-1].split(") ("):
                dx, dy, dz, scale = map(str.strip, view_data.split(","))
                view = VIEW_TEMPLATE % (dx, dy, dz, scale)
                self.views.append(view)
                self.next_dx -= int(dx)
                self.next_dy -= int(dy)
                self.next_dz -= int(dz)

    self.body.append(self.starttag(node, "section", **section_attrs))

    if title_text:
        self.body.append(title_text)
    if subtitle_text:
        self.body.append(subtitle_text)


def depart_slide(self, node):
    """Build end tag for a slide node."""
    self.body.append("</section>\n")

    if self.impressjs:
        while self.views:
            view = self.views.pop(0)
            self.body.append(view)


def visit_speaker_notes(self, node):
    """Build start tag for a speaker notes node."""
    self.body.append(self.starttag(node, "aside", **{"class": "notes"}))


def depart_speaker_notes(self, node):
    """Build end tag for a speaker notes node."""
    self.body.append("</aside>\n")


def setup(app):
    """Add the directives to a Sphinx application."""
    app.set_translator("html", KirlentTranslator)
    app.add_node(Slide, html=(visit_slide, depart_slide))
    app.add_node(SpeakerNotes, html=(visit_speaker_notes, depart_speaker_notes))
    app.add_directive("slide", SlideDirective)
    app.add_directive("speaker-notes", SpeakerNotesDirective)
