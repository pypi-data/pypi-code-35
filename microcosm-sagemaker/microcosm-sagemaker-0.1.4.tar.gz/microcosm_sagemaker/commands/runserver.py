"""
Main web service CLI

"""
from click import Path, command, option

from microcosm_sagemaker.app_hooks import AppHooks


@command()
@option(
    "--host",
    default="127.0.0.1",
    required=True,
)
@option(
    "--port",
    required=False,
)
@option(
    "--debug",
    default=False,
    required=True,
)
@option(
    "--artifact_path",
    type=Path(resolve_path=True),
    required=True,
    help="Path for reading artifacts, used for local testing",
)
def runserver_cli(host, port, debug, artifact_path):
    graph = AppHooks.create_serve_graph(debug=debug, artifact_path=artifact_path)

    graph.flask.run(
        host=host,
        port=port or graph.config.flask.port,
    )
