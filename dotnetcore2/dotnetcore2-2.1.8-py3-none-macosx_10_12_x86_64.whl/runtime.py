# Copyright (c) Microsoft Corporation. All rights reserved.
import distro
import glob
import os
import shutil
import subprocess
import sys
import tarfile
import logging
import urllib.request as request
from urllib.error import HTTPError
from typing import Optional

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')
logger = logging.getLogger(None) # root logger

def _set_logging_level(level):
    logger.setLevel(level)

def _enable_debug_logging():
    _set_logging_level(logging.DEBUG)

def _disable_debug_logging():
    _set_logging_level(logging.WARNING)


__version__ = '2.1.8'   # {major dotnet version}.{minor dotnet version}.{revision}
# We can rev the revision due to patch-level change in .net or changes in dependencies

deps_url_base = 'https://azuremldownloads.blob.core.windows.net/dotnetcore2-dependencies/' + __version__ + '/'
dist = None
version = None
if sys.platform == 'linux':
    dist = distro.id()
    version = distro.version_parts()

def _get_bin_folder() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin')


def get_runtime_path():
    search_string = os.path.join(_get_bin_folder(), 'dotnet*')
    matches = [f for f in glob.glob(search_string, recursive=True)]
    return matches[0]

def ensure_dependencies() -> Optional[str]:
    if dist is None:
        return None

    bin_folder = _get_bin_folder()
    deps_path = os.path.join(bin_folder, 'deps')
    deps_tar_path = deps_path + '.tar'
    success_file = os.path.join(deps_path, 'SUCCESS-' + __version__)
    if os.path.exists(success_file):
         return deps_path

    shutil.rmtree(deps_path, ignore_errors=True)

    deps_url = _construct_deps_url(deps_url_base)
    logger.debug("Constructed deps url: {}".format(deps_url))
    try:
        deps_tar = request.urlopen(deps_url)
        with open(deps_tar_path, 'wb') as f:
            f.write(deps_tar.read())
    except HTTPError as e:
        logger.debug("Error Code when accessing deps_url: {}".format(e.code))
        raise ValueError('Unsupported Linux distribution {0} {1}.{2}'.format(dist, version[0], version[1]))

    with tarfile.open(deps_tar_path, 'r') as tar:
        tar.extractall(path=bin_folder)

    os.remove(deps_tar_path)
    with open(success_file, 'a'):
        os.utime(success_file, None)
    return deps_path

def _construct_deps_url(base_url: str) -> str:
    return base_url + dist + '/' + version[0] + '/' + 'deps.tar'
