from pathlib import Path

from plumbum import cmd, local, ProcessExecutionError, RETCODE

MODIFIED_PATH = Path.home() / ".modified"
MODIFIED_PATH.touch()


def count_unpushed_commits() -> int:
    """Determine the number of unpushed commits for the cwd.

    :return:
    """
    branch_ref = cmd.git("symbolic-ref", "-q", "HEAD").strip()
    if not branch_ref:
        return False

    branch_origin = cmd.git("for-each-ref", "--format='%(upstream:short)'", branch_ref).strip().replace("'", '')
    if not branch_origin:
        return False

    assert branch_ref.startswith("refs/heads/")
    branch = branch_ref[len("refs/heads/"):]
    return int(cmd.git("rev-list", f"{branch_origin}..{branch}", "--count").strip())


def has_uncommitted_changes() -> bool:
    """Determine whether there are any uncommitted changes in the cwd.

    :return:
    """
    retcode = cmd.git["diff", "--no-ext-diff", "--quiet", "--exit-code"] & RETCODE
    return retcode == 1


def yes_no_response(query: str, default_response: bool = True) -> bool:
    """Prompt user with a yes / no response for a given query string.

    :param query: query string
    :param default_response: default return value if user input invalid
    :return:
    """
    default_string = "Y/n" if default_response else "y/N"

    response = input(f"{query} [{default_string}] ").lower().strip()
    if response in ("y", "yes"):
        return True
    elif response in ("n", "no"):
        return False
    return default_response


def read_changes():
    for path_str in MODIFIED_PATH.read_text().splitlines():
        path = Path(path_str)
        if not path.exists():
            continue

        try:
            with local.cwd(path):
                if has_uncommitted_changes():
                    should_commit = yes_no_response(f"{path} has uncommitted changes, do you want to commit them?")
                    if should_commit:
                        message = input(
                            "Enter commit message (leave blank for default): ") or "Default git-gone commit message."
                        cmd.git("commit", "-am", message)

                if count_unpushed_commits():
                    should_push = yes_no_response(f"{path} has unpushed commits, do you want to push them?")
                    if should_push:
                        print("Pushing commits...")
                        cmd.git("push")

            # Clear modified file
            MODIFIED_PATH.write_text("")

        except ProcessExecutionError:
            continue
