import logging
import os
import shutil
import stat
from pathlib import Path

_logger = logging.getLogger(__name__)


def assert_path_exists(path: Path):
    if not path.exists():
        raise Exception(f"The path {str(path)} does not exist")


def assert_path_is_file(path: Path):
    if not path.is_file():
        raise Exception(f"The path {str(path)} does not exist or is no file")
