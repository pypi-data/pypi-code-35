from Utilities.Console import Console

from Arguments.ImportArguments import ImportArguments
from Commands.DiprCommandBase import DiprCommandBase

from Protocols.Hg.HgGuestRepoImporter import HgGuestRepoImporter
from Protocols.Git.GitSubmoduleImporter import GitSubmoduleImporter


class ImportCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        repo_settings = super()._open_repo(arguments)
        import_args = arguments.import_command

        if not repo_settings.is_initialized:
            Console.error("Repo " + repo_settings.root_repo_path + " is not initialized.")
            return

        source = import_args.source.lower()

        import_count = 0

        if source == ImportArguments.GUESTREPO_SOURCE:
            hg_importer = HgGuestRepoImporter(repo_settings.root_repo_path)
            import_count = hg_importer.import_into(repo_settings.sources, repo_settings.dependencies, import_args.force)

            if arguments.import_command.clean:
                hg_importer.clean(arguments.import_command.clean_yes)

        elif source == ImportArguments.SUBMODULES_SOURCE:
            sm_importer = GitSubmoduleImporter(repo_settings.root_repo_path)
            import_count = sm_importer.import_into(repo_settings.sources, repo_settings.dependencies, import_args.force)

            if arguments.import_command.clean:
                sm_importer.clean(arguments.import_command.clean_yes)

        else:
            Console.error("Import source must be one of: " + ", ".join(ImportArguments.IMPORT_SOURCES))

        if import_count > 0:
            repo_settings.resolve_repos(reset=True)
            repo_settings.save_repo_files()
            Console.print("Imported " + str(import_count) + " repos.")
        else:
            Console.print("No repos imported.")
