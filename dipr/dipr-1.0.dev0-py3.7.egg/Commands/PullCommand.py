
from Utilities.Console import Console

from Commands.DiprCommandBase import DiprCommandBase
from Protocols.ProtocolHelper import resolve_repo_handler


class PullCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        pull_args = arguments.pull_command

        repo_settings = super()._open_repo(arguments)

        if not repo_settings.is_initialized:
            Console.print("Repo is not initialized.")
            return

        if pull_args.depends_only or pull_args.all_repos:
            PullCommand.__execute_on_repo(repo_settings.resolved_dependencies, pull_args)

        if pull_args.subrepos_only or pull_args.all_repos:
            PullCommand.__execute_on_repo(repo_settings.resolved_subrepos, pull_args)

    @staticmethod
    def __execute_on_repo(all_repos, arguments):
        for repo in all_repos:
            proto = resolve_repo_handler(resolved_repo=repo)

            if proto is None:
                Console.warning("Could not resolve " + repo.src_key + " to a protocol.  Skipping.")
                continue

            Console.print("Pulling " + str(repo))
            Console.push_indent()
            proto.pull()
            Console.print("Complete.")
            Console.pop_indent()



