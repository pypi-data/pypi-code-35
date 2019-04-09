
from abc import ABC
from shutil import rmtree

from Utilities.Console import Console
from Commands.DiprCommandBase import DiprCommandBase


class RepoCommandBase(DiprCommandBase, ABC):

    def __init__(self, user_settings):
        super(RepoCommandBase, self).__init__(user_settings)

    def execute(self, arguments):
        repo_settings = super()._open_repo(arguments)

        if not repo_settings.is_initialized:
            Console.error("Repo " + str(repo_settings.root_repo_path) + " is not initialized.")
            return

        repo_arguments = self._get_arguments(arguments)

        repos = self._open_repos(repo_settings, repo_arguments)
        resolved_repos = self._open_resolved_repos(repo_settings, repo_arguments)

        command = repo_arguments.command.lower()

        if command == "list":
            self._list_repos(resolved_repos, repo_settings, repo_arguments)
        elif command == "add":
            self._add_repo(repos, repo_settings, repo_arguments)
        elif command == "remove":
            self._remove_repo(repos, resolved_repos, repo_settings, repo_arguments)
        elif command == "freeze":
            self._freeze_repos(repos, resolved_repos, repo_settings, repo_arguments)
        elif command == "unfreeze":
            self._unfreeze_repos(repos, resolved_repos, repo_settings, repo_arguments)
        elif command == "upgrade":
            self._upgrade_repos(repos, resolved_repos, repo_settings, repo_arguments)
        elif command == "rev":
            self._rev_repos(repos, repo_settings, repo_arguments)

    def _get_arguments(self, arguments):
        raise NotImplementedError

    def _open_repos(self, repo_settings, arguments):
        raise NotImplementedError

    def _open_resolved_repos(self, repo_settings, arguments):
        raise NotImplementedError

    def _save_repos(self, repos, repo_settings, arguments):
        raise NotImplementedError

    def _list_repos(self, resolved_repos, repo_settings, arguments):
        for rr in resolved_repos:
            Console.print(str(rr))

    @staticmethod
    def __verify_source_key(repo_settings, key):
        if not key in repo_settings.sources:
            Console.error("Source key " + key + " was not found in sources.  Not adding.")
            return False

        return True

    def _add_repo(self, repos, repo_settings, arguments):
        source_key = arguments.source_key.upper()
        local_path = arguments.repo_local_path

        if not RepoCommandBase.__verify_source_key(repo_settings, source_key):
            return

        replace = arguments.replace

        if arguments.branch:
            repos.add(repo_path=local_path, src_key=source_key, branch=arguments.branch, replace=replace)
        elif arguments.revision:
            repos.add(repo_path=local_path, src_key=source_key, revision=arguments.revision, replace=replace)
        elif arguments.tag:
            repos.add(repo_path=local_path, src_key=source_key, tag=arguments.tag, replace=replace)
        else:
            repos.add(repo_path=local_path, src_key=source_key, replace=replace)

        self._save_repos(repos, repo_settings, arguments)

    @staticmethod
    def __find_relevant_repos(repos, resolved_repos, arguments, require_key_or_source):
        repo_key = arguments.repo_local_path
        source_key = arguments.source_key

        if not repo_key and not source_key:
            if require_key_or_source:
                Console.error("Either a source key or repo path must be specified.")
                return []

            return resolved_repos

        relevant = []

        if repo_key:
            if repo_key in repos:
                relevant = [repo_key]
            else:
                Console.warning("Repo could not be found: " + repo_key)

        if source_key:
            for rr in resolved_repos:
                if source_key == rr.src_key:
                    relevant.append(rr.repo_key)

            if not relevant:
                Console.warning("Could not find any repos with source key: " + source_key)

        if not relevant:
            return []

        resolved_relevant = []

        for rr in resolved_repos:
            for key in relevant:
                if rr.repo_key == key:
                    resolved_relevant.append(rr)

        return resolved_relevant

    def _remove_repo(self, repos, resolved_repos, repo_settings, arguments):
        removal_list = RepoCommandBase.__find_relevant_repos(repos, resolved_repos, arguments, True)

        if not removal_list:
            Console.warning("Could not find any repos to remove matching inputs.  Nothing removed.")
            return

        for rr in removal_list:
            Console.print("Removing: " + str(rr))

            repos.remove(rr.repo_key)

            if arguments.clean:
                full_path = rr.full_repo_path

                Console.print("Cleaning: " + full_path)

                if full_path.is_dir():
                    rmtree(full_path)

        self._save_repos(repos, repo_settings, arguments)

    def _freeze_repos(self, repos, resolved_repos, repo_settings, arguments):
        freeze_list = RepoCommandBase.__find_relevant_repos(repos, resolved_repos, arguments, False)

        if not freeze_list:
            return

        for rr in freeze_list:
            handler = rr.handler

            current_tags = handler.get_latest_tags()
            current_rev = handler.get_current_revision()

            if current_tags:
                tag = current_tags[0]
                Console.print("Setting " + rr.repo_key + " to tag " + tag)
                rr.set_tag(tag)
            elif current_rev:
                Console.print("Setting " + rr.repo_key + " to revision " + current_rev)
                rr.set_revision(current_rev)
            else:
                Console.warning("Could not retrieve current revision.  Has " + rr.repo_key + " been pulled?")

        self._save_repos(repos, repo_settings, arguments)

    def _unfreeze_repos(self, repos, resolved_repos, repo_settings, arguments):
        unfreeze_list = RepoCommandBase.__find_relevant_repos(repos, resolved_repos, arguments, False)

        if not unfreeze_list:
            return

        for rr in unfreeze_list:
            Console.print("Setting " + rr.repo_key + " to most recent revision (tip).")
            rr.set_tip()

        self._save_repos(repos, repo_settings, arguments)

        if unfreeze_list:
            Console.print("Repos have been modified.  Run 'update' to get the new contents.")

    def _upgrade_repos(self, repos, resolved_repos, repo_settings, arguments):
        upgrade_list = RepoCommandBase.__find_relevant_repos(repos, resolved_repos, arguments, False)

        if not upgrade_list:
            return

        for rr in upgrade_list:
            handler = rr.handler
            current_tags = handler.get_current_tags()
            latest_tags = handler.get_latest_tags()
            current_rev = handler.get_current_revision()

            if latest_tags:
                if current_tags and any(x in current_tags for x in latest_tags):
                    if not arguments.check:
                        Console.print(rr.repo_key + " is already at the latest version: " + ",".join(current_tags))
                else:
                    if not arguments.check:
                        tag = latest_tags[0]
                        Console.print("Upgrading " + rr.repo_key + " to tag " + tag + ".")
                        rr.set_tag(tag)
                    else:
                        if current_tags:
                            rev = ",".join(current_tags)
                        else:
                            rev = current_rev

                        Console.print(rr.repo_key + " may be upgraded from " + rev + " to " + ",".join(latest_tags) + ".")
            else:
                Console.warning("No tags are available for " + rr.repo_key + ".  Has it been pulled and tagged?")

        if arguments.check:
            return

        self._save_repos(repos, repo_settings, arguments)

        if upgrade_list:
            Console.print("Repos have been modified.  Run 'update' to get the new contents.")

    def _rev_repos(self, repos, resolved_repos, repo_settings, arguments):
        rev_list = RepoCommandBase.__find_relevant_repos(repos, resolved_repos, arguments, True)

        if not rev_list:
            return

        for rr in rev_list:
            if arguments.tip:
                Console.print("Setting " + rr.repo_key + " to most recent revision (tip).")
                rr.set_tip()
            elif arguments.revision:
                Console.print("Setting " + rr.repo_key + " to revision: " + arguments.revision)
                rr.set_revision(arguments.revision)
            elif arguments.branch:
                Console.print("Setting " + rr.repo_key + " to branch: " + arguments.branch)
                rr.set_branch(arguments.branch)
            elif arguments.tag:
                Console.print("Setting " + rr.repo_key + " to tag: " + arguments.tag)
                rr.set_tag(arguments.tag)

        self._save_repos(repos, repo_settings, arguments)

        if rev_list:
            Console.print("Repos have been modified.  Run 'update' to get the new contents.")





