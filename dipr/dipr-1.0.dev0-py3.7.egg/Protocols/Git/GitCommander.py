from Utilities.Console import Console

import git
from git import Repo
from git import RemoteProgress


class GitCommander(object):
    # region Progress Printing for Git Functions

    class MyProgressPrinter(RemoteProgress):
        """A pretty printer for long running git processes: clone, fetch"""

        def line_dropped(self, line):
            """
            Print lines produced by git.
            :param line: A line emitted by git client.
            """
            Console.print(line)

        def update(self, *args):
            """
            Catch all update statuses alternative to line_dropped.
            :param args: The args to the update.
            """
            Console.print(self._cur_line)

    # endregion

    def __init__(self, full_repo_path):
        self.full_repo_path = full_repo_path

    @property
    def __git_repo(self):
        return Repo(self.full_repo_path)

    @property
    def is_git_dir(self):
        """
        Check if the full repo path is a git directory by opening a repo and catching exceptions that might occur.
        :return: True if full repo path is a git managed directory.
        """
        try:
            _ = self.__git_repo
            return True
        except git.exc.NoSuchPathError:
            return False
        except git.exc.InvalidGitRepositoryError:
            return False

    def is_empty(self):
        try:
            return not bool(str(self.__git_repo.git.rev_list("--max-count=1", "--all")).strip())
        except git.exc.GitCommandError as e:
            Console.warning("Could not check commit list of repo: " + str(self.full_repo_path))
            Console.info("Error: " + str(e))

    @staticmethod
    def __combine_remote(remote, branch):
        """
        Combine remote and branch together as necessary.
        :param remote: Optional remote
        :param branch: The branch to use
        :return: If remote is not empty a combined remote/branch string, otherwise just branch.
        """
        if not remote:
            return branch

        return "/".join([remote, branch])

    def clone(self, url):
        """
        Clone the repo specified by resolved repo.
        """
        Repo.clone_from(url, self.full_repo_path,
                        progress=GitCommander.MyProgressPrinter())

    def fetch(self, remote):
        """
        Fetch changesets for the given remote.
        :param remote: The remote to fetch from.
        """
        try:
            if not remote:
                remote = "origin"

            self.__git_repo.remote(remote).fetch(progress=GitCommander.MyProgressPrinter())
        except git.exc.GitCommandError as e:
            Console.warning("Could not fetch repo: " + self.full_repo_path)
            Console.info("Error: " + str(e))

    def checkout(self, remote, revision):
        """
        Checkout the repo at the specified remote and/or revision (tag, branch, hash)
        :param remote: A remote if required by the resolved repo.
        :param revision: The revision to check out at (tag, branch, hash)
        """
        try:
            revision = GitCommander.__combine_remote(remote, revision)
            self.__git_repo.git.checkout(revision)
        except git.exc.GitCommandError as e:
            Console.warning("Could not update to " + revision + ".  Does it exist?")
            Console.info("Error: " + str(e))

    def pull(self):
        """
        Pull changeset into the checked out revision.
        """
        try:
            self.__git_repo.git.pull()
        except git.exc.GitCommandError as e:
            Console.warning("Could not pull changesets to repo: " + str(self.full_repo_path))
            Console.info("Error: " + str(e))

    def reset(self, remote, revision):
        """
        Hard reset the repo back to the version at remote and revision.
        :param remote: An optional remote.
        :param revision: The revision to reset to.
        """
        revision = GitCommander.__combine_remote(remote, revision)

        try:
            self.__git_repo.git.reset("--hard", revision)
        except git.exc.GitCommandError as e:
            Console.warning("Could not reset to " + revision + ".  Does it exist?")
            Console.info("Error: " + str(e))

    def discard(self):
        try:
            self.__git_repo.git.reset("--hard", "HEAD")
            self.__git_repo.git.clean("-f")
        except git.exc.GitCommandError as e:
            Console.warning("Could not discard changes in the git repo.")
            Console.info("Error: " + str(e))

    def status(self):
        """
        Return the short status of the git repo for display.
        :return: A short status string for the git repo.
        """
        try:
            return self.__git_repo.git.status("-b", "-s")
        except git.exc.GitCommandError as e:
            Console.warning("Could not get status for repo: " + str(self.full_repo_path))
            Console.info("Error: " + str(e))

    def add(self, file):
        """
        Attempts to add the file to the git repo.
        :param file: Path to a file to add.
        """
        try:
            return self.__git_repo.git.add(file)
        except git.exc.GitCommandError as e:
            Console.warning("Could not add file " + file + " to repo: " + str(self.full_repo_path))
            Console.info("Error: " + str(e))

    def file_status(self, file):
        """
        Return the short status of the git repo for display.
        :return: A short status string for the git repo.
        """
        try:
            return self.__git_repo.git.status("--porcelain", file)
        except git.exc.GitCommandError as e:
            Console.warning("Could not get status file: " + file)
            Console.info("Error: " + str(e))

    def remove(self, file):
        try:
            self.__git_repo.git.rm(file)
        except git.exc.GitCommandError as e:
            Console.warning("Could not remove file: " + file)
            Console.info("Error: " + str(e))

    def get_current_revision(self):
        try:
            return self.__git_repo.git.rev_parse("--short", "HEAD")
        except git.exc.GitCommandError as e:
            Console.warning("Could not get current revision ID.")
            Console.info("Error: " + str(e))

    def is_current_revision_tip(self):
        try:
            output = self.__git_repo.git.branch("--contains")
            return "HEAD detached" not in str(output)
        except git.exc.GitCommandError as e:
            Console.warning("Could determine revision tip state.")
            Console.info("Error: " + str(e))

    def get_current_tags(self):
        try:
            tags = self.__git_repo.git.tag("--points-at", "HEAD").split("\n")
            if '' in tags:
                tags.remove('')
            return tags
        except git.exc.GitCommandError as e:
            return None

    def get_latest_tags(self, branch):
        try:
            if not branch:
                branch = "master"
            tags = self.__git_repo.git.tag("--points-at", branch).split("\n")
            if '' in tags:
                tags.remove('')
            return tags
        except git.exc.GitCommandError as e:
            Console.warning("Could not get latest tag information.")
            Console.info("Error: " + str(e))

    def get_current_branch(self):
        try:
            output = str(self.__git_repo.git.branch("--contains"))

            if "HEAD detached" in output:
                return None

            lines = output.split("\n")

            branch = None

            for l in lines:
                if l.startswith("*"):
                    branch = l.split(" ")[1].strip()

            return branch
        except git.exc.GitCommandError as e:
            Console.warning("Could not get latest tag information.")
            Console.info("Error: " + str(e))
        except Exception as e:
            Console.warning("Invalid string return from git while getting branch.")
            Console.info("Error: " + str(e))

    def is_on_default_branch(self):
        branch = self.get_current_branch()

        return branch and branch == "master"

    def has_changes(self):
        try:
            #result = str(self.__git_repo.git.diff_index("HEAD"))
            result = str(self.__git_repo.git.status("-s"))

            return bool(result)
        except git.exc.GitCommandError as e:
            Console.warning("Could not get latest tag information.")
            Console.info("Error: " + str(e))

    def commit(self, message, add_remove):
        try:
            if add_remove:
                self.__git_repo.git.stage("--all", ":/")

            self.__git_repo.git.commit("--all", "-m", message)
        except git.exc.GitCommandError as e:
            Console.warning("Command error during commit.  Are there un-tracked files?")
            Console.info("Error: " + str(e))

    def tag(self, tag, message):
        try:
            self.__git_repo.git.tag("-a", tag, "-m", message)
        except git.exc.GitCommandError as e:
            Console.warning("Error occured while adding a tag.")
            Console.info("Error: " + str(e))

    def push(self, force):
        try:
            if force:
                self.__git_repo.git.push("--all", "--follow-tags", "--force")
            else:
                self.__git_repo.git.push("--all", "--follow-tags")
        except git.exc.GitCommandError as e:
            Console.warning("Error occured while performing a push.")
            Console.info("Error: " + str(e))
