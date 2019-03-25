import click
import sys
import pathlib
import shutil
import os
import stat

from ..logger import Logger
from subprocess import run, PIPE
from datetime import datetime


class NinjaPatcher(Logger):
    def __init__(self, config):
        super().__init__(config)
        self.datetime_str = str(datetime.now()).replace(" ", "-").replace(":", "-").replace(".", "-")
        self.folder_name = "ninja-patching-" + self.datetime_str
        self.folder = pathlib.Path.cwd().joinpath(self.folder_name)
        self.seed_repo_path = self.folder_name + "/seed/"
        self.all_repo_path = self.folder_name + "/all/"
        self.patch_filename = "patch.patch"

    def execute(self):
        self.folder.mkdir()
        click.echo("Created folder " + self.folder_name)

        self._prompt_repo_configuration()
        self._update_all_repo()
        self._read_submodule_names()
        self._create_patch()
        self._prompt_confirmation()
        self._apply_patch()

        shutil.rmtree(self.folder, onerror=self._remove_readonly)
        click.echo("Removed folder " + self.folder_name)
        sys.exit(0)

    def _prompt_repo_configuration(self):
        """
        Prompt user inputs about
            1. URL of the seed repository
            2. Commit SHA-1 of the current patch
            3. Commit SHA-1 of the new patch

        :return: None
        """
        seed_repo_url = click.prompt(click.style('SSH URL of the seed repo (git@ada....git)', fg='magenta'),
                                     type=str)
        completed_process = run(["git", "clone", seed_repo_url, self.seed_repo_path],
                                stderr=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

        all_repo_url = seed_repo_url[:-4] + "-all.git"
        completed_process = run(["git", "clone", all_repo_url, "--recursive", self.all_repo_path],
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

        self.current_sha = click.prompt(click.style('Patch from commit (8-digit/40-digit Git Commit SHA-1)',
                                                    fg='magenta'), type=str)
        completed_process = run(["git", "--git-dir=" + self.seed_repo_path + ".git",
                                 "cat-file", "commit", self.current_sha], stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit("Not a valid commit: " + self.current_sha)

        self.new_sha = click.prompt(click.style('Patch to commit (8-digit/40-digit Git Commit SHA-1)',
                                                fg='magenta'), type=str)
        completed_process = run(["git", "--git-dir=" + self.seed_repo_path + ".git",
                                 "cat-file", "commit", self.new_sha], stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit("Not a valid commit: " + self.new_sha)

        click.echo()

    def _update_all_repo(self):
        completed_process = run(["rc", "git", "checkout", "master"],
                                cwd=self.all_repo_path,
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

        completed_process = run(["rc", "git", "pull", "origin", "master"],
                                cwd=self.all_repo_path,
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))

    def _read_submodule_names(self):
        completed_process = run(["git", "config", "--file", ".gitmodules", "--name-only",
                                 "--get-regexp", "path"],
                                cwd=self.all_repo_path,
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        if completed_process.stdout is None:
            self._error_and_exit("-all repo does not contain any submodules")

        submodule_paths = str(completed_process.stdout, "utf-8").splitlines()
        self.submodule_names = []
        for path in submodule_paths:
            self.submodule_names.append(path.split(".")[1])

    def _create_patch(self):
        completed_process = run(["git", "--git-dir=" + self.seed_repo_path + ".git",
                                 "format-patch", "-k", "--stdout", self.current_sha + ".." + self.new_sha],
                                stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        with click.open_file(self.folder_name + "/" + self.patch_filename, 'w') as f:
            f.write(str(completed_process.stdout, "utf-8"))
        self._success("Generated patch file")
        click.echo()

        self._warn("******START_OF_PATCH******\n\n")
        completed_process = run(["git", "--git-dir=" + self.seed_repo_path + ".git",
                                 "diff", self.current_sha + ".." + self.new_sha],
                                stderr=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        self._warn("\n\n******END_OF_PATCH******\n")

    def _prompt_confirmation(self):
        if not click.confirm(click.style("Do you confirm the changes above and continue?", fg='magenta')):
            self._error_and_exit("Confirmation denied\nNo changes made")
        click.echo()

    def _apply_patch(self):
        click.echo("Started patching...")

        patch_path = "../../" + self.patch_filename
        success_count = 0
        warn_count = 0
        fail_count = 0
        for name in self.submodule_names:
            cwd = self.all_repo_path + name + "/"
            completed_process = run(["git", "apply", "--check", patch_path],
                                    cwd=cwd, stderr=PIPE, stdout=PIPE)
            if completed_process.returncode:
                if not self._has_diff(cwd):
                    self._warn(name + " is already up-to-date")
                    warn_count += 1
                else:
                    self._error("Skipped " + name + " due to merge conflicts")
                    fail_count += 1
            else:
                completed_process = run(["git", "am", "--signoff", patch_path],
                                        cwd=cwd, stderr=PIPE, stdout=PIPE)
                if completed_process.returncode:
                    self._error("Skipped " + name + ": " + str(completed_process.stderr, "utf-8"))
                    fail_count += 1
                else:
                    self._success("Patched " + name)
                    success_count += 1

        click.echo()
        if success_count:
            click.echo("Populating changes to students' repositories...")
            completed_process = run(["rc", "git", "push", "origin", "master"],
                                    cwd=self.all_repo_path,
                                    stderr=PIPE, stdout=PIPE)
            if completed_process.returncode:
                self._error_and_exit(str(completed_process.stderr, "utf-8"))
            click.echo()
        self._success("Ninja Patching completed!")
        self._success("     Patched " + str(success_count + warn_count))
        self._error("     Skipped " + str(fail_count))
        click.echo()

    def _has_diff(self, cwd):
        seed_path = "../../seed/.git"
        completed_process = run(["git", "remote", "add", "seed", seed_path],
                                cwd=cwd, stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        completed_process = run(["git", "remote", "update"],
                                cwd=cwd, stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        completed_process = run(["git", "fetch", "seed", self.new_sha + ":refs/remotes/seed/head"],
                                cwd=cwd, stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        completed_process = run(["git", "diff", "master", "seed/head"],
                                cwd=cwd, stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        diff = completed_process.stdout
        completed_process = run(["git", "remote", "rm", "seed"],
                                cwd=cwd, stderr=PIPE, stdout=PIPE)
        if completed_process.returncode:
            self._error_and_exit(str(completed_process.stderr, "utf-8"))
        return diff

    def _error_and_exit(self, msg):
        self._error(msg + "\n")
        shutil.rmtree(self.folder, onerror=self._remove_readonly)
        click.echo("Removed folder " + self.folder_name)
        sys.exit(1)

    # https://stackoverflow.com/questions/1889597/deleting-directory-in-python/1889686#1889686
    def _remove_readonly(self, func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)
