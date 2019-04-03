import backoff
import logging
from pathlib import Path
from tjpy_subprocess_util.exception import SubProcessExecutionException

from tjpy_git_util.shell_wrapper import git_get_current_local_branch, git_diff_to, git_fetch, git_rebase, git_push

_logger = logging.getLogger(__name__)


def safely_push_changes(repository: Path):
    """
    Use this function to safely update and push commits.

    In case of conflicts the push will be aborted and the contents of a git diff will be printed.
    Our gitblit is a bit... bitchy.
    Retry handling and posting contents in case of an error should be done automatically.
    Also there are a few cases of parallel use where the repository has to be updated first.
    """
    current_branch = git_get_current_local_branch(repository)
    diff = git_diff_to(repository, "origin/" + current_branch)
    try:
        _push_with_retry(repository)
    except Exception:
        _logger.critical(
            f"Failed to push changes. "
            f"Changes have to be manually applied if you this is running in a Jenkins job and the data is sensitive. "
            f"Git diff of commits is (starting on next line):\n{diff}")
        raise


@backoff.on_exception(backoff.constant,  # type: ignore # to ignore untyped decorator of 3rd-party lib
                      SubProcessExecutionException,
                      interval=3,
                      max_tries=5)
def _push_with_retry(repository: Path):
    git_fetch(repository)
    try:
        git_rebase(repository)
    except SubProcessExecutionException as exception:
        raise Exception("Rebase failed, probably a conflict. Will not retry.") from exception
    git_push(repository)
