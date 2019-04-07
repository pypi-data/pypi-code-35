# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    import Image
    import ImageDraw
from NNstyle.core.base import BaseImage
import math


class LayerImage(BaseImage):
    kind = "PNG"

    def __init__(self, width, depth, height, *args, **kwargs):
        self.img_rate = math.sqrt(2) / 2
        super().__init__(width, depth, height, *args, **kwargs)
        self.layer_color = kwargs.get("layer_color")
        self.line_color = kwargs.get("line_color")

    def image_size(self):
        """
        Caculate Size.
        """
        height = int(self.height + self.img_rate * self.width) + 2
        width = int(self.depth + self.img_rate * self.width) + 2
        return width, height

    def new_image(self, **kwargs):
        mode = "RGBA"
        img = Image.new(mode=mode, size=(self.BGwidth, self.BGheight))
        self._draw = ImageDraw.Draw(img)
        return img

    def main_rect_line_point(self):
        x1, y1, x2, y2 = 1, self.img_rate * self.width + 1, self.depth + 1, self.height + self.img_rate * self.width + 1
        a1 = (x1, y1)
        a2 = (x2, y1)
        a3 = (x2, y2)
        a4 = (x1, y2)
        return a1, a2, a3, a4, a1

    def main_rect_point(self):
        return self.main_rect_line_point()[0], self.main_rect_line_point()[2]

    def head_polygon_line_point(self):
        c = self.img_rate * self.width
        a1 = (1 + c, 1)
        a2 = (1 + self.depth + c, 1)
        a3 = (1 + self.depth, c + 1)
        a4 = (1, c + 1)
        return a1, a2, a3, a4, a1

    def head_polygon_point(self):
        return self.head_polygon_line_point()[0:4]

    def side_polygon_line_point(self):
        c = self.img_rate * self.width
        a1 = (1 + self.depth, c + 1)
        a2 = (1 + self.depth + c, 1)
        a3 = (1 + self.depth + c, 1 + self.height)
        a4 = (1 + self.depth, 1 + c + self.height)
        return a1, a2, a3, a4, a1

    def side_polygon_point(self):
        return self.side_polygon_line_point()[0:4]

    def drawMainRect(self):
        self._draw.rectangle(self.main_rect_point(), fill=self.layer_color)
        self._draw.line(self.main_rect_line_point(), fill=self.line_color, width=1)

    def drawHeadRect(self):
        self._draw.polygon(self.head_polygon_point(), fill=self.layer_color)
        self._draw.line(self.head_polygon_line_point(), fill=self.line_color, width=1)

    def drawSideRect(self):
        self._draw.polygon(self.side_polygon_point(), fill=self.layer_color)
        self._draw.line(self.side_polygon_line_point(), fill=self.line_color, width=1)

    def drawLayer(self):
        self.drawMainRect()
        self.drawHeadRect()
        self.drawSideRect()

    def get_image(self, **kwargs):
        """
        Return the image class for further processing.
        """
        return self._img

    def save(self, stream, format=None, **kwargs):
        if format is None:
            format = kwargs.get("kind", self.kind)
        if "kind" in kwargs:
            del kwargs["kind"]
        self._img.save("new_layers.png")
        # self._img.save(stream, format=format, **kwargs)


if __name__ == '__main__':
    l1 = LayerImage(depth=10, width=29, height=100, layer_color=(246, 246, 246, 216), line_color=(0, 0, 0))
    l1.drawLayer()
    l1.save(1, 'png')
