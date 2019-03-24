
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

# backends.py -- backend classes

import sys
import os
from abc import ABC, abstractmethod, abstractstaticmethod, abstractproperty

class AbstractBackend(ABC):
    """ Interface for all clipboard backends

    This class is an interface for all clipboard backends to
    be registered into.
    """
    @abstractmethod
    def get_text(self):
        """ Synchronously gets text from clipboard
        :returns: Text from clipboard
        :rtype: str
        """
        pass

    @abstractmethod
    def get_image(self, form):
        """ Synchronously gets image from clipboard
        :returns: Image from clipboard
        :rtype:
        """
        pass

    @abstractmethod
    def set_text(self, text):
        """ Sets text to the clipboard
        :param text: Text to add
        :type text: str
        """
        pass

    @abstractmethod
    def set_image(self, img):
        """ Sets image to clipboard
        :param img: Image to set to clipboard
        :type img:
        """
        pass

class AbstractImageConverter(ABC):
    """ Converts an image between a Pillow Image and a native clipboard image

    This interface is needed to convert native images to pillow images and vice
    versa.
    """
    @abstractproperty
    def image_type(self):
        """ The type of native image
        """
        pass

    @abstractproperty
    def image_str(self):
        """ String representing image
        """
        pass

    @abstractmethod
    def to_pillow(self, native_image):
        """ Converts a native image to Pillow iamge
        """
        pass

    @abstractmethod
    def from_pillow(self, pil):
        """ Converts a pillow image to native type
        """
        pass
