from Arguments.ArgumentBase import ArgumentBase


class ImportArguments(ArgumentBase):
    IMPORT_COMMAND = "import"

    GUESTREPO_SOURCE = "guestrepos"
    SUBMODULES_SOURCE = "submodules"

    IMPORT_SOURCES = [GUESTREPO_SOURCE, SUBMODULES_SOURCE]

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.init_parser = self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(ImportArguments.IMPORT_COMMAND,
                                                 help="Import existing sources and repos from the base repo.")

        parser.add_argument("import_source", metavar='source', type=str, nargs=1,
                            help="Import data source.  Available sources: " + ", ".join(ImportArguments.IMPORT_SOURCES))

        parser.add_argument("--clean", action='store_true', dest="import_clean",
                            help="Remove source files from the repo.  All files will be discarded.")

        parser.add_argument("--clean-force", action='store_true', dest="import_clean_yes",
                            help="Clean but don't prompt to warn of file removal.")

        parser.add_argument("--import-force", action='store_true', dest="import_force",
                            help="Force importing of sources and repos replacing any values that already have "
                                 "existing keys.")

        return parser

    @property
    def source(self):
        return self.args.import_source[0]

    @property
    def clean(self):
        return self.args.import_clean or self.args.import_clean_yes

    @property
    def clean_yes(self):
        return self.args.import_clean_yes

    @property
    def force(self):
        return self.args.import_force
