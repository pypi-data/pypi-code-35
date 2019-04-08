# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Add the plugin handlers for the tracking and the artifact stores."""

import logging

import azureml
import mlflow
from mlflow.exceptions import MlflowException

from azureml.exceptions import RunEnvironmentException
from azureml.core import Run

from . import store
from .utils import get_workspace_from_url, _IS_REMOTE, _TRUE_QUERY_VALUE, _TOKEN_PREFIX
from azureml.contrib.run._version import VERSION
from six.moves.urllib import parse

logger = logging.getLogger(__name__)

__version__ = VERSION


class _AzureMLStoreLoader(object):
    _azure_uri_to_store = {}

    @classmethod
    def _load_azureml_store(cls, store_uri, artifact_uri):
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
                    workspace=run.experiment.workspace, artifact_uri=artifact_uri)
                experiment_id = amlflow_store._exp_name_to_id.get(run.experiment.name)
                experiment = None if experiment_id is None else amlflow_store._exp_id_to_exp[experiment_id]
                if experiment is None:
                    exp_id = amlflow_store._get_next_exp_id()
                    amlflow_store._exp_id_to_exp[exp_id] = experiment
                    amlflow_store._name_to_exp_id[run.experiment.name] = exp_id

                cls._azure_uri_to_store[store_uri] = amlflow_store
                mlflow.set_experiment(run.experiment.name)
        else:
            workspace = get_workspace_from_url(parsed_url)
            cls._azure_uri_to_store[store_uri] = store.AzureMLflowStore(
                workspace=workspace, artifact_uri=artifact_uri)

        return cls._azure_uri_to_store[store_uri]


def azureml_store_builder(store_uri=None, artifact_uri=None):
    """Create or return an AzureMLflowStore."""
    from mlflow.tracking.utils import get_tracking_uri
    tracking_uri = store_uri if store_uri is not None else get_tracking_uri()
    return _AzureMLStoreLoader._load_azureml_store(tracking_uri, artifact_uri)


def azureml_artifacts_builder(artifact_uri=None):
    """Create an AzureMLflowArtifactRepository."""
    from .artifact_repo import AzureMLflowArtifactRepository
    return AzureMLflowArtifactRepository(artifact_uri)


def _get_mlflow_tracking_uri(self, with_auth=True):
    """
    Retrieve the tracking URI from Workspace for use in AzureMLflow.

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

    return "azureml://{}/history/v1.0{}?{}".format(
        service_location,
        self.service_context._get_workspace_scope(),
        "?" + "&".join(queries) if queries else "")


def _get_mlflow_artifacts_uri(self, exp_name, run_id, with_auth=True):
    """
    Retrieve the artifacts URI from Workspace for use in AzureMLflow.

    Return a URI identifying the workspace, with optionally the auth header embeded
    as a query string within the URI as well. The authentication header does not include
    the "Bearer " prefix. Additionally, the URI will also contain experiment and run
    names and IDs if specified while calling this function.

    :return: Returns the URI pointing to this workspace, experiment and run_id,
    with the auth query paramter if with_auth is True.
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

    return "azureml://{}/history/v1.0{}/experiments/{}/runs/{}/artifacts?{}".format(
        service_location,
        self.service_context._get_workspace_scope(),
        exp_name if exp_name is not None else "",
        run_id if run_id is not None else "",
        "?" + "&".join(queries) if queries else "")


azureml.core.workspace.Workspace.get_mlflow_tracking_uri = _get_mlflow_tracking_uri
azureml.core.workspace.Workspace.get_mlflow_artifacts_uri = _get_mlflow_artifacts_uri
