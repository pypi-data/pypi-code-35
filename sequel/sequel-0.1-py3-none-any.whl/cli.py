import logging
from pathlib import Path

import click

from sequel import __dist__

log = logging.getLogger(__name__)


@click.group(name=__dist__.project_name)
@click.version_option(version=__dist__.version)
@click.option('--debug', default=False, is_flag=True,
              help='Maximize verbosity for debugging.')
def main(debug):
    logging.basicConfig(level=logging.WARNING)
    if debug:  # noqa
        logging.basicConfig(level=logging.DEBUG)


@main.command()
@click.option('--graph', default=None,
              help='Specify the graph name to run.')
@click.argument('graph_file')
def play(graph_file, graph):
    """Build a job graph from a module then resolve its callable nodes."""
    from sequel import graphes

    _ = load_module(graph_file)

    try:
        graph = graphes[graph]
    except KeyError:
        if len(graphes) == 1:
            graph = next(iter(graphes.values()))
        else:
            raise click.BadArgumentUsage('You must specify a graph.')

    graph.execute()


def load_module(path, module_id=None):
    import importlib.util
    import importlib.machinery

    module_id = module_id or Path(path).name

    spec = importlib.util.spec_from_file_location(module_id, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
