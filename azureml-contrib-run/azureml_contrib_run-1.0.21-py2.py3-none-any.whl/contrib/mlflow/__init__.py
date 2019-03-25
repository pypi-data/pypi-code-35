# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Monkeypatch and add Azure tracking functionality to MLFlow."""

import logging
import os
import re
import uuid

import azureml
import mlflow
from mlflow.tracking.utils import get_tracking_uri
from mlflow.exceptions import MlflowException

from azureml.exceptions import RunEnvironmentException
from azureml.core import Run
from azureml.core.authentication import ArmTokenAuthentication, AzureMLTokenAuthentication

from azureml.contrib.mlflow.store import _MLFLOW_RUN_ID_ENV_VAR

from . import store
from . import artifact_repo
from azureml.contrib.run._version import VERSION
from six.moves.urllib import parse

logger = logging.getLogger(__name__)

__version__ = VERSION

_IS_REMOTE = "is-remote"
_REGION = "region"
_SUB_ID = "sub-id"
_RES_GRP = "res-grp"
_WS_NAME = "ws-name"
_AUTH_HEAD = "auth-head"
_AUTH_TYPE = "auth-type"
_TRUE_QUERY_VALUE = "True"

_TOKEN_PREFIX = "Bearer "


def _azure_uri_decomp(path):
    """
    Parse a URI into a dictionary.

    The URI contains the scope information for the workspace, and possible the experiment and run.
    """
    regex = "/history\\/v1.0" \
        "\\/subscriptions\\/(.*)" \
        "\\/resourceGroups\\/(.*)" \
        "\\/providers\\/Microsoft.MachineLearningServices" \
        "\\/workspaces\\/(.*)"

    pattern = re.compile(regex)
    mo = pattern.match(path)

    ret = {}
    ret[_SUB_ID] = mo.group(1)
    ret[_RES_GRP] = mo.group(2)
    ret[_WS_NAME] = mo.group(3)

    return ret


class _AzureMLStoreLoader(object):
    _azure_uri_to_store = {}

    @classmethod
    def _load_azureml_store(cls, store_uri):
        # cache the Azure workspace object
        parsed_url = parse.urlparse(store_uri)
        #  Check if the URL is a test or prod AML URL
        queries = parse.parse_qs(parsed_url.query)
        if store_uri in cls._azure_uri_to_store:
            return cls._azure_uri_to_store[store_uri]
        elif _IS_REMOTE in queries and queries[_IS_REMOTE][0] == _TRUE_QUERY_VALUE:
            try:
                run = Run.get_context()
            except RunEnvironmentException as run_env_exception:
                raise MlflowException(
                    "AzureMlflow tracking URI was set to remote but there was a failure in loading the run.")
            else:
                amlflow_store = store.AzureMLflowStore(
                    workspace=run.experiment.workspace)
                experiment_id = amlflow_store._exp_name_to_id.get(run.experiment.name)
                experiment = None if experiment_id is None else amlflow_store._exp_id_to_exp[experiment_id]
                if experiment is None:
                    exp_id = amlflow_store._get_next_exp_id()
                    amlflow_store._exp_id_to_exp[exp_id] = experiment
                    amlflow_store._name_to_exp_id[run.experiment.name] = exp_id

                cls._azure_uri_to_store[store_uri] = amlflow_store
                mlflow.set_experiment(run.experiment.name)
        else:
            parsed_path = _azure_uri_decomp(parsed_url.path)
            subscription_id = parsed_path[_SUB_ID]
            resource_group_name = parsed_path[_RES_GRP]
            workspace_name = parsed_path[_WS_NAME]

            if _AUTH_HEAD not in queries:
                auth = None
            else:
                if queries[_AUTH_TYPE] == AzureMLTokenAuthentication.__class__.__name__:
                    auth = AzureMLTokenAuthentication(
                        queries[_AUTH_HEAD],
                        host=parsed_url.netloc,
                        subscription_id=subscription_id,
                        resource_group_name=resource_group_name,
                        workspace_name=workspace_name,
                    )
                else:
                    auth = ArmTokenAuthentication(queries[_AUTH_HEAD])

            # TODO: Should we share Workspace if one is available? This would
            # also solve auth in many cases
            workspace = azureml.core.Workspace(subscription_id=subscription_id,
                                               resource_group=resource_group_name,
                                               workspace_name=workspace_name,
                                               auth=auth)

            cls._azure_uri_to_store[store_uri] = store.AzureMLflowStore(
                workspace=workspace)

        return cls._azure_uri_to_store[store_uri]


def _is_azureml_uri(store_uri):
    parsed_url = parse.urlparse(store_uri)
    #  Check if the URL is a test or prod AML URL
    return _is_azureml_host(parsed_url.netloc)


def _get_azureml_store(store_uri):
    return _AzureMLStoreLoader._load_azureml_store(store_uri)


def _new_init_decorator(orig_init):
    """
    Decorate and return a method which calls the original method, then apply modifications.

    This is used to patch MlflowClient.__init__.
    """
    def new_init(self, tracking_uri=None, *args, **kwargs):
        """
        Create constructor for MlflowClient monkeypatch.

        New __init__ for MlflowClient which detects if the tracking URI is Azure,
        and if it is, sets a different store to be our custom AzureMLflowStore.

        If the store already exists for this URI or workspace, then we'll reuse
        the same store instead of creating a new one. This is important so that
        """
        tracking_uri = tracking_uri if tracking_uri is not None else get_tracking_uri()
        if _is_azureml_uri(tracking_uri):
            self.tracking_uri = tracking_uri
            self.store = _get_azureml_store(self.tracking_uri)
        else:
            orig_init(self, tracking_uri, *args, **kwargs)

    return new_init


def _is_azureml_host(netloc):
    try:
        netloc_without_region = netloc.split(".", 1)[1]
        return netloc_without_region in ["experiments.azureml-test.net", "experiments.azureml.net"]
    except Exception as e:
        return False


def _new_from_artifact_uri_decorator(orig_from_artifact_uri, *args, **kwargs):
    """
    Decorate to monkeypatch ArtifactRepository.from_artifact_uri.

    Decorator which returns a method which calls the original method, then applies
    modifications. This is used to patch ArtifactRepository.from_artifact_uri.
    """
    def new_from_artifact_uri(artifact_uri, store, *args, **kwargs):
        parsed_url = parse.urlparse(artifact_uri)

        if _is_azureml_host(parsed_url.netloc):
            # return our custom store for azure URIs
            return artifact_repo.AzureMLflowArtifactRepository(
                artifact_uri,
                store)
        else:
            return orig_from_artifact_uri(artifact_uri, store)

    return new_from_artifact_uri


# monkeypatch
mlflow.tracking.MlflowClient.__init__ = _new_init_decorator(mlflow.tracking.MlflowClient.__init__)
mlflow.store.artifact_repo.ArtifactRepository.from_artifact_uri = _new_from_artifact_uri_decorator(
    mlflow.store.artifact_repo.ArtifactRepository.from_artifact_uri)

# TODO: remove this once pull request into workspace goes through
# this function is an addenum on workspace which allows us to retrieve a URI pointing to
# the workspace, with optionally an experiment name and run id in the URI as well, as
# well as the authentication token if requested


def _get_mlflow_tracking_uri(self, with_auth=True, exp_name=None, run_id=None):
    """
    Retrieve Azure URI from Workspace for use in AzureMLflow.

    Return a URI identifying the workspace, with optionally the auth header embeded
    as a query string within the URI as well. The authentication header does not include
    the "Bearer " prefix. Additionally, the URI will also contain experiment and run
    names and IDs if specified while calling this function.

    :return: Returns the URI pointing to this workspace, with the auth query paramter if
    with_auth is True.
    :rtype: str
    """
    queries = []
    if with_auth:
        auth = self._auth_object
        header = auth.get_authentication_header()
        token = header["Authorization"][len(_TOKEN_PREFIX):]
        queries.append("auth_type=" + auth.__class__.__name__)
        queries.append("auth=" + token)

    service_location = parse.urlparse(self.service_context._get_run_history_url()).netloc

    return "azureml://{}/history/v1.0{}{}{}?{}".format(
        service_location,
        self.service_context._get_workspace_scope(),
        exp_name if exp_name is not None else "",
        run_id if run_id is not None else "",
        "?" + "&".join(queries) if queries else "")


azureml.core.workspace.Workspace.get_mlflow_tracking_uri = _get_mlflow_tracking_uri
try:
    aml_run = Run.get_context(allow_offline=False)
except RunEnvironmentException as run_env_exception:
    logger.warning("Could not load a Run from the current context, not setting the mlflow tracking information")
else:
    mlflow.set_tracking_uri(aml_run._client.run.get_cluster_url().replace(
        "https://", "azureml://") + "?is-remote=True")
    os.environ[_MLFLOW_RUN_ID_ENV_VAR] = uuid.uuid4().hex
    mlflow.set_experiment(aml_run.experiment.name)
