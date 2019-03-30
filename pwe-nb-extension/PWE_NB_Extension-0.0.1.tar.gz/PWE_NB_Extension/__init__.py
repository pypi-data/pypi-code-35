from PW_explorer.nb_helper import ASPRules
from PW_explorer.run_clingo import run_clingo

import notebook
import shutil
import IPython
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, line_cell_magic, Magics, magics_class
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

    @staticmethod
    def clean_fname(fname: str):
        return fname.strip('\"').strip("\'")

    @line_cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-l', '--loadfrom', nargs='+', type=str, default=[])
    @magic_arguments.argument('-s', '--saveto', type=str, default=None)
    @magic_arguments.argument('--save_meta_data_to', type=str, default=None)
    @magic_arguments.argument('-n', '--num_solutions', type=int, default=0)
    @magic_arguments.argument('-lci', '--load_combined_input_to', type=str, default=None)
    @magic_arguments.defaults(display_input=True)
    @magic_arguments.argument('--display_input', dest='display_input', action='store_true')
    @magic_arguments.argument('--donot-display_input', dest='display_input', action='store_false')
    @magic_arguments.defaults(display_output=True)
    @magic_arguments.argument('--display_output', dest='display_output', action='store_true')
    @magic_arguments.argument('--donot-display_output', dest='display_output', action='store_false')
    @magic_arguments.defaults(run=True)
    @magic_arguments.argument('--run', dest='run', action='store_true')
    @magic_arguments.argument('--donot-run', dest='run', action='store_false')
    @magic_arguments.argument('-exp', '--experiment_name', type=str, default=None)
    def clingo(self, line='', cell=None):

        output = {}
        args = magic_arguments.parse_argstring(self.clingo, line)
        clingo_program = []
        if args.loadfrom:
            for v in args.loadfrom:
                clingo_program += self.load_lines(v)
        if cell:
            clingo_program += cell.splitlines()

        if args.load_combined_input_to:
            self.save_lines(clingo_program, args.load_combined_input_to)

        if args.display_input:
            print("Clingo Program")
            display(ASPRules(clingo_program))

        output['asp_rules'] = ASPRules(clingo_program)

        if args.run:
            clingo_soln, md = run_clingo(clingo_program, args.num_solutions)
            if args.display_output:
                # TODO Add a filter option for display purposes
                print("Clingo Solution")
                display(ASPRules("\n".join(clingo_soln)))

            if args.saveto:
                self.save_lines(clingo_soln, args.saveto)

            if args.save_meta_data_to:
                self.__save_to_ipython_global_ns__(md, args.save_meta_data_to)

            output['asp_soln'] = ASPRules(clingo_soln)
            output['meta_data'] = md

        if args.experiment_name:
            self.__save_to_ipython_global_ns__(output, args.experiment_name)


    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('fnames', nargs='+', type=str, default=[])
    @magic_arguments.argument('-r', '--reasoner', type=str, choices=['clingo', 'dlv'], default='clingo')
    @magic_arguments.defaults(edit=False)
    @magic_arguments.argument('-e', '--edit', dest='edit', action='store_true', help='Only works when one file is provided')
    @magic_arguments.argument('-no-e', '--no-edit', dest='edit', action='store_false')
    def asp_loadfiles(self, line=''):
        args = magic_arguments.parse_argstring(self.asp_loadfiles, line)
        if not args.fnames:
            print("No filenames provided")
            return
        code_lines = []
        for fname in args.fnames:
            code_lines.extend(self.load_lines(fname))
        options = []
        options.append('--run')
        if args.edit and len(args.fnames) == 1:
            options.append('--load_combined_input_to {}'.format(args.fnames[0]))
        contents = '%%clingo {}\n%asp_loadfiles {}\n\n{}'.format(" ".join(options), line, "\n".join(code_lines))
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
        js = "IPython.CodeCell.options_default.highlight_modes['prolog'] = {'reg':[/^%%clingo/]};"
        IPython.core.display.display_javascript(js, raw=True)
    except Exception as e:
        print("Failed to copy prolog codemirror files with error:\n{}".format(e))
    finally:
        ipython.register_magics(PWENBMagics)
