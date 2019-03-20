import inspect
import os
import sys
from itertools import dropwhile
from shutil import ignore_patterns

import parade
import six
from IPython import nbformat
from parade.command import ParadeCommand
from parade.core.task import ETLTask, SingleSourceETLTask
from parade.utils.misc import copytree

IGNORE = ignore_patterns('*.pyc', '.svn', '.git')

def get_function_body(func):
    source_lines = inspect.getsourcelines(func)[0]
    source_lines = dropwhile(lambda x: x.startswith('@'), source_lines)
    def_line = next(source_lines).strip()
    if def_line.startswith('def ') and def_line.endswith(':'):
        # Handle functions that are not one-liners
        first_line = next(source_lines)
        # Find the indentation of the first line
        indentation = len(first_line) - len(first_line.lstrip())
        return [first_line[indentation:]] + [line[indentation:] for line in source_lines]
    else:
        # Handle single line functions
        return [def_line.rsplit(':')[-1].strip()]


def get_imports(obj):
    source_lines = inspect.getsourcelines(sys.modules[obj.__module__])[0]
    source_lines = dropwhile(lambda x: x.startswith('@'), source_lines)
    import_lines = filter(lambda x: x.startswith('import ') or x.startswith('from '), source_lines)
    return list(import_lines)


class NotebookCommand(ParadeCommand):
    requires_workspace = True

    def run_internal(self, context, **kwargs):
        task_name = kwargs['task']
        NotebookCommand.init_jupyter(context)

        if task_name is None:
            os.system('jupyter notebook --ip=0.0.0.0 --allow-root')
            return

        task = context.get_task(task_name, task_class=ETLTask)
        import_lines = get_imports(task)
        if isinstance(task, SingleSourceETLTask):
            source = task.source
            if isinstance(source, six.string_types):
                body_lines = ['source = """{}"""\n'.format(source)]
            else:
                body_lines = ['source = {}\n'.format({'a': 1})]

            if task.is_source_query:
                body_lines.append('context.load_query(source, conn=\'{}\')\n'.format(task.source_conn))
            else:
                body_lines.append('context.load(source, conn=\'{}\')\n'.format(task.source_conn))

        else:
            body_lines = get_function_body(task.execute_internal)
            body_lines = list(map(lambda x: x.replace('return ', ''), body_lines))
        source_lines = import_lines + ['\n\n'] + body_lines

        notebook = nbformat.v4.new_notebook()
        cell = nbformat.v4.new_code_cell(source=source_lines)
        notebook.cells.append(cell)

        ipynb_path = os.path.join(context.workdir, '.jupyter', 'notebook', task.name + '.ipynb')
        with open(ipynb_path, 'wb') as f:
            ipy_content = nbformat.writes(notebook)
            f.write(ipy_content.encode())
            f.flush()

        os.system('jupyter notebook {}.ipynb'.format(task.name))


    @staticmethod
    def init_jupyter(context):
        jupyter_path = os.path.join(context.workdir, '.jupyter')
        NotebookCommand._init_jupyter(jupyter_path)
        # We need set PARADE_WORKSPACE since we'll head to notebook dir
        os.environ['PARADE_WORKSPACE'] = context.workdir
        os.chdir(os.path.join(jupyter_path, 'notebook'))

    @staticmethod
    def _init_jupyter(jupyter_path):
        if not os.path.exists(jupyter_path):
            jupyter_source_dir = os.path.join(parade.__path__[0], 'template', 'workspace', 'jupyter')
            copytree(jupyter_source_dir, jupyter_path, IGNORE)

        os.environ['JUPYTER_PATH'] = jupyter_path
        os.environ['IPYTHONDIR'] = os.path.join(jupyter_path, 'ipython')

    def short_desc(self):
        return 'start a jupyter notebook server with parade context or debug a specified task'

    def config_parser(self, parser):
        parser.add_argument('task', nargs='?', help='the task to debug in notebook')
