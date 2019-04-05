###########################################################################
#                                                                         #
# This file is part of Counter RNAseq Window (craw) package.              #
#                                                                         #
#    Authors: Bertrand Neron                                              #
#    Copyright (c) 2017-2019  Institut Pasteur (Paris).                   #
#    see COPYRIGHT file for details.                                      #
#                                                                         #
#    craw is free software: you can redistribute it and/or modify         #
#    it under the terms of the GNU General Public License as published by #
#    the Free Software Foundation, either version 3 of the License, or    #
#    (at your option) any later version.                                  #
#                                                                         #
#    craw is distributed in the hope that it will be useful,              #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                 #
#    See the GNU General Public License for more details.                 #
#                                                                         #
#    You should have received a copy of the GNU General Public License    #
#    along with craw (see COPYING file).                                  #
#    If not, see <http://www.gnu.org/licenses/>.                          #
#                                                                         #
###########################################################################

import logging
import os.path
import unittest
import platform
from contextlib import contextmanager
from io import StringIO

import numpy as np
from PIL import ImageChops


class CRAWTest(unittest.TestCase):

    _data_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "data"))

    def assertImageAlmostEqual(self, im1, im2, delta=None, msg=None):
        """"
        :param im1: The first image to compare
        :type im1: a :class:`Image` object
        :param im2: The second Image to compare
        :type im2: a :class:`Image` object
        :param delta: the deviation from ref accepted for instance 1.0 mean that you authorise
                      that the compute image differ from ref for 1 pixel for 1 value of intensity/color
        :type delta: float
        :param str msg: a message to append to the assertion message.
        :return: None if 2 images are identical or if distance is less or equal delta.
                 Otherwise raise an AssertionError
        """

        im_diff = ImageChops.difference(im1, im2)
        if delta is None:
            if im_diff.getbbox() is not None:
                msg = self._formatMessage(msg, 'image 1 != image 2')
                raise self.failureException(msg)
            else:
                return
        else:
            a_diff = np.asarray(im_diff, dtype=np.uint8)
            a_diff = np.transpose(a_diff, (1, 0, 2))
            dist = np.sqrt(np.sum(a_diff**2))
            if dist <= delta:
                return
            msg = self._formatMessage(msg, 'image 1  != image 2 within {} delta'.format(delta))
            raise self.failureException(msg)

    @contextmanager
    def catch_log(self):
        logger = logging.getLogger('craw')
        handlers_ori = logger.handlers
        fake_handler = logging.StreamHandler(StringIO())
        try:
            logger.handlers = [fake_handler]
            yield LoggerWrapper(logger)
        finally:
            logger.handlers = handlers_ori


def which(name, flags=os.X_OK):
    """
    Search PATH for executable files with the given name.

    :param name: the name of the executable to search
    :type name: str
    :param flags: os mod the name must have, default is executable (os.X_OK).
    :type flags: os file mode R_OK|R_OK|W_OK|X_OK
    :return: the path of the executable
    :rtype: string or None
    """
    result = None
    path = os.environ.get('PATH', None)
    if path is None:
        return result
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if platform.system() == 'Windows':
            p += '.exe'
        if os.access(p, flags):
            result = p
            break
    return result


class LoggerWrapper(object):

    def __init__(self, logger):
        self.logger = logger

    def __getattr__(self, item):
        return getattr(self.logger, item)

    def get_value(self):
        return self.logger.handlers[0].stream.getvalue()

