from .engine import LeafNodeMixin
from .xml import XmlAttributes, XmlElement


class SvgAttributes(XmlAttributes):
    attribute_name_substitutes = {
        'klass': 'class',
        'Class': 'class',
        'class_': 'class',
        'fill_opacity': 'fill-opacity',
        'stroke_width': 'stroke-width',
        'stroke_dasharray': ' stroke-dasharray',
        "stroke_opacity": "stroke-opacity",
        "stroke_dashoffset": "stroke-dashoffset",
        "stroke_linejoin": "stroke-linejoin",
        "stroke_linecap": "stroke-linecap",
        "stroke_miterlimit": "stroke-miterlimit",
    }


@XmlElement.make_attrs_float
class SvgNode(XmlElement):
    _attribute_processor = SvgAttributes

    def __init__(self, parent_node_, tag_name, *xml_args, **xml_kwargs):
        super(SvgNode, self).__init__(parent_node_, tag_name, *xml_args, **xml_kwargs)

    @staticmethod
    def _replicant_leaf_type():
        return SvgLeaf

    @classmethod
    def _root_head_items(cls):
        yield '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'
        yield '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'

    def a(self, *args, **kwargs):
        return self.node("a", *args, **kwargs)

    def animate(self, *args, **kwargs):
        return self.leaf("animate", *args, **kwargs)

    def animateMotion(self, *args, **kwargs):
        return self.leaf("animateMotion", *args, **kwargs)

    def animateTransform(self, *args, **kwargs):
        return self.leaf("animateTransform", *args, **kwargs)

    def audio(self, *args, **kwargs):
        return self.leaf("audio", *args, **kwargs)

    def canvas(self, *args, **kwargs):
        return self.leaf("canvas", *args, **kwargs)

    def circle(self, *args, **kwargs):
        return self.leaf("circle", *args, **kwargs)

    def clipPath(self, *args, **kwargs):
        return self.node("clipPath", *args, **kwargs)

    def defs(self, *args, **kwargs):
        return self.node("defs", *args, **kwargs)

    def desc(self, *args, **kwargs):
        return self.leaf("desc", *args, **kwargs)

    def discard(self, *args, **kwargs):
        return self.leaf("discard", *args, **kwargs)

    def ellipse(self, *args, **kwargs):
        return self.leaf("ellipse", *args, **kwargs)

    def feBlend(self, *args, **kwargs):
        return self.leaf("feBlend", *args, **kwargs)

    def feColorMatrix(self, *args, **kwargs):
        return self.leaf("feColorMatrix", *args, **kwargs)

    def feComponentTransfer(self, *args, **kwargs):
        return self.leaf("feComponentTransfer", *args, **kwargs)

    def feComposite(self, *args, **kwargs):
        return self.leaf("feComposite", *args, **kwargs)

    def feConvolveMatrix(self, *args, **kwargs):
        return self.leaf("feConvolveMatrix", *args, **kwargs)

    def feDiffuseLighting(self, *args, **kwargs):
        return self.leaf("feDiffuseLighting", *args, **kwargs)

    def feDisplacementMap(self, *args, **kwargs):
        return self.leaf("feDisplacementMap", *args, **kwargs)

    def feDistantLight(self, *args, **kwargs):
        return self.leaf("feDistantLight", *args, **kwargs)

    def feDropShadow(self, *args, **kwargs):
        return self.leaf("feDropShadow", *args, **kwargs)

    def feFlood(self, *args, **kwargs):
        return self.leaf("feFlood", *args, **kwargs)

    def feFuncA(self, *args, **kwargs):
        return self.leaf("feFuncA", *args, **kwargs)

    def feFuncB(self, *args, **kwargs):
        return self.leaf("feFuncB", *args, **kwargs)

    def feFuncG(self, *args, **kwargs):
        return self.leaf("feFuncG", *args, **kwargs)

    def feFuncR(self, *args, **kwargs):
        return self.leaf("feFuncR", *args, **kwargs)

    def feGaussianBlur(self, *args, **kwargs):
        return self.leaf("feGaussianBlur", *args, **kwargs)

    def feImage(self, *args, **kwargs):
        return self.leaf("feImage", *args, **kwargs)

    def feMerge(self, *args, **kwargs):
        return self.leaf("feMerge", *args, **kwargs)

    def feMergeNode(self, *args, **kwargs):
        return self.leaf("feMergeNode", *args, **kwargs)

    def feMorphology(self, *args, **kwargs):
        return self.leaf("feMorphology", *args, **kwargs)

    def feOffset(self, *args, **kwargs):
        return self.leaf("feOffset", *args, **kwargs)

    def fePointLight(self, *args, **kwargs):
        return self.leaf("fePointLight", *args, **kwargs)

    def feSpecularLighting(self, *args, **kwargs):
        return self.leaf("feSpecularLighting", *args, **kwargs)

    def feSpotLight(self, *args, **kwargs):
        return self.leaf("feSpotLight", *args, **kwargs)

    def feTile(self, *args, **kwargs):
        return self.leaf("feTile", *args, **kwargs)

    def feTurbulence(self, *args, **kwargs):
        return self.leaf("feTurbulence", *args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.leaf("filter", *args, **kwargs)

    def foreignObject(self, *args, **kwargs):
        return self.leaf("foreignObject", *args, **kwargs)

    def g(self, *args, **kwargs):
        return self.node("g", *args, **kwargs)

    def iframe(self, *args, **kwargs):
        return self.node("iframe", *args, **kwargs)

    def image(self, *args, **kwargs):
        return self.leaf("image", *args, **kwargs)

    def line(self, *args, **kwargs):
        return self.leaf("line", *args, **kwargs)

    def linearGradient(self, *args, **kwargs):
        return self.leaf("linearGradient", *args, **kwargs)

    def marker(self, *args, **kwargs):
        return self.node("marker", *args, **kwargs)

    def mask(self, *args, **kwargs):
        return self.node("mask", *args, **kwargs)

    def metadata(self, *args, **kwargs):
        return self.leaf("metadata", *args, **kwargs)

    def mpath(self, *args, **kwargs):
        return self.leaf("mpath", *args, **kwargs)

    def path(self, *args, **kwargs):
        return self.node("path", *args, **kwargs)

    def pattern(self, *args, **kwargs):
        return self.node("pattern", *args, **kwargs)

    def polygon(self, *args, **kwargs):
        return self.node("polygon", *args, **kwargs)

    def polyline(self, *args, **kwargs):
        return self.node("polyline", *args, **kwargs)

    def radialGradient(self, *args, **kwargs):
        return self.node("radialGradient", *args, **kwargs)

    def rect(self, *args, **kwargs):
        return self.leaf("rect", *args, **kwargs)

    def script(self, *args, **kwargs):
        return self.node("script", *args, **kwargs)

    def set(self, *args, **kwargs):
        return self.leaf("set", *args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.leaf("stop", *args, **kwargs)

    def style(self, *args, **kwargs):
        return self.leaf("style", *args, **kwargs)

    def svg(self, *args, **kwargs):
        if "xmlns" not in kwargs:
            kwargs["xmlns"] = "http://www.w3.org/2000/svg"
        return self.node("svg", *args, **kwargs)

    def switch(self, *args, **kwargs):
        return self.node("switch", *args, **kwargs)

    def symbol(self, *args, **kwargs):
        return self.node("symbol", *args, **kwargs)

    def text(self, *args, **kwargs):
        return self.node("text", *args, **kwargs)

    def textPath(self, *args, **kwargs):
        return self.leaf("textPath", *args, **kwargs)

    def title(self, *args, **kwargs):
        return self.leaf("title", *args, **kwargs)

    def tspan(self, *args, **kwargs):
        return self.node("tspan", *args, **kwargs)

    def unknown(self, *args, **kwargs):
        return self.node("unknown", *args, **kwargs)

    def use(self, *args, **kwargs):
        return self.leaf("use", *args, **kwargs)

    def video(self, *args, **kwargs):
        return self.leaf("video", *args, **kwargs)

    def view(self, *args, **kwargs):
        return self.leaf("view", *args, **kwargs)


class SvgLeaf(LeafNodeMixin, SvgNode):
    def string_items(self, tree_level):
        yield "<{}{} />".format(self.tag_name, self.attributes)


def svg_plant():
    return SvgNode(None, None)
