import click
import os
import shutil
import subprocess
from cookiecutter.main import cookiecutter
from pathlib import Path
from typing import MutableMapping


class _TemporaryGitWorktreeDirectory:
    """Context Manager for a temporary working directory of a branch in a git repo"""

    def __init__(self, path: str, repo: str, branch: str = 'master'):
        self.repo = repo
        self.path = path
        self.branch = branch

    def __enter__(self):
        if not os.path.exists(os.path.join(self.repo, ".git")):
            raise Exception("Not a git repository: %s" % self.repo)

        if os.path.exists(self.path):
            raise Exception("Temporary directory already exists: %s" % self.path)

        os.makedirs(self.path)
        subprocess.run(["git", "worktree", "add", "--no-checkout", self.path, self.branch],
                       cwd=self.repo, check=True)

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.path)
        subprocess.run(["git", "worktree", "prune"], cwd=self.repo, check=True)


def _git_repository_has_local_changes(git_repository: Path):
    result: subprocess.CompletedProcess = subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"],
                                                         cwd=str(git_repository), check=False)
    if result.returncode == 0:
        return False
    elif result.returncode == 1:
        return True
    else:
        raise Exception("could not determine whether git worktree is clean: " + repr(result))


def update_project_template_branch(context: MutableMapping[str, str], project_directory: str, branch: str,
                                   merge_now: bool):
    """Update template branch from a template url"""
    template_url = context['_template']
    tmp_directory = os.path.join(project_directory, ".git", "cookiecutter")
    project_directory_name = os.path.basename(project_directory)
    tmp_git_worktree_directory = os.path.join(tmp_directory, context.get('project_slug') or project_directory_name)

    if subprocess.run(["git", "rev-parse", "-q", "--verify", branch], cwd=project_directory).returncode != 0:
        # create a template branch if necessary
        click.echo(f"Creating git branch {branch}")
        firstref = subprocess.run(["git", "rev-list", "--max-parents=0", "--max-count=1", "HEAD"],
                                  cwd=project_directory,
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True,
                                  check=True).stdout.strip()
        subprocess.run(["git", "branch", branch, firstref], cwd=project_directory)

    with _TemporaryGitWorktreeDirectory(tmp_git_worktree_directory, repo=project_directory, branch=branch):
        # update the template
        click.echo(f"Updating template in branch {branch} using extra_context={context}")
        cookiecutter(template_url,
                     no_input=True,
                     extra_context=context,
                     overwrite_if_exists=True,
                     output_dir=tmp_directory)
        click.echo("===========================================")
        click.echo("Finished generating project from template.")

        # commit to template branch
        subprocess.run(["git", "add", "-A", "."], cwd=tmp_git_worktree_directory, check=True)
        has_changes = _git_repository_has_local_changes(Path(tmp_git_worktree_directory))
        if has_changes:
            click.echo("Committing changes...")
            subprocess.run(["git", "commit", "-m", "Update template"],
                           cwd=tmp_git_worktree_directory, check=True)
            subprocess.run(["git", "push", "origin", branch],
                           cwd=tmp_git_worktree_directory, check=False)
            click.echo(f"===========")

    if has_changes:
        if merge_now:
            result = subprocess.run(["git", "merge", branch],
                                    cwd=project_directory, check=False)
            click.echo(f"===========")
            if result.returncode == 0:
                click.echo("Merged changes successfully.")
            else:
                click.echo("Started merging changes into current branch, "
                           "however there seem to be conflicts or the working tree was not clean.")
        else:
            click.echo(
                f"Changes have been commited into branch '{branch}'. "
                f"Use the following command to update your branch:\n"
                f"git merge {branch}")

    else:
        click.echo("No changes found")
