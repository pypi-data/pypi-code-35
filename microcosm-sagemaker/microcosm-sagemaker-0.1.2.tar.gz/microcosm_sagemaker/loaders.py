"""
Loaders to inject SM parameters as microcosm configurations.

"""
from json import load as json_load, loads as json_loads
from os.path import join

from boto3 import client
from microcosm.config.model import Configuration
from microcosm.loaders.compose import merge
from microcosm.loaders.keys import expand_config

from microcosm_sagemaker.constants import CONFIGURATION_CACHE, SagemakerPath
from microcosm_sagemaker.s3 import S3Object


def load_from_hyperparameters(metadata):
    """
    Sagemaker only supports single-layer hyperparameters, so we use double underscores
    (__) to signify the delineation between nested dictionaries.  This mirrors the
    formatting of our ENV variables.  Note that these values are all strings by convention,
    so any end applications should.

    This configuration helper parses these into the underlying dictionary structure.

    """
    try:
        with open(SagemakerPath.HYPERPARAMETERS) as raw_file:
            return expand_config(
                json_load(raw_file),
                separator="__",
                skip_to=0,
            )

    except FileNotFoundError:
        return Configuration()


def load_from_s3(url):
    """
    Loads a S3 formatted url that points to a remote json file, and parses it into a local
    configuration variable.

    """
    def _load(metadata):
        s3 = client("s3")
        s3_object = S3Object.from_url(url)

        object = s3.get_object(Bucket=s3_object.bucket, Key=s3_object.key)
        return Configuration(json_loads(object["Body"].read()))

    return _load


def load_train_conventions(metadata):
    """
    Opinionated loader that:
    1. Reads all of the hyperparameters passed through by SageMaker
    2. Uses a special `base_configuration` key to read the given configuration from S3

    """
    configuration = load_from_hyperparameters(metadata)
    base_configuration_url = configuration.pop("base_configuration", None)

    if base_configuration_url:
        remote_configuration = load_from_s3(base_configuration_url)(metadata)

        # Locally specified hyperparameters should take precedence over the
        # base configuration
        configuration = merge([
            remote_configuration,
            configuration,
        ])

    return configuration


def load_model_artifact_config(artifact_path):
    """
    When we train a model, we freeze all of the current graph variables and store it alongside
    the artifact. Whenever we boot up the model again, we want to hydrate this from disk.

    """
    def _load_path(metadata):
        path = join(artifact_path, CONFIGURATION_CACHE)

        try:
            with open(path) as raw_file:
                return json_load(raw_file)
        except FileNotFoundError:
            return Configuration()

    return _load_path
