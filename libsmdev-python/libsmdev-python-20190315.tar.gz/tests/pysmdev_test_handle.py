#!/usr/bin/env python
#
# Python-bindings handle type test script
#
# Copyright (C) 2010-2019, Joachim Metz <joachim.metz@gmail.com>
#
# Refer to AUTHORS for acknowledgements.
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import sys
import unittest

import pysmdev


class HandleTypeTests(unittest.TestCase):
  """Tests the handle type."""

  def test_signal_abort(self):
    """Tests the signal_abort function."""
    smdev_handle = pysmdev.handle()

    smdev_handle.signal_abort()

  def test_open(self):
    """Tests the open function."""
    if not unittest.source:
      return

    smdev_handle = pysmdev.handle()

    smdev_handle.open(unittest.source)

    with self.assertRaises(IOError):
      smdev_handle.open(unittest.source)

    smdev_handle.close()

    with self.assertRaises(TypeError):
      smdev_handle.open(None)

    with self.assertRaises(ValueError):
      smdev_handle.open(unittest.source, mode="w")

  def test_open_file_object(self):
    """Tests the open_file_object function."""
    if not unittest.source:
      return

    file_object = open(unittest.source, "rb")

    smdev_handle = pysmdev.handle()

    smdev_handle.open_file_object(file_object)

    with self.assertRaises(IOError):
      smdev_handle.open_file_object(file_object)

    smdev_handle.close()

    # TODO: change IOError into TypeError
    with self.assertRaises(IOError):
      smdev_handle.open_file_object(None)

    with self.assertRaises(ValueError):
      smdev_handle.open_file_object(file_object, mode="w")

  def test_close(self):
    """Tests the close function."""
    if not unittest.source:
      return

    smdev_handle = pysmdev.handle()

    with self.assertRaises(IOError):
      smdev_handle.close()

  def test_open_close(self):
    """Tests the open and close functions."""
    if not unittest.source:
      return

    smdev_handle = pysmdev.handle()

    # Test open and close.
    smdev_handle.open(unittest.source)
    smdev_handle.close()

    # Test open and close a second time to validate clean up on close.
    smdev_handle.open(unittest.source)
    smdev_handle.close()

    file_object = open(unittest.source, "rb")

    # Test open_file_object and close.
    smdev_handle.open_file_object(file_object)
    smdev_handle.close()

    # Test open_file_object and close a second time to validate clean up on close.
    smdev_handle.open_file_object(file_object)
    smdev_handle.close()

    # Test open_file_object and close and dereferencing file_object.
    smdev_handle.open_file_object(file_object)
    del file_object
    smdev_handle.close()

  def test_read_buffer(self):
    """Tests the read_buffer function."""
    if not unittest.source:
      return

    smdev_handle = pysmdev.handle()

    smdev_handle.open(unittest.source)

    file_size = smdev_handle.get_size()

    # Test normal read.
    data = smdev_handle.read_buffer(size=4096)

    self.assertIsNotNone(data)
    self.assertEqual(len(data), min(file_size, 4096))

    if file_size < 4096:
      data = smdev_handle.read_buffer()

      self.assertIsNotNone(data)
      self.assertEqual(len(data), file_size)

    # Test read beyond file size.
    if file_size > 16:
      smdev_handle.seek_offset(-16, os.SEEK_END)

      data = smdev_handle.read_buffer(size=4096)

      self.assertIsNotNone(data)
      self.assertEqual(len(data), 16)

    with self.assertRaises(ValueError):
      smdev_handle.read_buffer(size=-1)

    smdev_handle.close()

    # Test the read without open.
    with self.assertRaises(IOError):
      smdev_handle.read_buffer(size=4096)

  def test_read_buffer_file_object(self):
    """Tests the read_buffer function on a file-like object."""
    if not unittest.source:
      return

    file_object = open(unittest.source, "rb")

    smdev_handle = pysmdev.handle()

    smdev_handle.open_file_object(file_object)

    file_size = smdev_handle.get_size()

    # Test normal read.
    data = smdev_handle.read_buffer(size=4096)

    self.assertIsNotNone(data)
    self.assertEqual(len(data), min(file_size, 4096))

    smdev_handle.close()

  def test_read_buffer_at_offset(self):
    """Tests the read_buffer_at_offset function."""
    if not unittest.source:
      return

    smdev_handle = pysmdev.handle()

    smdev_handle.open(unittest.source)

    file_size = smdev_handle.get_size()

    # Test normal read.
    data = smdev_handle.read_buffer_at_offset(4096, 0)

    self.assertIsNotNone(data)
    self.assertEqual(len(data), min(file_size, 4096))

    # Test read beyond file size.
    if file_size > 16:
      data = smdev_handle.read_buffer_at_offset(4096, file_size - 16)

      self.assertIsNotNone(data)
      self.assertEqual(len(data), 16)

    with self.assertRaises(ValueError):
      smdev_handle.read_buffer_at_offset(-1, 0)

    with self.assertRaises(ValueError):
      smdev_handle.read_buffer_at_offset(4096, -1)

    smdev_handle.close()

    # Test the read without open.
    with self.assertRaises(IOError):
      smdev_handle.read_buffer_at_offset(4096, 0)

  def test_seek_offset(self):
    """Tests the seek_offset function."""
    if not unittest.source:
      return

    smdev_handle = pysmdev.handle()

    smdev_handle.open(unittest.source)

    file_size = smdev_handle.get_size()

    smdev_handle.seek_offset(16, os.SEEK_SET)

    offset = smdev_handle.get_offset()
    self.assertEqual(offset, 16)

    smdev_handle.seek_offset(16, os.SEEK_CUR)

    offset = smdev_handle.get_offset()
    self.assertEqual(offset, 32)

    smdev_handle.seek_offset(-16, os.SEEK_CUR)

    offset = smdev_handle.get_offset()
    self.assertEqual(offset, 16)

    smdev_handle.seek_offset(-16, os.SEEK_END)

    offset = smdev_handle.get_offset()
    self.assertEqual(offset, file_size - 16)

    smdev_handle.seek_offset(16, os.SEEK_END)

    offset = smdev_handle.get_offset()
    self.assertEqual(offset, file_size + 16)

    # TODO: change IOError into ValueError
    with self.assertRaises(IOError):
      smdev_handle.seek_offset(-1, os.SEEK_SET)

    # TODO: change IOError into ValueError
    with self.assertRaises(IOError):
      smdev_handle.seek_offset(-32 - file_size, os.SEEK_CUR)

    # TODO: change IOError into ValueError
    with self.assertRaises(IOError):
      smdev_handle.seek_offset(-32 - file_size, os.SEEK_END)

    # TODO: change IOError into ValueError
    with self.assertRaises(IOError):
      smdev_handle.seek_offset(0, -1)

    smdev_handle.close()

    # Test the seek without open.
    with self.assertRaises(IOError):
      smdev_handle.seek_offset(16, os.SEEK_SET)


if __name__ == "__main__":
  argument_parser = argparse.ArgumentParser()

  argument_parser.add_argument(
      "source", nargs="?", action="store", metavar="PATH",
      default=None, help="The path of the source file.")

  options, unknown_options = argument_parser.parse_known_args()
  unknown_options.insert(0, sys.argv[0])

  setattr(unittest, "source", options.source)

  unittest.main(argv=unknown_options, verbosity=2)
