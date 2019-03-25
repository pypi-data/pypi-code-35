from ._xml_attributes import XmlAttributes
from .engine import LeafNodeMixin
from .xml import XmlElement


class HtmlAttributes(XmlAttributes):
    attribute_name_substitutes = {
        "http_equiv": "http-equiv",
        'klass': 'class',
        'Class': 'class',
        'class_': 'class',
    }


class HtmlNodeBase(XmlElement):
    _attribute_processor = HtmlAttributes


class HtmlLeafNode(LeafNodeMixin, HtmlNodeBase):

    def string_items(self, tree_level):
        yield "<{}{} />".format(self.tag_name, self.attributes)


@HtmlNodeBase.make_attrs_float
class HtmlCommon(HtmlNodeBase):
    """ Set of tags that are common for HTML version 4 and 5."""

    @staticmethod
    def _replicant_leaf_type():
        return HtmlLeafNode

    @classmethod
    def _root_head_items(cls):
        yield '<!DOCTYPE html>\n'

    def html(self, *args, **kwargs):
        """Defines an HTML document"""
        return self.node("html", *args, **kwargs)

    def head(self, *args, **kwargs):
        """Defines information about the document"""
        return self.node("head", *args, **kwargs)

    def title(self, *args, **kwargs):
        """Defines a title for the document"""
        return self.node("title", *args, **kwargs)

    def body(self, *args, **kwargs):
        """Defines the document's body"""
        return self.node("body", *args, **kwargs)

    def h1(self, *args, **kwargs):
        """Defines HTML heading, rank 1."""
        return self.node("h1", *args, **kwargs)

    def h2(self, *args, **kwargs):
        """Defines HTML heading, rank 2."""
        return self.node("h2", *args, **kwargs)

    def h3(self, *args, **kwargs):
        """Defines HTML heading, rank 3."""
        return self.node("h3", *args, **kwargs)

    def h4(self, *args, **kwargs):
        """Defines HTML heading, rank 4."""
        return self.node("h4", *args, **kwargs)

    def h5(self, *args, **kwargs):
        """Defines HTML heading, rank 5."""
        return self.node("h5", *args, **kwargs)

    def h6(self, *args, **kwargs):
        """Defines HTML heading, rank 6."""
        return self.node("h6", *args, **kwargs)

    def p(self, *args, **kwargs):
        """Defines a paragraph"""
        return self.node("p", *args, **kwargs)

    def br(self, *args, **kwargs):
        """Inserts a single line break"""
        return self.leaf("br", *args, **kwargs)

    def hr(self, *args, **kwargs):
        """Defines a thematic change in the content"""
        return self.leaf("hr", *args, **kwargs)

    def abbr(self, *args, **kwargs):
        """Defines an abbreviation or an acronym"""
        return self.node("abbr", *args, **kwargs)

    def address(self, *args, **kwargs):
        """Defines contact information for the author/owner of a document/article"""
        return self.node("address", *args, **kwargs)

    def b(self, *args, **kwargs):
        """Defines bold text"""
        return self.node("b", *args, **kwargs)

    def bdo(self, *args, **kwargs):
        """Overrides the current text direction"""
        return self.node("bdo", *args, **kwargs)

    def blockquote(self, *args, **kwargs):
        """Defines a section that is quoted from another source"""
        return self.node("blockquote", *args, **kwargs)

    def cite(self, *args, **kwargs):
        """Defines the title of a work"""
        return self.node("cite", *args, **kwargs)

    def code(self, *args, **kwargs):
        """Defines a piece of computer code"""
        return self.node("code", *args, **kwargs)

    def del_(self, *args, **kwargs):
        """Defines text that has been deleted from a document"""
        return self.node("del_", *args, **kwargs)

    def dfn(self, *args, **kwargs):
        """Represents the defining instance of a term"""
        return self.node("dfn", *args, **kwargs)

    def em(self, *args, **kwargs):
        """Defines emphasized text """
        return self.node("em", *args, **kwargs)

    def i(self, *args, **kwargs):
        """Defines a part of text in an alternate voice or mood"""
        return self.node("i", *args, **kwargs)

    def ins(self, *args, **kwargs):
        """Defines a text that has been inserted into a document"""
        return self.node("ins", *args, **kwargs)

    def kbd(self, *args, **kwargs):
        """Defines keyboard input"""
        return self.node("kbd", *args, **kwargs)

    def meter(self, *args, **kwargs):
        """Defines a scalar measurement within a known range (a gauge)"""
        return self.node("meter", *args, **kwargs)

    def pre(self, *args, **kwargs):
        """Defines preformatted text"""
        return self.node("pre", *args, **kwargs)

    def q(self, *args, **kwargs):
        """Defines a short quotation"""
        return self.node("q", *args, **kwargs)

    def s(self, *args, **kwargs):
        """Defines text that is no longer correct"""
        return self.node("s", *args, **kwargs)

    def samp(self, *args, **kwargs):
        """Defines sample output from a computer program"""
        return self.node("samp", *args, **kwargs)

    def small(self, *args, **kwargs):
        """Defines smaller text"""
        return self.node("small", *args, **kwargs)

    def strong(self, *args, **kwargs):
        """Defines important text"""
        return self.node("strong", *args, **kwargs)

    def sub(self, *args, **kwargs):
        """Defines subscripted text"""
        return self.node("sub", *args, **kwargs)

    def sup(self, *args, **kwargs):
        """Defines superscripted text"""
        return self.node("sup", *args, **kwargs)

    def u(self, *args, **kwargs):
        """Defines text that should be stylistically different from normal text"""
        return self.node("u", *args, **kwargs)

    def var(self, *args, **kwargs):
        """Defines a variable"""
        return self.node("var", *args, **kwargs)

    def form(self, *args, **kwargs):
        """Defines an HTML form for user input"""
        return self.node("form", *args, **kwargs)

    def input(self, *args, **kwargs):
        """Defines an input control"""
        return self.leaf("input", *args, **kwargs)

    def textarea(self, *args, **kwargs):
        """Defines a multiline input control (text area)"""
        return self.node("textarea", *args, **kwargs)

    def button(self, *args, **kwargs):
        """Defines a clickable button"""
        return self.node("button", *args, **kwargs)

    def select(self, *args, **kwargs):
        """Defines a drop-down list"""
        return self.node("select", *args, **kwargs)

    def optgroup(self, *args, **kwargs):
        """Defines a group of related options in a drop-down list"""
        return self.node("optgroup", *args, **kwargs)

    def option(self, *args, **kwargs):
        """Defines an option in a drop-down list"""
        return self.node("option", *args, **kwargs)

    def label(self, *args, **kwargs):
        """Defines a label for an <input> element"""
        return self.node("label", *args, **kwargs)

    def fieldset(self, *args, **kwargs):
        """Groups related elements in a form"""
        return self.node("fieldset", *args, **kwargs)

    def legend(self, *args, **kwargs):
        """Defines a caption for a <fieldset> element"""
        return self.node("legend", *args, **kwargs)

    def iframe(self, *args, **kwargs):
        """Defines an inline frame"""
        return self.node("iframe", *args, **kwargs)

    def img(self, *args, **kwargs):
        """Defines an image"""
        return self.leaf("img", *args, **kwargs)

    def map(self, *args, **kwargs):
        """Defines a client-side image-map"""
        return self.node("map", *args, **kwargs)

    def area(self, *args, **kwargs):
        """Defines an area inside an image-map"""
        return self.leaf("area", *args, **kwargs)

    def a(self, *args, **kwargs):
        """Defines a hyperlink"""
        return self.node("a", *args, **kwargs)

    def link(self, *args, **kwargs):
        """Defines the relationship between a document and an external resource (most used to link to style sheets)"""
        return self.leaf("link", *args, **kwargs)

    def ul(self, *args, **kwargs):
        """Defines an unordered list"""
        return self.node("ul", *args, **kwargs)

    def ol(self, *args, **kwargs):
        """Defines an ordered list"""
        return self.node("ol", *args, **kwargs)

    def li(self, *args, **kwargs):
        """Defines a list item"""
        return self.node("li", *args, **kwargs)

    def dl(self, *args, **kwargs):
        """Defines a description list"""
        return self.node("dl", *args, **kwargs)

    def dt(self, *args, **kwargs):
        """Defines a term/name in a description list"""
        return self.node("dt", *args, **kwargs)

    def dd(self, *args, **kwargs):
        """Defines a description of a term/name in a description list"""
        return self.node("dd", *args, **kwargs)

    def menu(self, *args, **kwargs):
        """Defines a list/menu of commands"""
        return self.node("menu", *args, **kwargs)

    def table(self, *args, **kwargs):
        """Defines a table"""
        return self.node("table", *args, **kwargs)

    def caption(self, *args, **kwargs):
        """Defines a table caption"""
        return self.node("caption", *args, **kwargs)

    def th(self, *args, **kwargs):
        """Defines a header cell in a table"""
        return self.node("th", *args, **kwargs)

    def tr(self, *args, **kwargs):
        """Defines a row in a table"""
        return self.node("tr", *args, **kwargs)

    def td(self, *args, **kwargs):
        """Defines a cell in a table"""
        return self.node("td", *args, **kwargs)

    def thead(self, *args, **kwargs):
        """Groups the header content in a table"""
        return self.node("thead", *args, **kwargs)

    def tbody(self, *args, **kwargs):
        """Groups the body content in a table"""
        return self.node("tbody", *args, **kwargs)

    def tfoot(self, *args, **kwargs):
        """Groups the footer content in a table"""
        return self.node("tfoot", *args, **kwargs)

    def col(self, *args, **kwargs):
        """Specifies column properties for each column within a <colgroup> element"""
        return self.leaf("col", *args, **kwargs)

    def colgroup(self, *args, **kwargs):
        """Specifies a group of one or more columns in a table for formatting"""
        return self.node("colgroup", *args, **kwargs)

    def style(self, *args, **kwargs):
        """Defines style information for a document"""
        return self.node("style", *args, **kwargs)

    def div(self, *args, **kwargs):
        """Defines a section in a document"""
        return self.node("div", *args, **kwargs)

    def span(self, *args, **kwargs):
        """Defines a section in a document"""
        return self.node("span", *args, **kwargs)

    def meta(self, *args, **kwargs):
        """Defines metadata about an HTML document"""
        return self.leaf("meta", *args, **kwargs)

    def base(self, *args, **kwargs):
        """Specifies the base URL/target for all relative URLs in a document"""
        return self.leaf("base", *args, **kwargs)

    def script(self, *args, **kwargs):
        """Defines a client-side script"""
        return self.node("script", *args, **kwargs)

    def noscript(self, *args, **kwargs):
        """Defines an alternate content for users that do not support client-side scripts"""
        return self.node("noscript", *args, **kwargs)

    def object(self, *args, **kwargs):
        """Defines an embedded object"""
        return self.node("object", *args, **kwargs)

    def param(self, *args, **kwargs):
        """Defines a parameter for an object"""
        return self.leaf("param", *args, **kwargs)


@HtmlNodeBase.make_attrs_float
class Html4Node(HtmlCommon):

    def acronym(self, *args, **kwargs):
        """Not supported in HTML5.
        Use <abbr> instead. Defines an acronym."""
        return self.node("acronym", *args, **kwargs)

    def big(self, *args, **kwargs):
        """Not supported in HTML5.
        Use CSS instead. Defines big text"""
        return self.node("big", *args, **kwargs)

    def center(self, *args, **kwargs):
        """Not supported in HTML5.
        Use CSS instead. Defines centered text."""
        return self.node("center", *args, **kwargs)

    def font(self, *args, **kwargs):
        """Not supported in HTML5.
        Use CSS instead. Defines font, color, and size for text."""
        return self.node("font", *args, **kwargs)

    def strike(self, *args, **kwargs):
        """Not supported in HTML5.
        Use <del> or <s> instead. Defines strikethrough text"""
        return self.node("strike", *args, **kwargs)

    def tt(self, *args, **kwargs):
        """Not supported in HTML5.
        Use CSS instead. Defines teletype text."""
        return self.node("tt", *args, **kwargs)

    def frame(self, *args, **kwargs):
        """Not supported in HTML5.
        Defines a window (a frame) in a frameset"""
        return self.node("frame", *args, **kwargs)

    def frameset(self, *args, **kwargs):
        """Not supported in HTML5.
        Defines a set of frames"""
        return self.node("frameset", *args, **kwargs)

    def noframes(self, *args, **kwargs):
        """Not supported in HTML5.

        Defines an alternate content for users that do not support frames"""
        return self.node("noframes", *args, **kwargs)

    def dir(self, *args, **kwargs):
        """Not supported in HTML5.
        Use <ul> instead.
        Defines a directory list"""
        return self.node("dir", *args, **kwargs)

    def basefont(self, *args, **kwargs):
        """Not supported in HTML5.
        Use CSS instead.
        Specifies a default color, size, and font for all text in a document"""
        return self.node("basefont", *args, **kwargs)

    def applet(self, *args, **kwargs):
        """Not supported in HTML5.
        Use <embed> or <object> instead. Defines an embedded applet"""
        return self.node("applet", *args, **kwargs)


@HtmlNodeBase.make_attrs_float
class Html5Node(HtmlCommon):

    def bdi(self, *args, **kwargs):
        """Isolates a part of text that might be formatted in a different direction from other text outside it"""
        return self.node("bdi", *args, **kwargs)

    def mark(self, *args, **kwargs):
        """Defines marked/highlighted text"""
        return self.node("mark", *args, **kwargs)

    def progress(self, *args, **kwargs):
        """Represents the progress of a task"""
        return self.node("progress", *args, **kwargs)

    def rp(self, *args, **kwargs):
        """Defines what to show in browsers that do not support ruby annotations"""
        return self.node("rp", *args, **kwargs)

    def rt(self, *args, **kwargs):
        """Defines an explanation/pronunciation of characters (for East Asian typography)"""
        return self.node("rt", *args, **kwargs)

    def ruby(self, *args, **kwargs):
        """Defines a ruby annotation (for East Asian typography)"""
        return self.node("ruby", *args, **kwargs)

    def time(self, *args, **kwargs):
        """Defines a date/time"""
        return self.node("time", *args, **kwargs)

    def wbr(self, *args, **kwargs):
        """Defines a possible line-break"""
        return self.leaf("wbr", *args, **kwargs)

    def datalist(self, *args, **kwargs):
        """Specifies a list of pre-defined options for input controls"""
        return self.node("datalist", *args, **kwargs)

    def keygen(self, *args, **kwargs):
        """Defines a key-pair generator field (for forms)"""
        return self.leaf("keygen", *args, **kwargs)

    def output(self, *args, **kwargs):
        """Defines the result of a calculation"""
        return self.node("output", *args, **kwargs)

    def canvas(self, *args, **kwargs):
        """Used to draw graphics, on the fly, via scripting (usually JavaScript)"""
        return self.node("canvas", *args, **kwargs)

    def figcaption(self, *args, **kwargs):
        """Defines a caption for a <figure> element"""
        return self.node("figcaption", *args, **kwargs)

    def figure(self, *args, **kwargs):
        """Specifies self-contained content"""
        return self.node("figure", *args, **kwargs)

    def picture(self, *args, **kwargs):
        """Defines a container for multiple image resources"""
        return self.node("picture", *args, **kwargs)

    def audio(self, *args, **kwargs):
        """Defines sound content"""
        return self.node("audio", *args, **kwargs)

    def source(self, *args, **kwargs):
        """Defines multiple media resources for media elements (<video>, <audio> and <picture>"""
        return self.leaf("source", *args, **kwargs)

    def track(self, *args, **kwargs):
        """Defines text tracks for media elements (<video> and <audio>"""
        return self.leaf("track", *args, **kwargs)

    def video(self, *args, **kwargs):
        """Defines a video or movie"""
        return self.node("video", *args, **kwargs)

    def nav(self, *args, **kwargs):
        """Defines navigation links"""
        return self.node("nav", *args, **kwargs)

    def menuitem(self, *args, **kwargs):
        """Defines a command/menu item that the user can invoke from a popup menu"""
        return self.node("menuitem", *args, **kwargs)

    def header(self, *args, **kwargs):
        """Defines a header for a document or section"""
        return self.node("header", *args, **kwargs)

    def footer(self, *args, **kwargs):
        """Defines a footer for a document or section"""
        return self.node("footer", *args, **kwargs)

    def main(self, *args, **kwargs):
        """Specifies the main content of a document"""
        return self.node("main", *args, **kwargs)

    def section(self, *args, **kwargs):
        """Defines a section in a document"""
        return self.node("section", *args, **kwargs)

    def article(self, *args, **kwargs):
        """Defines an article"""
        return self.node("article", *args, **kwargs)

    def aside(self, *args, **kwargs):
        """Defines content aside from the page content"""
        return self.node("aside", *args, **kwargs)

    def details(self, *args, **kwargs):
        """Defines additional details that the user can view or hide"""
        return self.node("details", *args, **kwargs)

    def dialog(self, *args, **kwargs):
        """Defines a dialog box or window"""
        return self.node("dialog", *args, **kwargs)

    def summary(self, *args, **kwargs):
        """Defines a visible heading for a <details> element"""
        return self.node("summary", *args, **kwargs)

    def data(self, *args, **kwargs):
        """Links the given content with a machine-readable translation"""
        return self.node("data", *args, **kwargs)

    def embed(self, *args, **kwargs):
        """Defines a container for an external (non-HTML) application"""
        return self.leaf("embed", *args, **kwargs)


def html4_plant():
    return Html4Node(None, None)


def html5_plant():
    return Html5Node(None, None)
