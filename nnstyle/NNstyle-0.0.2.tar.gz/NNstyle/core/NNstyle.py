import math
from NNstyle.core.LayerImage import LayerImage
from NNstyle.core.ArrowImage import ArrowImage

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    import Image
    import ImageDraw


class NNstyle:
    def __init__(self, size_layers, colors_layers):
        self.sizes = size_layers
        self.colors = colors_layers
        self.len_layers = len(size_layers)
        self.len_arrow = self.len_layers - 1
        self.width = []
        self.w = 0
        self.h = 0
        self.background = self.makeBG()
        self.makeNN()

    def makeBG(self):
        mode = "RGBA"
        width = 0
        height = 0
        for i, x in enumerate(self.sizes):
            width += x[2] + x[1] * math.sqrt(2) / 2 + 25
            self.width.append(width)
            if height < x[0] + x[1] * math.sqrt(2) / 2:
                height = x[0] + x[1] * math.sqrt(2) / 2
        img = Image.new(mode=mode, size=(int(width), int(height) + 10))
        self.w = int(width)
        self.h = int(height) + 10
        self._draw = ImageDraw.Draw(img)
        return img

    def makeNN(self):
        # x : h w d
        for i, x in enumerate(self.sizes):
            L = LayerImage(height=self.sizes[i][0], width=self.sizes[i][1], depth=self.sizes[i][2],
                           layer_color=self.colors[i], line_color=(0, 0, 0))
            L.drawLayer()
            l_im = L.get_image()
            if i == 0:
                self.background.paste(l_im, (int(self.width[i]) - 25 - self.sizes[i][1], 5))
                A = ArrowImage(width=10, height=10, arrow_color=(242, 242, 242, 256), line_color=(0, 0, 0))
                A.drawArrow()
                a_im = A.get_image()
                self.background.paste(a_im, (int(self.width[i]) - 15, int(self.h / 2)))
            else:
                self.background.paste(l_im, (int(self.width[i] - 25 - self.sizes[i][1]), 5))
                if i == len(self.sizes) - 1: continue
                A = ArrowImage(width=10, height=10, arrow_color=(242, 242, 242, 256), line_color=(0, 0, 0))
                A.drawArrow()
                a_im = A.get_image()
                self.background.paste(a_im, (int(self.width[i] - 15), int(self.h / 2)))

    def saveNN(self, dist="./NN.png"):
        self.background.save(dist)

    def getNN(self):
        return self.background



