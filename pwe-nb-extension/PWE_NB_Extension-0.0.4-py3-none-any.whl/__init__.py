from .helper import ASPRules
from PW_explorer.run_clingo import run_clingo
from PW_explorer.run_dlv import run_dlv
from PW_explorer.meta_data_parser import parse_meta_data

import notebook
import shutil
import IPython
from IPython.core import magic_arguments
from IPython.core.magic import (
    line_magic,
    line_cell_magic,
    Magics,
    magics_class,
    needs_local_scope,
)
import os

PROLOG_CODEMIRROR_MODE_SOURCE_LOCATION = 'Prolog-Codemirror-Mode/prolog'


@magics_class
class PWENBMagics(Magics):

    def load_lines(self, v):
        v = PWENBMagics.clean_fname(v)
        lines = []
        if os.path.exists(v):
            with open(v, 'r') as f:
                lines = f.read().splitlines()
        elif v in self.shell.user_global_ns:
            temp = self.shell.user_global_ns[v]
            if isinstance(temp, list):
                lines = temp
            elif isinstance(temp, str):
                lines = temp.splitlines()
        return lines

    def save_lines(self, lines, loc):

        loc = PWENBMagics.clean_fname(loc)

        def is_a_valid_textfile_name(loc: str):
            return loc.find('.') != -1

        if is_a_valid_textfile_name(loc):
            with open(loc, 'w') as f:
                if isinstance(lines, list):
                    f.write("\n".join(lines))
                elif isinstance(lines, str):
                    f.write(lines)
        else:
            self.__save_to_ipython_global_ns__(ASPRules(lines), loc)

    def __save_to_ipython_global_ns__(self, data, variable_name):
        self.shell.user_global_ns[variable_name] = data

    def __display_usage_error__(self, err_msg):
        self.shell.show_usage_error(err_msg)

    @staticmethod
    def clean_fname(fname: str):
        return fname.strip('\"').strip("\'")

    @line_cell_magic
    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-l', '--loadfrom', nargs='+', type=str, default=[],
                              help='List the variables in the namespace and the filepaths to load ASP rules from. '
                                   'In case of filepaths with spaces, use "filepath" .')
    @magic_arguments.argument('-s', '--saveto', type=str, default=None,
                              help='The filepath or variable name to save the output of the ASP reasoner to.')
    @magic_arguments.argument('--save_meta_data_to', type=str, default=None,
                              help='The variable name to save the extracted meta data to.')
    @magic_arguments.argument('-n', '--num_solutions', type=int, default=0,
                              help='Specify the maximum number of PWs to generate. Default: 0 i.e. generate all PWs.')
    @magic_arguments.argument('-lci', '--load_combined_input_to', type=str, default=None,
                              help='Specify the filepath or variable to save the combined input to.')
    @magic_arguments.defaults(display_input=True)
    @magic_arguments.argument('--display_input', dest='display_input', action='store_true',
                              help='Include to display the combined input. Displayed by default.')
    @magic_arguments.argument('--donot-display_input', dest='display_input', action='store_false',
                              help='Include to skip displaying the combined input.')
    @magic_arguments.defaults(display_output=True)
    @magic_arguments.argument('--display_output', dest='display_output', action='store_true',
                              help='Include to display the output of the ASP Reasoner. True by default.')
    @magic_arguments.argument('--donot-display_output', dest='display_output', action='store_false',
                              help='Include to skip displaying the output of the ASP reasoner.')
    @magic_arguments.defaults(run=True)
    @magic_arguments.argument('--run', dest='run', action='store_true',
                              help='Include to run the rules and generate the PWs. True by default.')
    @magic_arguments.argument('--donot-run', dest='run', action='store_false',
                              help='Include to skip running the ASP reasoner.')
    @magic_arguments.argument('-exp', '--experiment_name', type=str, default=None,
                              help='Save the various artifacts like combined rule set, extracted meta data and output '
                                   'of the ASP reasoner as a dict to a local variable. '
                                   'Provide the name of this variable')
    def clingo(self, line='', cell=None, local_ns=None):

        args = magic_arguments.parse_argstring(self.clingo, line)
        self.run_asp(args, line, cell, 'clingo', local_ns)

    @line_cell_magic
    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-l', '--loadfrom', nargs='+', type=str, default=[],
                              help='List the variables in the namespace and the filepaths to load ASP rules from. '
                                   'In case of filepaths with spaces, use "filepath" .')
    @magic_arguments.argument('-s', '--saveto', type=str, default=None,
                              help='The filepath or variable name to save the output of the ASP reasoner to.')
    @magic_arguments.argument('--save_meta_data_to', type=str, default=None,
                              help='The variable name to save the extracted meta data to.')
    @magic_arguments.argument('-n', '--num_solutions', type=int, default=0,
                              help='Specify the maximum number of PWs to generate. Default: 0 i.e. generate all PWs.')
    @magic_arguments.argument('-lci', '--load_combined_input_to', type=str, default=None,
                              help='Specify the filepath or variable to save the combined input to.')
    @magic_arguments.defaults(display_input=True)
    @magic_arguments.argument('--display_input', dest='display_input', action='store_true',
                              help='Include to display the combined input. Displayed by default.')
    @magic_arguments.argument('--donot-display_input', dest='display_input', action='store_false',
                              help='Include to skip displaying the combined input.')
    @magic_arguments.defaults(display_output=True)
    @magic_arguments.argument('--display_output', dest='display_output', action='store_true',
                              help='Include to display the output of the ASP Reasoner. True by default.')
    @magic_arguments.argument('--donot-display_output', dest='display_output', action='store_false',
                              help='Include to skip displaying the output of the ASP reasoner.')
    @magic_arguments.defaults(run=True)
    @magic_arguments.argument('--run', dest='run', action='store_true',
                              help='Include to run the rules and generate the PWs. True by default.')
    @magic_arguments.argument('--donot-run', dest='run', action='store_false',
                              help='Include to skip running the ASP reasoner.')
    @magic_arguments.argument('-exp', '--experiment_name', type=str, default=None,
                              help='Save the various artifacts like combined rule set, extracted meta data and output '
                                   'of the ASP reasoner as a dict to a local variable. '
                                   'Provide the name of this variable')
    @magic_arguments.argument('-wfs', dest='wfs', action='store_true', default=False,
                              help='Include to run the WFS mode in DLV.')
    def dlv(self, line='', cell=None, local_ns=None):

        args = magic_arguments.parse_argstring(self.dlv, line)
        self.run_asp(args, line, cell, 'dlv', local_ns)

    def run_asp(self, args, line='', cell=None, reasoner='clingo', local_ns=None):

        output = {}
        asp_program = []
        if args.loadfrom:
            for v in args.loadfrom:
                asp_program += self.load_lines(v)
        if cell:
            asp_program += cell.splitlines()

        if args.load_combined_input_to:
            self.save_lines(asp_program, args.load_combined_input_to)

        if args.display_input:
            print("Input:")
            display(ASPRules(asp_program))

        output['asp_rules'] = ASPRules(asp_program)
        if not args.run: # To avoid running it twice redundantly
            output['meta_data'] = parse_meta_data(asp_program)

        if args.save_meta_data_to:
            self.__save_to_ipython_global_ns__(output['meta_data'], args.save_meta_data_to)

        if args.run:
            if reasoner == 'dlv':
                asp_soln, md = run_dlv(asp_program, args.num_solutions, args.wfs)
            elif reasoner == 'clingo':
                asp_soln, md = run_clingo(asp_program, args.num_solutions)
            else:
                self.__display_usage_error__('Reasoner not recognized')
                return

            if args.display_output:
                # TODO Add a filter option for display purposes
                print("Output:")
                display(ASPRules("\n".join(asp_soln)))

            if args.saveto:
                self.save_lines(asp_soln, args.saveto)

            output['asp_soln'] = ASPRules(asp_soln)
            output['meta_data'] = md

        if args.experiment_name:
            self.__save_to_ipython_global_ns__(output, args.experiment_name)

    @line_magic
    @needs_local_scope
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('fnames', nargs='+', type=str, default=[])
    @magic_arguments.argument('-r', '--reasoner', type=str, choices=['clingo', 'dlv'], default='clingo')
    @magic_arguments.defaults(edit=False)
    @magic_arguments.argument('-e', '--edit', dest='edit', action='store_true', help='Only works when one file is provided')
    @magic_arguments.argument('-no-e', '--no-edit', dest='edit', action='store_false')
    def asp_loadfiles(self, line='', local_ns=None):
        args = magic_arguments.parse_argstring(self.asp_loadfiles, line)
        if not args.fnames:
            print("No filenames provided")
            return
        code_lines = []
        for fname in args.fnames:
            code_lines.extend(self.load_lines(fname))
        options = []
        options.append('--run')
        if args.edit:
            if len(args.fnames) == 1:
                options.append('--load_combined_input_to {}'.format(args.fnames[0]))
            else:
                self.__display_usage_error__('Edit functionality only works when loading a single file or variable')
        contents = '%%{} {}\n%asp_loadfiles {}\n\n{}'.format(
            args.reasoner, " ".join(options), line, "\n".join(code_lines))
        self.shell.set_next_input(contents, replace=True)


def load_prolog_js_files():
    this_dir, this_filename = os.path.split(__file__)
    codemirror_modes_location = os.path.join(notebook.DEFAULT_STATIC_FILES_PATH, 'components', 'codemirror', 'mode')
    codemirror_prolog_dest_location = '{}/prolog/'.format(codemirror_modes_location)
    os.makedirs(codemirror_prolog_dest_location, exist_ok=True)

    DATA_PATH = os.path.join(this_dir, PROLOG_CODEMIRROR_MODE_SOURCE_LOCATION)
    for fname in os.listdir(DATA_PATH):
        shutil.copy2(os.path.join(DATA_PATH, fname), codemirror_prolog_dest_location)


def load_ipython_extension(ipython):
    try:
        load_prolog_js_files()
        js = "IPython.CodeCell.options_default.highlight_modes['prolog'] = {'reg':[/^%%(clingo|dlv)/]};"
        IPython.core.display.display_javascript(js, raw=True)
    except Exception as e:
        print("Failed to copy prolog codemirror files with error:\n{}".format(e))
    finally:
        ipython.register_magics(PWENBMagics)
