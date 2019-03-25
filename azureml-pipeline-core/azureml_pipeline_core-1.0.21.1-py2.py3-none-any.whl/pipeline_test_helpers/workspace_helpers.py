from azureml.core.compute import ComputeTarget, DataFactoryCompute, AdlaCompute, DatabricksCompute
from azureml.core.compute import AmlCompute, DsvmCompute
from azureml.core.workspace import Workspace
from azureml.core.runconfig import RunConfiguration
from azureml.exceptions import ComputeTargetException
from azureml.pipeline.core._aeva_provider import _AevaWorkflowProvider
from pipeline_test_helpers.mock_objects import MockObjects

import shutil
import os


def setup_workspace(subscription_id="mock-subscription",
                    resource_group="mock-rg",
                    workspace="mock-workspace",
                    experiment_name="helloworld",
                    dry_run=False,
                    service_endpoint=None,
                    default_source_directory=None,
                    location="eastus2euap"):
    if default_source_directory is None:
        default_source_directory = experiment_name

    if not os.path.exists(default_source_directory):
        os.makedirs(default_source_directory)

    if not dry_run:
        workspace = Workspace._get_or_create(name=workspace, subscription_id=subscription_id,
                                             resource_group=resource_group, location=location)
        print("Got workspace: " + workspace._workspace_name)
        workspace._initialize_folder(experiment_name, directory="./" + experiment_name)
        print("Set up folder: " + experiment_name)
        provider = _AevaWorkflowProvider.create_provider(workspace, experiment_name, service_endpoint)

    else:
        workspace = MockObjects.get_workspace(name=workspace, location=location, subscription_id=subscription_id,
                                              resource_group=resource_group)
        provider = MockObjects.get_workflow_provider(workspace)
        MockObjects.mock_datastore(dry_run=True)

    # copy files into default source directory
    src_root = os.path.dirname(os.path.abspath(__file__))
    src_files = ["test.py", "word_count.py"]
    for file_name in src_files:
        dest = os.path.join(experiment_name, file_name)
        src = os.path.join(src_root, file_name)
        if not os.path.isfile(dest):
            shutil.copy(src, dest)

    return workspace, provider, default_source_directory


def setup_computes(workspace, dry_run):
    if not dry_run:
        # HDI target is set up in hdi_tests.py
        hdi_target = None
        hdi_run_config = None

        targets = {
            "dsvm": get_or_create_dsvm_compute(workspace, compute_name="dsvm"),
            "hdi": hdi_target,
            "aml-compute": get_or_create_amlcompute(workspace, compute_name="aml-compute"),
            "datafactory": get_or_create_data_factory(workspace, factory_name='testadf'),
            "adla": get_or_create_adla_compute(workspace, compute_name='testadl'),
            "databricks": get_or_create_databricks_compute(workspace, databricks_name='fahdkdbeastus',
                                                           pat='fake_pat')
        }

        dsvm_run_config = RunConfiguration()
        dsvm_run_config.environment.docker.enabled = "true"

        amlcompute_run_config = RunConfiguration()
        amlcompute_run_config.environment.docker.enabled = "true"

        run_configs = {"hdi": hdi_run_config, "dsvm": dsvm_run_config, "aml-compute": amlcompute_run_config}

    else:
        targets = {"dsvm": MockObjects.get_compute_target("dsvm"),
                   "hdi": MockObjects.get_compute_target("hdi"),
                   "aml-compute": MockObjects.get_compute_target("aml-compute"),
                   "batchaiwithdetails": MockObjects.get_batchai_target_withdetails("batchaiwithdetails"),
                   "datafactory": MockObjects.get_data_factory(),
                   "adla": MockObjects.get_adla_compute(),
                   "databricks": MockObjects.get_databricks_compute(),
                   "batch": MockObjects.get_batch_compute()}
        run_configs = {"dsvm": MockObjects.get_run_config(),
                       "hdi": MockObjects.get_run_config(),
                       "aml-compute": MockObjects.get_run_config()}

    return targets, run_configs


def get_or_create_data_factory(workspace, factory_name):
    try:
        return DataFactoryCompute(workspace, factory_name)
    except ComputeTargetException as e:
        if 'ComputeTargetNotFound' in e.message:
            print('Data factory not found, creating...')
            provisioning_config = DataFactoryCompute.provisioning_configuration()
            data_factory = ComputeTarget.create(workspace, factory_name, provisioning_config)
            data_factory.wait_for_completion()
            return data_factory
        else:
            raise e


def get_or_create_adla_compute(workspace, compute_name):
    try:
        return AdlaCompute(workspace, compute_name)
    except ComputeTargetException as e:
        if 'ComputeTargetNotFound' in e.message:
            print('adla compute not found, creating...')
            provisioning_config = AdlaCompute.provisioning_configuration()
            adla_compute = ComputeTarget.create(workspace, compute_name, provisioning_config)
            adla_compute.wait_for_completion()
            return adla_compute
        else:
            raise e


def get_databricks_compute(name, workspace):
    try:
        databricks_compute = DatabricksCompute(workspace, name)
        return databricks_compute
    except ComputeTargetException as ce:
        print('Could not get databricks compute due to exception: {}'.format(ce))
        return None


def get_or_create_databricks_compute(workspace, databricks_name, pat):
    databricks_compute = get_databricks_compute(databricks_name, workspace)
    if databricks_compute is None:
        print('attaching databricks {}'.format(databricks_name))
        attach_config = DatabricksCompute.attach_configuration(
            resource_id='/subscriptions/ad203158-bc5d-4e72-b764-2607833a71dc/resourceGroups' +
                        '/azureml-pipeline-test/providers/Microsoft.Databricks/workspaces/fahdkdbeastus',
            access_token=pat)
        databricks_compute = ComputeTarget.attach(
            workspace=workspace,
            name=databricks_name,
            attach_configuration=attach_config)
        databricks_compute.wait_for_completion(True)
        print('finished attaching databricks {}'.format(databricks_name))

    return databricks_compute


def get_or_create_dsvm_compute(workspace, compute_name):
    try:
        return DsvmCompute(workspace, compute_name)
    except ComputeTargetException as e:
        if 'ComputeTargetNotFound' in e.message:
            print('dsvm compute not found, creating...')
            dsvm_config = DsvmCompute.provisioning_configuration(vm_size="Standard_D2_v2")
            dsvm_target = DsvmCompute.create(workspace, compute_name, provisioning_configuration=dsvm_config)
            dsvm_target.wait_for_completion(show_output=True)
            return dsvm_target
        else:
            raise e


def get_or_create_amlcompute(workspace, compute_name):
    try:
        return AmlCompute(workspace, compute_name)
    except ComputeTargetException as e:
        if 'ComputeTargetNotFound' in e.message:
            print('amlcompute compute not found, creating...')
            provisioning_config = AmlCompute.provisioning_configuration(vm_size="STANDARD_D2_V2",
                                                                        min_nodes=1,
                                                                        max_nodes=1)
            compute_target = ComputeTarget.create(workspace, compute_name, provisioning_config)
            compute_target.wait_for_completion(show_output=True)
            return compute_target
        else:
            raise e
