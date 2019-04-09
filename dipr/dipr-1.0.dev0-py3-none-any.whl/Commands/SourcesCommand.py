
import string

from Protocols import ProtocolHelper
from Utilities.Console import Console

from Commands.DiprCommandBase import DiprCommandBase


class SourcesCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        repo = super()._open_repo(arguments)

        if not repo.is_initialized:
            Console.error("Repo " + str(repo.root_repo_path) + " is not initialized.")
            return

        src_arguments = arguments.sources_command

        command = src_arguments.command.lower()

        if command == "list":
            SourcesCommand.print_sources(repo, src_arguments)
            return

        if command == "add":
            SourcesCommand.add_source(repo, src_arguments)

        if command == "remove":
            SourcesCommand.remove_source(repo, src_arguments)

    @staticmethod
    def print_sources(repo, arguments):
        for s in repo.sources.values():
            Console.print(str(s))

    @staticmethod
    def __sanitize_key(key):
        valid_chars = string.ascii_uppercase + string.digits + "_" + "-"

        sanitized = ""

        for l in key:
            if l in valid_chars:
                sanitized += l
            else:
                sanitized += "_"

        return sanitized

    @staticmethod
    def add_source(repo, arguments):

        proto = arguments.protocol.upper()

        if proto not in ProtocolHelper.SUPPORTED_PROTOCOLS:
            Console.error("Protocol " + proto + " is not supported.")
            return

        replace = arguments.replace

        key = SourcesCommand.__sanitize_key(arguments.key.upper())

        if key in repo.sources and not replace:
            Console.error("Key " + key + " already exists.  Specify --replace to overwrite it.")
            return

        url = arguments.url

        Console.print("Adding Source: " + key + " => [" + proto + "] " + url)

        repo.sources.add(src_key=key, protocol=proto, url=url, values=arguments.remaining_args, replace=replace)

        repo.save_repo_files()

    @staticmethod
    def remove_source(repo, arguments):

        key = SourcesCommand.__sanitize_key(arguments.key.upper())

        if key not in repo.sources:
            Console.error("Key " + key + " is not in sources.")
            return

        preserve = arguments.preserve

        if not preserve:
            depends = repo.dependencies.get_entries_for_key(key)

            for d in depends:
                Console.print("Removing dependency: " + d.repo_key)
                repo.dependencies.remove(d.repo_key)

            subrepos = repo.subrepos.get_entries_for_key(key)

            for s in subrepos:
                Console.print("Removing subrepo: " + s.repo_key)
                repo.subrepos.remove(s.repo_key)

        Console.print("Removing source: " + key)

        repo.sources.remove(key)

        repo.save_repo_files()


