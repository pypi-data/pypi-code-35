
# crossclip -- cross platform clipboard API
# Copyright (C) 2019  Charlie Sale

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# qtbackend.py -- qt backend class

from PyQt5.Qt import QApplication, QClipboard, QBuffer
from PyQt5.QtGui import QImage, QPixmap
import PyQt5
from PIL import Image as PilImage

from .absbackend import AbstractBackend, AbstractImageConverter


class QtImageConverter(AbstractImageConverter):

    native_image = QImage
    native_image_str = 'qt'

    def to_pillow(qimage):
        buf = QBuffer()
        buf.open(QBuffer.ReadWrite)
        qimage.save(buf, 'PNG') # TODO: make this dynamic
        pimage = PilImage.open(io.BytesIO(buf.data()))
        return pimage

    def from_pillow(image):
        qimg = PilImageQt(image)
        return qimg

class QtBackend(AbstractBackend):
    """ Backend for Qt clipboard

    This class backends the default Qt Clipboard
    """
    image_converter = QtImageConverter

    def __init__(self):
        # Get the default application. I am ignoring any sort
        # of signal/slot setup. This will all be based off of user
        # actions
        super().__init__()
        self.app = QApplication([])
        self.clipboard = self.app.clipboard()

    def get_text(self):
        return self.clipboard.text()

    def get_image(self, format='pil'):
        img = self.clipboard.image()
        if format == self.image_converter.native_image_str:
            return img
        elif format == 'pil':
            return self.image_converter.to_pillow(img)
        else:
            raise RuntimeWarning('Image format is not supported')
            return None

    def set_text(self, text):
        self.clipboard.setText(text)

    def set_image(self, image, format='pil'):
        if format == self.image_converter.native_image_str:
            self.clipboard.setImage(image)
        elif format == 'pil':
            qimg = self.image_converter.from_pillow(image)
            self.clipboard.setImage(qimg)
        else:
            raise RuntimeWarning('Image format is not supported')
            return None
