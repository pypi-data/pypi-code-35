# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    import Image
    import ImageDraw


class ArrowImage:
    kind = "PNG"

    def __init__(self, width, height, *args, **kwargs):
        self.arrow_color = kwargs.get("arrow_color")
        self.line_color = kwargs.get("line_color")
        self.width = width
        self.height = height
        self._img = self.new_image()

    def new_image(self, **kwargs):  # pragma: no cover
        mode = "RGBA"
        img = Image.new(mode=mode, size=(self.width+2, self.height+2))
        self._draw = ImageDraw.Draw(img)
        return img

    def polygon_line_point(self):
        a1 = (1, 1 + self.height / 4)
        a2 = (1 + self.width / 2, 1 + self.height / 4)
        a3 = (1 + self.width / 2, 1)

        a4 = (1 + self.width, 1 + self.height / 2)

        a5 = (1 + self.width / 2, 1 + self.height)
        a6 = (1 + self.width / 2, 1 + 3 * self.height / 4)
        a7 =(1, 1 + 3 * self.height / 4)
        return a1, a2, a3, a4, a5, a6, a7, a1

    def polygon_point(self):
        return self.polygon_line_point()[0:7]

    def drawArrow(self):
        self._draw.polygon(self.polygon_point(), fill=self.arrow_color)
        self._draw.line(self.polygon_line_point(), fill=self.line_color, width=1)

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
        self._img.save("new_arrow.png")
        # self._img.save(stream, format=format, **kwargs)


if __name__ == '__main__':
    A1 = ArrowImage(width=40, height=40, arrow_color=(242, 242, 242, 256), line_color=(0, 0, 0))
    A1.drawArrow()
    A1.save(1, 'png')
