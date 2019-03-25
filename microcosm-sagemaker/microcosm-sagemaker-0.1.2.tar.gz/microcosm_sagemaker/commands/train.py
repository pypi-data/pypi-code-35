"""
Main training CLI

"""
from json import load as json_load
from os import chdir

import click

from microcosm_sagemaker.app_hooks import AppHooks
from microcosm_sagemaker.commands.evaluate import evaluate
from microcosm_sagemaker.constants import SagemakerPath
from microcosm_sagemaker.exceptions import handle_sagemaker_exception


@click.command()
@click.option(
    "--configuration",
    type=click.Path(resolve_path=True),
    required=False,
    help="Manual import of configuration file, used for local testing",
)
@click.option(
    "--input_path",
    type=click.Path(resolve_path=True),
    required=False,
    help="Path of the folder that houses the train/test datasets",
)
@click.option(
    "--artifact_path",
    type=click.Path(resolve_path=True),
    required=False,
    help="Path for outputting artifacts, used for local testing",
)
@click.option(
    "--auto_evaluate",
    type=bool,
    default=True,
    help="Whether to automatically evaluate after the training has completed",
)
def train_cli(configuration, input_path, artifact_path, auto_evaluate):
    if not artifact_path:
        artifact_path = SagemakerPath.MODEL
    if not input_path:
        input_path = SagemakerPath.INPUT

    if configuration:
        with open(configuration) as configuration_file:
            extra_config = json_load(configuration_file)
    else:
        extra_config = {}

    graph = AppHooks.create_train_graph(extra_config=extra_config)

    chdir(input_path)

    try:
        model = graph.active_bundle
        model.prefit(artifact_path)
        model.fit(artifact_path)
    except Exception as e:
        handle_sagemaker_exception(e)

    if auto_evaluate:
        evaluate(input_path, artifact_path)
