# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowStore** provides a class to read and record run metrics and artifacts on Azure via MLflow."""

import datetime
import uuid
import time
import logging
import os

import mlflow
from mlflow.protos import databricks_pb2
from mlflow.store.abstract_store import AbstractStore
from mlflow.exceptions import MlflowException
from mlflow.entities import Experiment, Param, Metric, RunTag, SourceType
from mlflow.entities import Run, RunInfo, RunStatus, ViewType, RunData

from azureml.core import Workspace
from azureml.core import Run as AMLRun
from azureml.core import Experiment as AMLExperiment
from azureml.core.authentication import AzureMLTokenAuthentication

from azureml._restclient.experiment_client import ExperimentClient
from azureml._restclient.run_client import RunClient
from azureml._restclient.metrics_client import MetricsClient
from azureml._restclient.contracts.utils import DATE_TIME_FORMAT
from azureml._restclient.models.create_run_dto import CreateRunDto
from azureml._restclient.models.created_from_dto import CreatedFromDto
from azureml.exceptions import RunEnvironmentException

from azureml.exceptions import SnapshotException

logger = logging.getLogger(__name__)

PARAM_PREFIX = "azureml.param."
_MLFLOW_RUN_ID_ENV_VAR = "MLFLOW_RUN_ID"


class AzureMLflowStore(AbstractStore):
    """Client for remote Azure Machine Learning tracking server."""

    def __init__(self, workspace=None):
        """
        Construct an AzureMLflowStore object.

        Initializes workspace settings and loads existing experiments.
        In MLflow stores, the default Experiment is created when calling the constructor,
        but this is not the case here.

        :param workspace: the Azure ML worskpace
        :type model_name: azureml.core.Workspace
        """
        self._exp_id_to_exp = {}  # types are {int: AzureMLflowExperiment}
        self._exp_name_to_id = {}  # types are {str: int}
        self._run_uuid_to_exp = {}  # types are {uuid: AzureMLflowExperiment}
        self._run_uuid_to_run_id = {}
        self._current_exp_id = 0

        # set workspace for azure ml purposes
        self.workspace = workspace if workspace else Workspace.from_config()

        # create experiments for all those existing on Azure
        self._load_azure_experiments()

    def _get_next_exp_id(self):
        self._current_exp_id += 1
        return self._current_exp_id

    def _get_aml_run_from_id(self, run_id):
        if run_id not in self._run_uuid_to_exp:
            return None
        experiment = self._run_uuid_to_exp[run_id]
        exp_client = ExperimentClient(self.workspace.service_context, experiment.name)
        runid = self._run_uuid_to_run_id[run_id]
        run_dto = exp_client.get_run(runid)
        return AMLRun(experiment.aml_exp, run_dto.run_id, _run_dto=run_dto)

    def _load_azure_experiments(self):
        """Load all the experiments created in the Azure Workspace."""
        # give unique incremental ID to every existing Azure experiment and store
        for name, exp in self.workspace.experiments.items():
            id = self._get_next_exp_id()
            self._exp_name_to_id[name] = id
            self._exp_id_to_exp[id] = _AzureMlflowExperiment.from_aml(id, exp)

    def list_experiments(self, view_type=ViewType.ACTIVE_ONLY):
        """
        Return a list of all the MLflow Experiments.

        :param view_type: Qualify requested type of experiments.
        :return: a list of Experiment objects stored in store for requested view.
        """
        # TODO: implement view_type
        exp_list = []
        for _, exp in self._exp_id_to_exp.items():
            exp_list.append(exp.mlflow_exp)
        return exp_list

    def create_experiment(self, name, artifact_location=None, _experiment_id=None):
        """
        Create a new experiment.

        If an experiment with the given name already exists, throws exception.
        Currently, create_experiment does not create an Azure experiment until a Run is started.
        Note: as Azure does not support experiments of name length only one character long, for
        the default experiment name of "0", we give it the default name on Azure of
        MLflow-Default-0.

        _experiment_id parameter only to be used internally by get_or_make_experiment()
        see get_or_make_experiment() for INFO

        :param name: Desired name for an experiment
        :param artifact_location: Base location for artifacts in runs. May be None.
        :return: experiment_id (integer) for the newly created experiment if successful, else None
        """
        # !! artifact_location is never used
        # ideally check that it's a valid Azure name here
        # otherwise will return an azureml type error (rather than MlflowException)
        if _experiment_id:
            assert _experiment_id not in self._exp_id_to_exp  # for internal use only

        if name is None or name == "":
            raise MlflowException("Invalid experiment name '%s'" %
                                  name, databricks_pb2.INVALID_PARAMETER_VALUE)

        # verify that name is new to both MLflow and Azure
        if name in self._exp_name_to_id:
            raise MlflowException("Experiment already exists with name '%s'" %
                                  name, databricks_pb2.INVALID_PARAMETER_VALUE)
        else:
            # mirror the default behavior of mlflow here, instead of creating a Default Experiment in __init__
            if name == "0":
                name = "MLflow-Default-0"

            # ID 0 is reserved for MLflow's default experiment ID
            id = _experiment_id if _experiment_id is not None else max(
                self._exp_id_to_exp or [0]) + 1
            self._exp_name_to_id[name] = id
            self._exp_id_to_exp[id] = _AzureMlflowExperiment(
                id, name, self.workspace)
            return id

    def get_experiment(self, experiment_id):
        """
        Fetch the experiment by ID from the backend store.

        Throws an exception if experiment is not found or permanently deleted.

        :param experiment_id: Integer id for the experiment
        :return: A single Experiment object if it exists, otherwise raises an Exception.
        """
        return self._get_mlflow_experiment(experiment_id)

    def get_experiment_by_name(self, name):
        """
        Fetch the experiment by name from the backend store.

        Returns None if no experiment exists with given name

        :param name: The experiment name.
        :return: :py:class:`mlflow.entities.Experiment`
        """
        if name in self._exp_name_to_id:
            experiment_id = self._exp_name_to_id[name]
        else:
            id = max(self._exp_id_to_exp or [0]) + 1
            experiment = _AzureMlflowExperiment(id, name, self.workspace)
            self._exp_id_to_exp[id] = experiment
            self._exp_name_to_id[name] = id
            experiment_id = id

        return self._get_mlflow_experiment(experiment_id)

    def get_or_make_experiment(self, experiment_id):
        """
        Fetch the experiment by ID from the backend store.

        Makes an experiment if not previously made whose name is the stringified experiment_id.
        Function only to be used internally by create_run()

        INFO: Ideally this function wouldn't exist as the store should have full say
        over an experiment ID's number. However, MLFlow does not require the creation
        of an experiment (as opposed to Azure ML). If the user doesn't explicitly set
        an experiment, MLflow calls create_run() with a default experiment ID (=0) without
        checking with the store whether that's a valid ID / whether the experiment already
        exists. In that case, it is then necessary to create an experiment with that particular
        default ID. (Same happens for user setting an environment variable for the experiment ID
        which is even worse.)

        :param experiment_id: Integer id for the experiment
        :return: A single Experiment object if it exists, otherwise raises an Exception.
        """
        if experiment_id not in self._exp_id_to_exp:
            logger.info("Experiment '%s' was not explicitly created before." %
                        experiment_id)
            self.create_experiment(name=str(experiment_id), _experiment_id=experiment_id)
            logger.info("Created experiment '%s'." %
                        self._exp_id_to_exp[experiment_id].name)
        return self._exp_id_to_exp[experiment_id]

    def delete_experiment(self, experiment_id):
        """
        Delete the experiment from the backend store.

        Deleted experiments can be restored untilpermanently deleted.
        This operation is not supported in Azure, and this change will not be propagated to Azure.

        :param experiment_id: Integer id for the experiment
        """
        raise MlflowException(
            "`delete_experiment` is not supported in with AzureML tracking.")

    def restore_experiment(self, experiment_id):
        """
        Restore deleted experiment unless it is permanently deleted.

        This operation is not supported in Azure, and this change will not be propagated to Azure.

        :param experiment_id: Integer id for the experiment
        """
        raise MlflowException(
            "`restore_experiment` is not supported in with AzureML tracking.")

    def rename_experiment(self, experiment_id, new_name):
        """
        Update an experiment's name. The new name must be unique.

        This operation is not supported in Azure, and this change will not be propagated to Azure.

        :param experiment_id: Integer id for the experiment
        """
        raise MlflowException(
            "`rename_experiment` is not supported with AzureML tracking.")

    def get_run(self, run_id):
        """
        Fetch the run from backend store.

        Raises exception if run doesn't exist.

        :param run_id: Unique identifier for the run
        :return: A single Run object if it exists, otherwise raises an Exception
        """
        return self._get_mlflow_run(run_id)

    def update_run_info(self, run_id, run_status, end_time):
        """
        Update the metadata of the specified run.

        :return: RunInfo describing the updated run.
        """
        return self._get_amlflow_run(run_id).update_run_info(run_status, end_time)

    def create_run(self, experiment_id, user_id, run_name, source_type, source_name,
                   entry_point_name, start_time, source_version, tags, parent_run_id):
        """
        Create a run under the specified experiment ID.

        Sets the run's status to "RUNNING" and the start time to the current time.

        The first time we create a run, we reset the authentication of the workspace to use
        AzureMLTokenAuthentication with the new run's configuration, so that the token refreshes
        itself.

        :param experiment_id: ID of the experiment for this run
        :param user_id: ID of the user launching this run
        :param source_type: Enum (integer) describing the source of the run
        :return: The created Run object
        """
        # needed because mlflow does not require explicit experiment creation before
        # create_run()
        experiment = self.get_or_make_experiment(experiment_id)

        if not experiment.is_active:
            raise MlflowException(
                "Could not create run under non-active experiment with ID %s."
                % experiment_id,
                databricks_pb2.INVALID_STATE)

        run_uuid = uuid.uuid4().hex

        _AzureMlflowRun.create(
            uuid=run_uuid,
            experiment=experiment,
            name=run_name,
            source_type=source_type,
            source_name=source_name,
            entry_point_name=entry_point_name,
            user_id=user_id,
            start_time=start_time,
            source_version=source_version,
            parent_run_id=parent_run_id
        )
        self._run_uuid_to_run_id[run_uuid] = run_uuid
        self._run_uuid_to_exp[run_uuid] = experiment

        # Refresh the store's workspace with the new auth token which can be requested with the new run.
        # Only do this once for each store/workspace, since the new auth token refreshes itself automatically.

        auth = self.workspace._auth_object
        if not isinstance(auth, AzureMLTokenAuthentication):
            aml_run = self._get_aml_run(run_uuid)
            auth_token = aml_run._run_dto.get('token', aml_run._client.run.get_token().token)
            auth_object = AzureMLTokenAuthentication.create(
                azureml_access_token=auth_token,
                expiry_time=None,
                host=aml_run._client.run.get_cluster_url(),
                subscription_id=self.workspace.subscription_id,
                resource_group_name=self.workspace.resource_group,
                workspace_name=self.workspace.name,
                experiment_name=experiment.name,
                run_id=run_uuid
            )
            self.workspace._auth = auth_object

            tags_dict = {tag.key: tag.value for tag in tags}
            self._get_aml_run(run_uuid).set_tags(tags_dict)

        return self._get_mlflow_run(run_uuid)

    def delete_run(self, run_id):
        """
        Delete a run.

        This operation is not supported in Azure, and this change will not be propagated to Azure.

        :param run_id:
        """
        raise MlflowException(
            "`delete_run` is not supported in with AzureML tracking.")

    def restore_run(self, run_id):
        """
        Restore a run.

        This operation is not supported in Azure, and this change will not be propagated to Azure.

        :param run_id:
        """
        raise MlflowException(
            "`restore_run` is not support in with AzureML tracking.")

    def log_metric(self, run_id, metric):
        """
        Log a metric for the specified run.

        :param run_id: String id for the run
        :param metric: Metric instance to log
        """
        self._get_amlflow_run(run_id).log(name=metric.key, value=metric.value)

    def log_param(self, run_id, param):
        """
        Log a param for the specified run.

        :param run_id: String id for the run
        :param param: Param instance to log
        """
        self._get_amlflow_run(run_id).log_param(name=param.key, value=param.value)

    def set_tag(self, run_id, tag):
        """
        Set a tag for the specified run.

        :param run_id: String id for the run
        :param tag: RunTag instance to set
        """
        self._get_amlflow_run(run_id).set_tag(key=tag.key, value=tag.value)

    def get_metric(self, run_id, metric_key):
        """
        Return the last logged value for a given metric.

        :param run_id: Unique identifier for run
        :param metric_key: Metric name within the run

        :return: A single float value for the given metric if logged, else None
        """
        return self._get_amlflow_run(run_id).get_metric(metric_key)

    def get_param(self, run_id, param_name):
        """
        Return the value of the specified parameter.

        :param run_id: Unique identifier for run
        :param param_name: Parameter name within the run

        :return: Value of the given parameter if logged, else None
        """
        return self._get_amlflow_run(run_id).get_param(param_name)

    def get_metric_history(self, run_id, metric_key):
        """
        Return all logged value for a given metric.

        :param run_id: Unique identifier for run
        :param metric_key: Metric name within the run

        :return: A list of float values logged for the give metric if logged, else empty list
        """
        return self._get_amlflow_run(run_id).get_metric_history(metric_key)

    def search_runs(self, experiment_ids, search_expressions, run_view_type):   # noqa
        """
        Return runs that match the given list of search expressions within the experiments.

        Given multiple search expressions, all these expressions are ANDed together for search.

        :param experiment_ids: List of experiment ids to scope the search
        :param search_expression: list of search expressions

        :return: A list of Run objects that satisfy the search expressions
        """
        # TODO: implement search functionality
        matches = []
        for id in experiment_ids:
            experiment = self._exp_id_to_exp.get(id)
            runs = experiment.aml_exp.get_runs()
            for run in runs:
                matches.append(_AzureMlflowRun(run.id, experiment).mlflow_run)
        return matches

    def list_run_infos(self, experiment_id, run_view_type):  # noqa
        """
        Return run information for runs which belong to the experiment_id.

        :param experiment_id: The experiment id which to search.

        :return: A list of RunInfo objects that satisfy the search expressions
        """
        experiment = self._exp_id_to_exp.get(experiment_id)
        runs = experiment.aml_exp.get_runs()
        infos = []
        for run in runs:
            infos.append(_AzureMlflowRun(run.id, experiment).mlflow_run.info)
        return infos

    def _get_amlflow_experiment(self, experiment_id):
        experiment = self._exp_id_to_exp.get(experiment_id)
        if experiment is None:
            raise MlflowException("Experiment '%s' does not exist." % experiment_id,
                                  databricks_pb2.RESOURCE_DOES_NOT_EXIST)
        return experiment

    def _get_mlflow_experiment(self, experiment_id):
        return self._get_amlflow_experiment(experiment_id).mlflow_exp

    def _get_aml_experiment(self, experiment_id):
        return self._get_amlflow_experiment(experiment_id).aml_exp

    def _get_amlflow_run(self, run_id):
        aml_run = self._get_aml_run_from_id(run_id)
        if aml_run is not None:
            experiment = self._run_uuid_to_exp[run_id]
            return _AzureMlflowRun(run_id, experiment, _aml_run=aml_run)
        else:
            try:
                aml_run = AMLRun.get_context(allow_offline=False)
            except RunEnvironmentException as e:
                raise MlflowException("Azure ML Run {} does not exist.".format(run_id),
                                      databricks_pb2.RESOURCE_DOES_NOT_EXIST)
            else:
                experiment_id = self._exp_name_to_id.get(aml_run.experiment.name)
                experiment = None if experiment_id is None else self._exp_id_to_exp[experiment_id]
                if experiment is None:
                    exp_id = self._get_next_exp_id()
                    self._exp_id_to_exp[exp_id] = experiment
                    self._name_to_exp_id[aml_run.experiment.name] = exp_id
                    experiment = _AzureMlflowExperiment.from_exp(exp_id, aml_run.experiment)

                created_from_dto = CreatedFromDto(type=SourceType.JOB,
                                                  location_type="ArtifactId",
                                                  location="remote")

                properties = {}
                properties["EntryPointName"] = ""
                properties["UserId"] = ""
                properties["CreatedBy"] = ""
                properties["LifeCycleStage"] = RunInfo.ACTIVE_LIFECYCLE

                create_run_dto = CreateRunDto(created_from=created_from_dto,
                                              properties=properties)

                run_client = aml_run._client.run
                run_dto = run_client.patch_run(create_run_dto)
                aml_run._internal_run_dto = run_dto

                self._run_uuid_to_run_id[run_id] = aml_run.id
                self._run_uuid_to_exp[run_id] = experiment
                mlflow.set_experiment(aml_run.experiment.name)
            return _AzureMlflowRun(run_id, experiment, run_id=aml_run.id, _aml_run=aml_run)

    def _get_mlflow_run(self, run_id):
        return self._get_amlflow_run(run_id).mlflow_run

    def _get_aml_run(self, run_id):
        return self._get_amlflow_run(run_id).aml_run


class _AzureMlflowExperiment():
    """Integrate experiments from MLFlow and Azure."""

    def __init__(self, id, name, workspace):
        """
        Construct an AzureMlflowExperiment.

        :param workspace: the Azure workspace in which to create experiment
        :type workspace: azureml.core.workspace.Workspace
        """
        self._id = id
        self._name = name
        self._workspace = workspace
        self._aml_exp = AMLExperiment(workspace=self.workspace, name=self.name)
        self._mlflow_exp = Experiment(
            self.id, self.name, self.workspace.location, Experiment.ACTIVE_LIFECYCLE)

    def location(self, run_id=None):
        # this translates into part of the artifact_uri for the Run as well as
        # initializes the ArtifactRepository, so it must include all information
        # about the whereabouts of the experiment
        #  TODO add container here, then set it on store. to avoid _get_or_start_run
        return self._workspace.get_mlflow_tracking_uri(
            with_auth=True,
            exp_name=self.name,
            run_id=run_id)

    @staticmethod
    def from_aml(id, aml_exp):
        return _AzureMlflowExperiment(id, aml_exp.name, aml_exp.workspace)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def workspace(self):
        return self._workspace

    @property
    def mlflow_exp(self):
        return self._mlflow_exp

    @property
    def aml_exp(self):
        return self._aml_exp

    @property
    def is_active(self):
        return self._mlflow_exp.lifecycle_stage == Experiment.ACTIVE_LIFECYCLE


class _AzureMlflowRun(object):
    """Integrate runs from MLFlow and Azure."""

    def __init__(self, uuid, experiment, run_id=None, _aml_run=None):
        """
        Construct an AzureMlflowRun object.

        :type experiment: AzureMlflowExperiment
        """
        self._uuid = uuid
        run_id = run_id if run_id is not None else uuid  # Assuming the run id is the uuid if not set

        self._aml_run = _aml_run if _aml_run is not None else AMLRun(experiment.aml_exp, run_id)

        self.container = self._aml_run._run_dto['data_container_id']
        run_dto_dict = self._aml_run._run_dto

        created_from = run_dto_dict.get("created_from")
        source_type = created_from["type"] if created_from is not None else SourceType.LOCAL
        source_version = created_from.get("location") if created_from is not None else ""
        source_name = run_dto_dict.get("script_name", "")

        start_time_utc = run_dto_dict["start_time_utc"]

        start_time = int(datetime.datetime.strptime(start_time_utc, DATE_TIME_FORMAT).timestamp())
        end_time_utc = run_dto_dict.get("end_time_utc")
        end_time = (None if end_time_utc is None else
                    int(datetime.datetime.strptime(end_time_utc, DATE_TIME_FORMAT).timestamp()))

        status = RunStatus.RUNNING if run_dto_dict["status"] == "Running" else -1

        # TODO This should be a mapping from status
        properties = run_dto_dict["properties"]
        entry_point_name = properties.get("EntryPointName")
        lifecycle_stage = properties.get("LifeCycleStage")
        user_id = properties.get("CreatedBy", "")

        # MLFlow handling
        run_info = RunInfo(run_uuid=self._uuid, experiment_id=experiment.id,
                           name=run_dto_dict.get("name", ""),
                           artifact_uri=experiment.location(run_id=self._uuid),
                           source_type=int(source_type), source_name=source_name,
                           entry_point_name=entry_point_name, user_id=user_id,
                           start_time=start_time, source_version=source_version,
                           status=status, lifecycle_stage=lifecycle_stage,
                           end_time=end_time)

        params = [
            Param(key[len(PARAM_PREFIX):], value) for key, value in properties.items() if PARAM_PREFIX in key
        ]
        metrics = [
            Metric(key, value, None) for key, value in self._aml_run.get_metrics().items()
        ]
        tags = [
            RunTag(key, value) for key, value in self._aml_run.get_tags().items()
        ]
        run_data = RunData(metrics=metrics, params=params, tags=tags)
        self._mlflow_run = Run(run_info=run_info, run_data=run_data)

    @classmethod
    def create(cls, uuid, experiment, source_type, source_name, entry_point_name,
               user_id, source_version, name=None, parent_run_id=None, start_time=None,
               status=RunStatus.RUNNING, lifecycle_stage=RunInfo.ACTIVE_LIFECYCLE):
        """Create an Azure Machine Learning run within an experiment for given run id."""
        logger.debug("Start time was set to {}, we ignore this and use the start event's start time".format(
            start_time))

        #  TODO make sure these values are in the correct location
        aml_experiment = experiment.aml_exp
        created_from_dto = CreatedFromDto(type=source_type, location_type="ArtifactId", location=source_version)

        #  TODO these should not be properties
        properties = {}
        properties["EntryPointName"] = entry_point_name
        properties["CreatedBy"] = user_id
        properties["LifeCycleStage"] = lifecycle_stage

        create_run_dto = CreateRunDto(created_from=created_from_dto,
                                      script_name=source_name,
                                      name=name,
                                      run_id=uuid,
                                      parent_run_id=parent_run_id,
                                      properties=properties)
        run_client = RunClient(aml_experiment.workspace.service_context, aml_experiment.name, uuid)
        run_dto = run_client.create_run(run_id=uuid, create_run_dto=create_run_dto)
        run_client.post_event_start()
        run_dto = run_client.get_run()

        run = AMLRun(aml_experiment, run_dto.run_id, _run_dto=run_dto)

        # also create a snapshot here, on the current directory, based on the source_* params
        try:
            snapshot_path = os.path.abspath(".")
            run.take_snapshot(snapshot_path)
        except SnapshotException as s_exception:
            logger.warning(s_exception)
            logger.warning("The working directory is too large; skipping Azure Run snapshot...")

        return cls(uuid, experiment, _aml_run=run)

    def update_run_info(self, run_status, end_time):
        """
        Update the metadata of the specified run.

        :return: RunInfo describing the updated run.
        """
        if not self.is_active:
            raise MlflowException('The run {} must be in an active lifecycle_stage.'
                                  .format(self._uuid))

        if run_status == RunStatus.FINISHED:
            self._aml_run.complete()

        if run_status == RunStatus.FAILED:
            self._aml_run.fail()

        if run_status == RunStatus.SCHEDULED:
            # logger.warning("Scheduled status is not supported in Azure MLFlow integration.")
            # logger.warning("Status will remain" + self.aml_run.get_status())
            # TODO: do we want to update neither or still update only mlflow run?
            # return self._mlflow_run.info
            raise NotImplementedError

        new_info = self._mlflow_run.info._copy_with_overrides(status=run_status, end_time=end_time)
        self._mlflow_run = Run(run_info=new_info, run_data=self._mlflow_run.data)

        return new_info

    def complete(self):
        """
        Mark this run as completed.

        :return: RunInfo describing the updated, finished run.
        """
        return self.update_run_info(run_status=RunStatus.FINISHED, end_time=int(time.time() * 1000))

    def log(self, name, value):
        """
        Log a value for the given name in the run logs.

        :param name: The name of metric
        :type name: str
        :param value: The value of metric
        :type value: float
        """
        self._aml_run.log(name=name, value=value)

    def log_param(self, name, value):
        """
        Add a parameter for the given name in the run logs.

        :param name: The name of paramater
        :type name: str
        :param value: The value of parameter
        :type value: str, will be string-ified if not
        """
        # TODO: needs to be reconciled with Parameters as top level
        key = _AzureMlflowRun._construct_param_key(name)
        self._aml_run.add_properties({key: value})

    def set_tag(self, key, value):
        """
        Set a tag for the specified run.

        :param key: The key of the tag
        :type key: str
        :param value: The value of the tag
        :type value: str, will be string-ified if not
        """
        self._aml_run.tag(key=key, value=value)

    def get_log(self, name):
        """
        Retrieve a value for the given name from the run logs.

        :param name: The name of metric
        :type name: str
        :return: The value of metric
        :rtype: any, The value to be posted to the service
        """
        metrics = self._aml_run.get_metrics()
        value = metrics.get(name)
        if value is None:
            raise MlflowException("Metric '%s' not found under run '%s'" % (name, self._uuid),
                                  databricks_pb2.RESOURCE_DOES_NOT_EXIST)
        return value

    def get_param(self, name):
        """
        Retrieve the previously logged parameter by name.

        :param name: The name of the parameter
        :type name: str
        :return: The parameter value
        :rtype: any, The logged parameter value if it exists.
        """
        properties = self._aml_run.get_properties()
        key = _AzureMlflowRun._construct_param_key(name)
        value = properties.get(key)
        if value is None:
            raise MlflowException("Parameter '%s' not found under run '%s'" % (name, self._uuid),
                                  databricks_pb2.RESOURCE_DOES_NOT_EXIST)
        return value

    def get_metric(self, metric_key):
        """
        Return the last logged value for a given metric.

        :param run_id: Unique identifier for run
        :param metric_key: Metric name within the run

        :return: A single float value for the given metric if logged, else None
        """
        res = self._aml_run._client.metrics.get_metrics_by_run_ids(run_ids=[self._uuid],
                                                                   order_by=('CreatedUtc', 'desc'),
                                                                   merge_strategy_type="None",
                                                                   page_size=1)
        metrics = MetricsClient.dto_to_metrics_dict(res)
        if metric_key in metrics:
            return metrics[metric_key][0] if isinstance(metrics[metric_key], list) else metrics[metric_key]
        else:
            return None

    def get_metric_history(self, metric_key):
        """
        Return all logged value for a given metric.

        :param run_id: Unique identifier for run
        :param metric_key: Metric name within the run

        :return: A list of float values logged for the give metric if logged, else empty list
        """
        metrics = self._aml_run.get_metrics()
        if metric_key in metrics:
            return metrics[metric_key] if isinstance(metrics[metric_key], list) else [metrics[metric_key]]
        else:
            return []

    @staticmethod
    def _construct_param_key(param_name):
        return PARAM_PREFIX + param_name

    @property
    def is_active(self):
        return (self.mlflow_run.info.lifecycle_stage == RunInfo.ACTIVE_LIFECYCLE)

    @property
    def mlflow_run(self):
        return self._mlflow_run

    @property
    def aml_run(self):
        return self._aml_run
