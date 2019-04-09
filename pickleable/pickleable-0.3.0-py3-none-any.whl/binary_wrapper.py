import tempfile
import os
import shutil
from io import BytesIO
from copy import copy
from subprocess import call
from pathlib import Path
from random import random
from distutils.dir_util import copy_tree

def ensure_dir(directory):
  if not os.path.exists(directory):
    try:
      os.makedirs(directory)
    except OSError as e:
      if e.errno != os.errno.EEXIST:
        raise

def get_tmp_directory():
  tmp_dir = Path(tempfile.gettempdir())
  destination = 'tmp-' + str(random())[2:]
  dir_path = tmp_dir / destination
  os.makedirs(dir_path)
  return dir_path

def read_bytes(path):
  with open(path, 'rb') as file:
    return BytesIO(file.read())

def write_bytes(path, data):
  with open(path, 'wb') as file:
    file.write(data)

def path_to_byte_map(root, path, binary_by_path={}):
  if path.is_file():
    binary_by_path[path.relative_to(root)] = read_bytes(path)
  else:
    for sub_path in path.iterdir():
      if sub_path.name not in ['.DS_Store', 'thumbs.db']:
        path_to_byte_map(root, sub_path, binary_by_path)
  return binary_by_path

def byte_map_to_files(root, byte_map):
  directories = {rel_path.parent for rel_path in byte_map.keys()}
  for directory in directories:
    ensure_dir(Path(root, directory))
  for rel_path, bytes_ in byte_map.items():
    full_path = Path(root, rel_path)
    data = copy(bytes_).read()
    write_bytes(full_path, data)

class BinaryWrapper:
  def __init__(self):
    self.path = get_tmp_directory()

  def __enter__(self):
    return self

  def __exit__(self, *_):
    self.byte_map = path_to_byte_map(self.path, self.path)
    shutil.rmtree(self.path)
    self.path = None

  def update(self, byte_map):
    bw = BinaryWrapper()
    bw.path = None
    bw.byte_map = self.byte_map.copy()
    for key, value in byte_map.items():
      bw.byte_map[key] = BytesIO(str.encode(value))
    return bw

  def unwrap(self):
    return BinaryUnwrapper(self.byte_map)

class BinaryUnwrapper:
  def __init__(self, byte_map):
    self.path = get_tmp_directory()
    self.byte_map = byte_map

  def __enter__(self):
    byte_map_to_files(self.path, self.byte_map)
    return self.path

  def __exit__(self, *_):
    try:
      shutil.rmtree(self.path)
    except FileNotFoundError:
      pass

def binary_wrapper_from_dir(path):
  with BinaryWrapper() as bw:
    copy_tree(sim_path, str(bw.path))
  return bw
