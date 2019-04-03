import logging
from pathlib import Path

from tjpy_git_util.shell_wrapper import git_fetch, git_rebase

_logger = logging.getLogger(__name__)


def update_repository(repository_directory: Path, autostash: bool = True):
    # TODO retry handling?
    _logger.info(f"Updating repository {repository_directory.name} ({str(repository_directory)})")
    git_fetch(repository_directory)
    git_rebase(repository_directory, autostash)
