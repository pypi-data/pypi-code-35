from mock import Mock
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core.compute import DataFactoryCompute, AdlaCompute, BatchCompute
from azureml.core.workspace import Workspace
from azureml.core.compute_target import AbstractComputeTarget, _BatchAITarget
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core._restclients.aeva.dryrun_service_caller import DryRunServiceCaller
from azureml.pipeline.core._aeva_provider import _AevaModuleSnapshotUploader, _AevaWorkflowProvider
from azureml.pipeline.core import PipelineRun, StepRun
import azureml


def mock_get_url(*args, **kwargs):
    return "Fake url"


azureml._base_sdk_common.service_discovery.CachedServiceDiscovery.get_cached_service_url = mock_get_url


def _get_authentication_header():
    return {"Authorization": "Bearer " + "TOKEN"}


# the purpose of this class is to mock BatchAITarget which has has _batchai_workspace_name variable
# that cannot be mocked as it is not a property
class MockableBatchAITarget(_BatchAITarget):
    _batchai_workspace_name = "wsname"


class MockObjects:

    @staticmethod
    def get_run_config(arguments=None):
        mock_config = RunConfiguration(script="testscript.py",
                                       arguments=arguments if arguments else [],
                                       framework="Python")
        return mock_config

    @staticmethod
    def get_workspace(name="mock name", location="mock location", subscription_id="mock subscription",
                      resource_group="mock resource group"):
        auth_object_mock = Mock(InteractiveLoginAuthentication)
        auth_object_mock.get_authentication_header = _get_authentication_header

        mock_workspace = Mock(spec_set=Workspace)
        workspace_attrs = {
            "subscription_id": subscription_id,
            "name": name,
            "resource_group": resource_group,
            "location": location,
            "_auth_object": auth_object_mock,
            "_workspace_id": "unittest",
        }
        mock_workspace.configure_mock(**workspace_attrs)
        return mock_workspace

    @staticmethod
    def get_compute_target(name):
        mock_compute_target = Mock(spec_set=AbstractComputeTarget)
        target_attrs = {
            "name": name,
            "type": "local"
        }
        mock_compute_target.configure_mock(**target_attrs)
        mock_compute_target._serialize_to_dict.return_value = {
            "type": "local"
        }
        return mock_compute_target

    @staticmethod
    def get_batchai_target_withdetails(name):
        mock_compute_target = Mock(spec_set=MockableBatchAITarget)
        target_attrs = {
            "name": name,
            "cluster_name": "test_cluster_bai_with_details",
            "subscription_id": "test_subscription_123",
            "resource_group_name": "test_rg",
            "type": "batchai",
            "_batchai_workspace_name": "wsname"
        }
        mock_compute_target.configure_mock(**target_attrs)
        mock_compute_target._serialize_to_dict.return_value = {
            "cluster_name": "test_cluster_bai_with_details",
            "subscription_id": "test_subscription_123",
            "resource_group_name": "test_rg",
            "type": "batchai",
            "_batchai_workspace_name": "wsname"
        }
        return mock_compute_target

    @staticmethod
    def get_data_factory():
        return MockDataFactory()

    @staticmethod
    def get_adla_compute():
        return MockAdlaCompute()

    @staticmethod
    def get_databricks_compute():
        return MockDatabricksCompute()

    @staticmethod
    def get_batch_compute():
        return MockBatchCompute()

    @staticmethod
    def get_module_uploader():
        mock_module_uploader = Mock(spec_set=_AevaModuleSnapshotUploader)
        mock_module_uploader.upload.return_value = "mock_snapshot"
        return mock_module_uploader

    @staticmethod
    def get_workflow_provider(workspace):
        service_caller = DryRunServiceCaller()
        module_uploader = MockObjects.get_module_uploader()
        return _AevaWorkflowProvider(service_caller, module_uploader, workspace)

    @staticmethod
    def mock_datastore(dry_run=False):
        if dry_run:
            from azureml.core import Datastore

            class MockedDatastore(object):
                def __init__(self, workspace, name):
                    self.workspace = workspace
                    self.name = name
                    self.type = "AzureBlob"

            @staticmethod
            def _monkey_patched_new(cls, workspace, name=None):
                return MockedDatastore(workspace, name or "Default")

            Datastore.__new__ = _monkey_patched_new


class MockDataFactory(DataFactoryCompute):
    type = "DataFactory"

    def __new__(cls):
        return super(MockDataFactory, cls).__new__(cls, workspace=None, name="mock datafactory")

    def __init__(self):
        self.cluster_resource_id = '/subscriptions/mock-subscription/resourceGroups/mockresourcegroup' \
                                   '/providers/Microsoft.DataFactory/factories/mockfactory'


class MockAdlaCompute(AdlaCompute):
    type = "adla"

    def __new__(cls):
        return super(MockAdlaCompute, cls).__new__(cls, workspace=None, name="mock adla compute")

    def __init__(self):
        self.cluster_resource_id = '/subscriptions/mock-subscription/resourceGroups/mockresourcegroup' \
                                   '/providers/Microsoft.DataLakeAnalytics/accounts/mockadla'


class MockDatabricksCompute(object):
    type = "databricks"

    def __init__(self):
        self.name = "fake databricks"

    def get_credentials(self):
        return {"databricksAccessToken": ""}

    def _get(self, workspace, name):
        return {"properties": {"computeLocation": "eastus"}}


class MockBatchCompute(BatchCompute):
    type = "batch"

    def __new__(cls):
        return super(MockBatchCompute, cls).__new__(cls, workspace=None, name="mock batch compute")

    def __init__(self):
        self.cluster_resource_id = '/subscriptions/mock_subscription/resourceGroups/mock_resource_group' \
                                   '/providers/Microsoft.Batch/batchAccounts/mock_batch_account'


class MockPipelineRun(PipelineRun):
    def __init__(self, run_id, context):
        self._context = context
        self._run_id = run_id
        self._pipeline_run_provider = self._context.workflow_provider.pipeline_run_provider
        self._run_details_url = "sample/url"
        self._graph = None

    def complete(self):
        pass

    def fail(self):
        pass

    def child_run(self, name=None, run_id=None, outputs=None):
        pass

    def get_children(self, **kwargs):
        step_runs = [MockStepRun(self._context, None, self._run_id, n.node_id) for n in self.get_graph().module_nodes]
        return step_runs

    def wait_for_completion(self, show_output=True, timeout_seconds=1000):
        status = self._get_status()
        last_status = None
        separator = ''
        while status == 'NotStarted' or status == 'Running' or status == 'Unknown':
            status = self._get_status()
            if last_status != status:
                if show_output:
                    print('%sstatus:%s' % (separator, status))
                last_status = status
                separator = ''
            else:
                if show_output:
                    print('.')
                separator = '\n'


class MockStepRun(StepRun):
    def __init__(self, context, step_run_id, pipeline_run_id, node_id):
        self._context = context
        self._pipeline_run_id = pipeline_run_id
        self._node_id = node_id
        self._step_run_id = step_run_id
        self._step_run_provider = self._context.workflow_provider.step_run_provider

    def fail(self):
        pass

    def child_run(self, name=None, run_id=None, outputs=None):
        pass

    def complete(self):
        pass
