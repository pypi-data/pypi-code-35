import logging
from pathlib import Path
from tjpy_subprocess_util.execution import SubProcessExecution
from typing import List, Optional

_logger = logging.getLogger(__name__)


def git_push(repository: Path):
    SubProcessExecution.execute(["git", "push"], working_directory=repository,
                                logging_level="INFO")


def git_init(repository: Path):
    SubProcessExecution.execute("git init".split(), working_directory=repository)


def git_add(repository: Path,
            path_to_stage_for_commit: Optional[Path]):
    SubProcessExecution.execute(["git", "add", str(path_to_stage_for_commit)], working_directory=repository)


def git_add_everything(repository: Path):
    SubProcessExecution.execute("git add -A .".split(), working_directory=repository)


def git_commit_staged_changes(repository: Path, message: str):
    SubProcessExecution.execute(["git", "commit", "-m", message], working_directory=repository)


def git_rebase(repository_directory, autostash: bool = True):
    autostash_parameters = ["--autostash"] if autostash else []
    SubProcessExecution.execute(["git", "rebase", *autostash_parameters], working_directory=repository_directory)


def git_fetch(repository_directory: Path):
    SubProcessExecution.execute("git fetch".split(), working_directory=repository_directory,
                                logging_level="INFO")


def git_set_autostash_on_rebase(repository_directory: Path):
    SubProcessExecution.execute("git config rebase.autoStash true".split(), working_directory=repository_directory)


def git_get_current_local_branch(repository_directory: Path) -> str:
    result = SubProcessExecution.execute("git rev-parse --abbrev-ref HEAD".split(),
                                         working_directory=repository_directory)
    return result.trimmed_stdout


def git_diff_to(repository_directory: Path, to: str) -> str:
    result = SubProcessExecution.execute(["git", "diff", to],
                                         working_directory=repository_directory)
    return result.stdout


def git_clone(source: str, target: Path):
    SubProcessExecution.execute(["git", "clone", source, str(target)],
                                logging_level="INFO")


def git_checkout(repository_directory: Path, target: str, option_args: Optional[List[str]] = None):
    if option_args is None:
        option_args = []
    SubProcessExecution.execute(["git", "checkout", *option_args, target],
                                working_directory=repository_directory)


def git_get_commit_id(repository_directory: Path, ref: str = "HEAD") -> str:
    result = SubProcessExecution.execute(["git", "rev-parse", ref],
                                         working_directory=repository_directory)
    return result.trimmed_stdout


def git_get_commit_message(repository_directory: Path, commit: str = "HEA") -> str:
    result = SubProcessExecution.execute(["git", "show", "-s", "--format=%B", commit],
                                         working_directory=repository_directory)
    return result.trimmed_stdout
