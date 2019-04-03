import logging
from pathlib import Path

from tjpy_subprocess_util.execution import SubProcessExecution

_logger = logging.getLogger(__name__)


def initialize_git_repository_and_commit_everything(repository: Path, message="initial"):
    SubProcessExecution.execute(["git", "init"], working_directory=repository)
    SubProcessExecution.execute(["git", "add", "-A"], working_directory=repository)
    SubProcessExecution.execute(["git", "commit", "-m", message], working_directory=repository)
