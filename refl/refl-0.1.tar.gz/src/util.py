#!/usr/bin/env python3

from typing import *
import subprocess
import urllib.request

from tqdm import tqdm
import tarfile

from .config import *

class DownloadProgressBar(tqdm):
  def update_to(self, b=1, bsize=1, tsize=None):
    if tsize is not None:
      self.total = tsize
    self.update(b * bsize - self.n)

def download_url(url, output_path):
  with DownloadProgressBar(unit='B', unit_scale=True,
                           miniters=1, desc=url.split('/')[-1]) as t:
    urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def unzip(fname:str):
  dir = os.path.dirname(os.path.realpath(fname))

  if (fname.endswith("tar.gz")):
    tar = tarfile.open(fname, "r:gz")
    tar.extractall(dir)
    tar.close()

def run(cmd:str, cwd:str) -> int:
  ret = -1

  try:
    ret = subprocess.run(cmd, cwd=cwd, shell=True, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    pass

  return ret


T = TypeVar('T')
def flatten(xs:List[List[T]]) -> List[T]:
  return [ y for ys in xs for y in ys ]
