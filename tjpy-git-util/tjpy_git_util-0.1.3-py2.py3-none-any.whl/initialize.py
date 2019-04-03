import logging
from pathlib import Path

from tjpy_git_util.shell_wrapper import git_add_everything, git_commit_staged_changes, git_init

_logger = logging.getLogger(__name__)


def initialize_git_repository_and_commit_everything(repository: Path, message="initial"):
    git_init(repository)
    git_add_everything(repository)
    git_commit_staged_changes(repository, message)
