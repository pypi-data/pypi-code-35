"""
Main training CLI

"""
from json import load as json_load
from os import chdir

from click import Path, command, option

from microcosm_sagemaker.app_hooks import AppHooks
from microcosm_sagemaker.commands.evaluate import evaluate
from microcosm_sagemaker.constants import SagemakerPath
from microcosm_sagemaker.exceptions import raise_sagemaker_exception


@command()
@option(
    "--configuration",
    type=Path(resolve_path=True),
    required=False,
    help="Manual import of configuration file, used for local testing",
)
@option(
    "--input_path",
    type=Path(resolve_path=True),
    required=False,
    help="Path of the folder that houses the train/test datasets",
)
@option(
    "--artifact_path",
    type=Path(resolve_path=True),
    required=False,
    help="Path for outputting artifacts, used for local testing",
)
@option(
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
        model.fit(artifact_path)
    except Exception as e:
        raise_sagemaker_exception(e)

    if auto_evaluate:
        evaluate(input_path, artifact_path)
