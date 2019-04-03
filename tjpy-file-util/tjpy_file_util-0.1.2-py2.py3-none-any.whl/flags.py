import logging
import os
import stat
from pathlib import Path

from tjpy_file_util.user_friendly_assertion import assert_path_is_file

_logger = logging.getLogger(__name__)


def make_file_executable_if_necessary(file: Path):
    assert_path_is_file(file)
    if not os.access(str(file), os.X_OK):
        mode = file.stat().st_mode
        new_mode = mode | stat.S_IEXEC
        _logger.info(f"Making file {file} executable")
        file.chmod(new_mode)
