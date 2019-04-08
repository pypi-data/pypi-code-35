#!/usr/bin/env python3

import os
from os import path
from typing import *
import getpass

from logging import Logging
from config import *
from util import *

log = Logging(LOGLEVEL)()


class Installation:
  def __init__(self, root:str=ROOT, version:str='latest'):
    assert path.exists(root), 'Root path does not exist'

    self.root = root
    self.version = version

  def __call__(self:Any) -> bool:
    log.info('====== Installing Agda version {self.version} at {self.root}/agda-{self.version} ======')
    log.info('')
    log.info('')

    log.info('====== Downloading stack ======')
    stack_path = path.join(self.root, 'agda-' + self.version)

    os.mkdir(stack_path)
    download_url(
      'https://get.haskellstack.org/stable/linux-x86_64.tar.gz',
      path.join(stack_path, 'stack.tar.gz')
    )
    unzip(path.join(stack_path, 'stack.tar.gz'))
    os.remove(path.join(stack_path, 'stack.tar.gz'))

    stack_dir = [ x for x in os.listdir(stack_path) if 'stack' in x ][0]
    os.rename(
      path.join(path.join(stack_path, stack_dir), 'stack'),
      path.join(stack_path, 'stack')
    )

    log.info('====== Installing Agda ======')
    ret = run('./stack install cabal-install', stack_path)
    ret = run('./stack install happy', stack_path)
    ret = run('./stack --resolver lts-12.0 --install-ghc install Agda', stack_path)
    if ret.returncode != 0:
      log.critical('Failed to install Agda')
      raise Exception('Failed to install Agda, perhaps some packages are missing?')
    else:
      log.info('====== Agda Installed ======')

    dot_agda = path.join(HOME, '.agda')
    os.mkdir(dot_agda)

    log.info('Next things to do:')
    log.info('Run `agdatool install bash` or `agdatool install zsh` after this for integrating with respective shells')

    return True

  def bash(self):
    with open(path.join(HOME, '.bashrc'), 'w+') as bashrc:
      bashrc.write('export PATH=~/.local/bin:$PATH')
      bashrc.write('\n')

  def zsh(self):
    with open(path.join(HOME, '.zshrc'), 'w+') as zshrc:
      zshrc.write('export PATH=~/.local/bin:$PATH')
      zshrc.write('\n')


