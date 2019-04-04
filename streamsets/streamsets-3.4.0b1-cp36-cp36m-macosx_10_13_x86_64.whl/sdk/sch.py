# Copyright 2019 StreamSets Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstractions for interacting with StreamSets Dataflow Performance Manager."""
import io
import json
import logging
import zipfile
from datetime import datetime

from . import sch_api
from .sdc import DataCollector as DataCollectorInstance
from .sch_models import (ClassificationRuleBuilder, Configuration, DataCollector, Job, JobBuilder, Organization,
                         OrganizationBuilder, Pipeline, PipelineBuilder, ProtectionMethodBuilder, ProtectionPolicy,
                         ProtectionPolicyBuilder, ReportDefinition, Topology, User, UserBuilder, Jobs, Users,
                         DataCollectors, Organizations, Pipelines, ProtectionPolicies, ScheduledTaskBuilder,
                         ScheduledTasks, Topologies)
from .utils import SeekableList, join_url_parts, wait_for_condition

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_SDC_ID = 'SYSTEM_SDC_ID'


class ControlHub:
    """Class to interact with StreamSets Control Hub.

    Args:
        server_url (:obj:`str`): SCH server base URL.
        username (:obj:`str`): SCH username.
        password (:obj:`str`): SCH password.
    """
    VERIFY_SSL_CERTIFICATES = True
    def __init__(self,
                 server_url,
                 username,
                 password):
        self.server_url = server_url
        self.username = username
        self.password = password

        self.organization = self.username.split('@')[1]

        session_attributes = {'verify': self.VERIFY_SSL_CERTIFICATES}
        self.api_client = sch_api.ApiClient(server_url=self.server_url,
                                            username=self.username,
                                            password=self.password,
                                            session_attributes=session_attributes)

        self.login_command = self.api_client.login()

        self._roles = {user_role['id']: user_role['label']
                       for user_role in self.api_client.get_all_user_roles()}

        # We keep the Swagger API definitions as attributes for later use by various
        # builders.
        self._job_api = self.api_client.get_job_api()
        self._pipelinestore_api = self.api_client.get_pipelinestore_api()
        self._security_api = self.api_client.get_security_api()
        self._topology_api = self.api_client.get_topology_api()
        self._scheduler_api = self.api_client.get_scheduler_api()

    @property
    def system_data_collector(self):
        return DataCollectorInstance(server_url=join_url_parts(self.server_url, 'pipelinestore'),
                                     control_hub=self)

    @property
    def organization_global_configuration(self):
        organization_global_configuration = self.api_client.get_organization_global_configurations().response.json()

        # Some of the config names are a bit long, so shorten them slightly...
        ID_TO_REMAP = {'accountType': 'Organization account type',
                       'contractExpirationTime': 'Timestamp of the contract expiration',
                       'trialExpirationTime': 'Timestamp of the trial expiration'}
        return Configuration(configuration=organization_global_configuration,
                             update_callable=self.api_client.update_organization_global_configurations,
                             id_to_remap=ID_TO_REMAP)

    @organization_global_configuration.setter
    def organization_global_configuration(self, value):
        self.api_client.update_organization_global_configurations(value._data)

    def set_user(self, username, password):
        """Set the user by which subsequent actions will be run.

        Args:
            username (:obj:`str`): SCH username.
            password (:obj:`str`): SCH password.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        self.username = self.api_client.username = username
        self.password = self.api_client.password = password
        return self.api_client.login()

    def get_pipeline_builder(self, data_collector=None):
        """Get a pipeline builder instance with which a pipeline can be created.

        Args:
            data_collector (:py:obj:`streamsets.sdk.sch_models.DataCollector`, optional): The Data Collector
                in which to author the pipeline. If omitted, Control Hub's system SDC will be used. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.PipelineBuilder`.
        """
        pipeline = {property: None
                    for property in self._pipelinestore_api['definitions']['PipelineJson']['properties']}

        if data_collector is not None:
            pipeline['sdcId'] = data_collector.id
            pipeline['sdcVersion'] = data_collector.version
            data_collector_instance = data_collector.instance
        else:
            # For the system Data Collector, we need to create a new pipeline (which we then delete) to populate
            # DataCollector._pipeline.
            data_collector_instance = self.system_data_collector
            commit_pipeline_json = {'name': 'Pipeline Builder',
                                    'sdcId': DEFAULT_SYSTEM_SDC_ID}
            commit_pipeline_response = self.api_client.commit_pipeline(new_pipeline=True,
                                                                       import_pipeline=False,
                                                                       body=commit_pipeline_json).response.json()
            pipeline['sdcId'] = commit_pipeline_response['sdcId']
            pipeline['sdcVersion'] = commit_pipeline_response['sdcVersion']

            commit_id = commit_pipeline_response['commitId']
            pipeline_id = commit_pipeline_response['pipelineId']

            pipelines_zip_data = self.api_client.export_pipelines(body=[commit_id]).response.content
            pipelines_zip_file = zipfile.ZipFile(file=io.BytesIO(pipelines_zip_data), mode='r')
            pipeline_json_filename = next(filename
                                          for filename in pipelines_zip_file.namelist()
                                          if filename.endswith('.json'))
            with pipelines_zip_file.open(pipeline_json_filename) as pipeline_json:
                data_collector_instance._pipeline = json.loads(pipeline_json.read().decode())
            self.api_client.delete_pipeline(pipeline_id)

        data_collector_pipeline_builder = data_collector_instance.get_pipeline_builder()
        return PipelineBuilder(pipeline=pipeline,
                               data_collector_pipeline_builder=data_collector_pipeline_builder)

    def publish_pipeline(self, pipeline, commit_message='New pipeline'):
        """Publish a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            commit_message (:obj:`str`, optional): Default: ``'New pipeline'``.
        """
        # A :py:class:`streamsets.sdk.sch_models.Pipeline` instance with no commit ID hasn't been
        # published to Control Hub before, so we do so first.
        if not pipeline.commit_id:
            commit_pipeline_json = {'name': pipeline._pipeline_definition['title'],
                                    'sdcId': pipeline.sdc_id}
            if pipeline.sdc_id != DEFAULT_SYSTEM_SDC_ID:
                commit_pipeline_json.update({'pipelineDefinition': json.dumps(pipeline._pipeline_definition),
                                             'rulesDefinition': json.dumps(pipeline._rules_definition)})
            pipeline._data = self.api_client.commit_pipeline(new_pipeline=True,
                                                             import_pipeline=False,
                                                             body=commit_pipeline_json).response.json()
        # If the pipeline does have a commit ID, we want to create a new draft and update the existing
        # one in the pipeline store instead of creating a new one.
        else:
            pipeline._data = self.api_client.create_pipeline_draft(
                commit_id=pipeline.commit_id,
                authoring_sdc_id=pipeline.sdc_id,
                authoring_sdc_version=pipeline.sdc_version
            ).response.json()
            # The pipeline name is overwritten when drafts are created, so we account for it here.
            pipeline.name = pipeline._pipeline_definition['title']

        pipeline.commit_message = commit_message
        pipeline.current_rules['rulesDefinition'] = json.dumps(pipeline._rules_definition)
        pipeline.pipeline_definition = json.dumps(pipeline._pipeline_definition)

        self.api_client.save_pipeline_commit(commit_id=pipeline.commit_id,
                                             include_library_definitions=True,
                                             body=pipeline._data)
        publish_pipeline_commit_command = self.api_client.publish_pipeline_commit(commit_id=pipeline.commit_id)
        # Due to DPM-4470, we need to do one more REST API call to get the correct pipeline data.
        pipeline_commit = self.api_client.get_pipeline_commit(commit_id=pipeline.commit_id).response.json()
        pipeline._builder._sch_pipeline = pipeline._data = pipeline_commit
        return publish_pipeline_commit_command

    def delete_pipeline(self, pipeline, only_selected_version=False):
        """Delete a pipeline.

        Args:
            pipeline (:py:obj:`streamsets.sdk.sch_models.Pipeline`): Pipeline object.
            only_selected_version (:obj:`boolean`): Delete only current commit.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if only_selected_version:
            return self.api_client.delete_pipeline_commit(pipeline.commit_id)
        return self.api_client.delete_pipeline(pipeline.pipeline_id)

    def get_user_builder(self):
        """Get a user builder instance with which a user can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.UserBuilder`.
        """
        user = {}
        # Update the UserJson with the API definitions from Swagger.
        user.update({property: None
                     for property in self._security_api['definitions']['UserJson']['properties']})

        # Set other properties based on defaults from the web UI.
        user_defaults = {'active': True,
                         'groups': ['all@{}'.format(self.organization)],
                         'organization': self.organization,
                         'passwordGenerated': True,
                         'roles': ['timeseries:reader',
                                   'datacollector:manager',
                                   'jobrunner:operator',
                                   'pipelinestore:pipelineEditor',
                                   'topology:editor',
                                   'org-user',
                                   'sla:editor',
                                   'provisioning:operator',
                                   'user',
                                   'datacollector:creator',
                                   'notification:user'],
                         'userDeleted': False}
        user.update(user_defaults)

        return UserBuilder(user=user, roles=self._roles)

    def add_user(self, user):
        """Add a user. Some user attributes are updated by SCH such as
            created_by,
            created_on,
            last_modified_by,
            last_modified_on,
            password_expires_on,
            password_system_generated.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding a user %s ...', user)
        create_user_command = self.api_client.create_user(self.organization, user._data)
        # Update :py:class:`streamsets.sdk.sch_models.User` with updated User metadata.
        user._data = create_user_command.response.json()
        return create_user_command

    def update_user(self, user):
        """Update a user. Some user attributes are updated by SCH such as
            last_modified_by,
            last_modified_on.

        Args:
            user (:py:class:`streamsets.sdk.sch_models.User`): User object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Updating a user %s ...', user)
        update_user_command = self.api_client.update_user(body=user._data,
                                                          org_id=self.organization,
                                                          user_id=user.id)
        user._data = update_user_command.response.json()
        return update_user_command

    def delete_user(self, *users, deactivate=False):
        """Delete users. Deactivate users before deleting if configured.

        Args:
            *users: One or more instances of :py:class:`streamsets.sdk.sch_models.User`.
            deactivate (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        if deactivate:
            for user in users:
                logger.info('Deactivating a user %s ...', user)
                user.active = False
                self.update_user(user)

        delete_user_command = None
        if len(users) == 1:
            logger.info('Deleting a user %s ...', users[0])
            delete_user_command = self.api_client.delete_user(org_id=self.organization,
                                                              user_id=users[0].id)
        else:
            user_ids = [user.id for user in users]
            logger.info('Deleting users %s ...', user_ids)
            delete_user_command = self.api_client.delete_users(body=user_ids,
                                                               org_id=self.organization)
        return delete_user_command

    @property
    def users(self):
        """Users.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.Users`.
        """
        return Users(self, self._roles, self.organization)

    @property
    def data_collectors(self):
        """Data Collectors registered to the Control Hub instance.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DataCollectors`.
        """
        return DataCollectors(self)

    def deactivate_datacollector(self, data_collector):
        """Deactivate data collector.

         Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Deactivating data collector component from organization %s with component id %s ...',
                    self.organization, data_collector.id)
        self.api_client.deactivate_components(org_id=self.organization,
                                              components_json=[data_collector.id])

    def activate_datacollector(self, data_collector):
        """Activate data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Activating data collector component from organization %s with component id %s ...',
                    self.organization, data_collector.id)
        self.api_client.activate_components(org_id=self.organization,
                                            components_json=[data_collector.id])

    def delete_data_collector(self, data_collector):
        """Delete data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Deleting data dollector %s ...', data_collector.id)
        self.api_client.delete_sdc(data_collector_id=data_collector.id)

    def delete_and_unregister_data_collector(self, data_collector):
        """Delete and Unregister data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.
        """
        logger.info('Deactivating data collector component from organization %s with component id %s ...',
                    data_collector.organization, data_collector.id)
        self.api_client.deactivate_components(org_id=self.organization,
                                              components_json=[data_collector.id])
        logger.info('Deleting data collector component from organization %s with component id %s ...',
                    data_collector.organization, data_collector.id)
        self.api_client.delete_components(org_id=self.organization,
                                          components_json=[data_collector.id])
        logger.info('Deleting data dollector from jobrunner %s ...', data_collector.id)
        self.api_client.delete_sdc(data_collector_id=data_collector.id)

    def update_data_collector_labels(self, data_collector):
        """Update data collector labels.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.DataCollector`.
        """
        logger.info('Updating data collector %s with labels %s ...',
                    data_collector.id, data_collector.labels)
        return DataCollector(self.api_client.update_sdc_labels(
            data_collector_id=data_collector.id,
            data_collector_json=data_collector._data).response.json(), self)

    def get_data_collector_labels(self, data_collector):
        """Returns all labels assigned to data collector.

        Args:
            data_collector (:py:class:`streamsets.sdk.sch_models.DataCollector`): Data Collector object.

        Returns:
            A :obj:`list` of data collector assigned labels.
        """
        logger.info('Getting assigned labels for data collector %s ...', data_collector.id)
        return self.api_client.get_sdc_lables(data_collector_id=data_collector.id).response.json()

    def get_job_builder(self):
        """Get a job builder instance with which a job can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.JobBuilder`.
        """
        job = {property: None
               for property in self._job_api['definitions']['JobJson']['properties']}

        # Set other properties based on defaults from the web UI.
        JOB_DEFAULTS = {'forceStopTimeout': 120000,
                        'labels': ['all'],
                        'numInstances': 1,
                        'statsRefreshInterval': 60000}
        job.update(JOB_DEFAULTS)
        return JobBuilder(job=job, control_hub=self)

    def get_components(self, component_type_id, offset=None, len_=None, order_by='LAST_VALIDATED_ON', order='ASC'):
        """Get components.

        Args:
            component_type_id (:obj:`str`): Component type id.
            offset (:obj:`str`, optional): Default: ``None``.
            len_ (:obj:`str`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``'LAST_VALIDATED_ON'``.
            order (:obj:`str`, optional): Default: ``'ASC'``.
        """
        return self.api_client.get_components(org_id=self.organization,
                                              component_type_id=component_type_id,
                                              offset=offset,
                                              len_=len_,
                                              order_by=order_by,
                                              order=order)

    def create_components(self, component_type, number_of_components=1, active=True):
        """Create components.

        Args:
            component_type (:obj:`str`): Component type.
            number_of_components (:obj:`int`, optional): Default: ``1``.
            active (:obj:`bool`, optional): Default: ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.CreateComponentsCommand`.
        """
        return self.api_client.create_components(org_id=self.organization,
                                                 component_type=component_type,
                                                 number_of_components=number_of_components,
                                                 active=active)

    def get_organization_builder(self):
        """Get an organization builder instance with which an organization can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.OrganizationBuilder`.
        """
        organization = {property: None
                        for property in self._security_api['definitions']['NewOrganizationJson']['properties']}

        # Set other properties based on defaults from the web UI.
        organization_defaults = {'active': True,
                                 'passwordExpiryTimeInMillis': 5184000000,  # 60 days
                                 'validDomains': '*'}
        organization_admin_user_defaults = {'active': True,
                                            'roles': ['user',
                                                      'org-admin',
                                                      'datacollector:admin',
                                                      'pipelinestore:pipelineEditor',
                                                      'jobrunner:operator',
                                                      'timeseries:reader',
                                                      'timeseries:writer',
                                                      'topology:editor',
                                                      'notification:user',
                                                      'sla:editor',
                                                      'provisioning:operator']}
        organization['organization'] = organization_defaults
        organization['organizationAdminUser'] = organization_admin_user_defaults

        return OrganizationBuilder(organization=organization['organization'],
                                   organization_admin_user=organization['organizationAdminUser'])

    def add_organization(self, organization):
        """Add an organization.

        Args:
            organization (:py:obj:`streamsets.sdk.sch_models.Organization`): Organization object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        logger.info('Adding organization %s ...', organization.name)
        body = {'organization': organization._data,
                'organizationAdminUser': organization._organization_admin_user}
        create_organization_command = self.api_client.create_organization(body)
        organization._data = create_organization_command.response.json()
        return create_organization_command

    @property
    def organizations(self):
        """Organizations.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.Organizations`.
        """
        return Organizations(self)

    @property
    def pipelines(self):
        """Pipelines.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.Pipelines`.
        """
        return Pipelines(self, self.organization)

    def import_pipelines_from_archive(self, archive, commit_message, fragments=False):
        """Import pipelines from archived zip directory.

        Args:
            archive (:obj:`file`): file containing the pipelines.
            commit_message (:obj:`str`): Commit message.
            fragments (:obj:`bool`, optional): Indicates if pipeline contains fragments.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        return SeekableList([Pipeline(pipeline,
                                      builder=None,
                                      pipeline_definition=json.loads(pipeline['pipelineDefinition']),
                                      rules_definition=json.loads(pipeline['currentRules']['rulesDefinition']),
                                      control_hub=self)
                             for pipeline in self.api_client.import_pipelines(commit_message=commit_message,
                                                                              pipelines_file=archive,
                                                                              fragments=fragments).response.json()])

    def import_pipeline(self, pipeline, commit_message, name=None, data_collector_instance=None):
        """Import pipeline from json file.

        Args:
            pipeline (:obj:`dict`): A python dict representation of ControlHub Pipeline.
            commit_message (:obj:`str`): Commit message.
            name (:obj:`str`, optional): Name of the pipeline. If left out, pipeline name from JSON object will be
                                         used. Default ``None``.
            data_collector_instance (:py:class:`streamsets.sdk.sch_models.DataCollector`): If excluded, system sdc will
                                                                                           be used. Default ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        if name is None: name = pipeline['pipelineConfig']['title']
        sdc_id = data_collector_instance.id if data_collector_instance is not None else DEFAULT_SYSTEM_SDC_ID
        pipeline['pipelineConfig']['info']['sdcId'] = sdc_id
        commit_pipeline_json = {'name': name,
                                'commitMessage': commit_message,
                                'pipelineDefinition': json.dumps(pipeline['pipelineConfig']),
                                'libraryDefinitions': json.dumps(pipeline['libraryDefinitions']),
                                'rulesDefinition': json.dumps(pipeline['pipelineRules']),
                                'sdcId': sdc_id}
        commit_pipeline_response = self.api_client.commit_pipeline(new_pipeline=False,
                                                                   import_pipeline=True,
                                                                   body=commit_pipeline_json).response.json()
        commit_id = commit_pipeline_response['commitId']
        return self.pipelines.get(commit_id=commit_id)


    def export_pipelines(self, pipelines, fragments=False):
        """Export pipelines.

        Args:
            pipelines (:obj:`list`): A list of :py:class:`streamsets.sdk.sch_models.Pipeline` instances.
            fragments (:obj:`bool`): Indicates if exporting fragments is needed.

        Returns:
            An instance of type :py:obj:`bytes` indicating the content of zip file with pipeline json files.
        """
        commit_ids = [pipeline.commit_id for pipeline in pipelines]
        return self.api_client.export_pipelines(body=commit_ids, fragments=fragments).response.content

    @property
    def jobs(self):
        """Jobs.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.Jobs`.
        """
        return Jobs(self)

    @property
    def data_protector_enabled(self):
        """:obj:`bool`: Whether Data Protector is enabled for the current organization."""
        add_ons = self.api_client.get_available_add_ons().response.json()
        logger.debug('Add-ons: %s', add_ons)
        return all(app in add_ons['enabled'] for app in ['policy', 'sdp_classification'])

    def add_job(self, job):
        """Add a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        new_job_json = {property_: value
                        for property_, value in job._data.items()
                        if property_ in self._job_api['definitions']['NewJobJson']['properties']}
        logger.info('Adding job %s ...', job.job_name)
        create_job_command = self.api_client.create_job(body=new_job_json)
        # Update :py:class:`streamsets.sdk.sch_models.Job` with updated Job metadata.
        job._data = create_job_command.response.json()

        if self.data_protector_enabled:
            policies = dict(jobId=job.job_id)
            if job.read_policy:
                policies['readPolicyId'] = job.read_policy._id
            else:
                read_protection_policies = self.protection_policies.get_all(enactment='Read')
                if len(read_protection_policies) == 1:
                    logger.warning('Read protection policy not set for job (%s). Setting to %s ...',
                                   job.job_name,
                                   read_protection_policies[0].name)
                    policies['readPolicyId'] = read_protection_policies[0]._id
                else:
                    raise Exception('Read policy not selected.')

            if job.write_policy:
                policies['writePolicyId'] = job.write_policy._id
            else:
                write_protection_policies = self.protection_policies.get_all(enactment='Write')
                if len(write_protection_policies) == 1:
                    logger.warning('Write protection policy not set for job (%s). Setting to %s ...',
                                   job.job_name,
                                   write_protection_policies[0].name)
                    policies['writePolicyId'] = write_protection_policies[0]._id
                else:
                    raise Exception('Write policy not selected.')
            self.api_client.update_job_policies(body=policies)
        return create_job_command

    def edit_job(self, job):
        """Edit a job.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        logger.info('Editing job %s with job id %s ...', job.job_name, job.job_id)
        return Job(self.api_client.update_job(job_id=job.job_id, job_json=job._data).response.json())

    def get_current_job_status(self, job):
        """Returns the current job status for given job id.

        Args:
            job (:py:class:`streamsets.sdk.sch_models.Job`): Job object.
        """
        logger.info('Fetching job status for job id %s ...', job.job_id)
        return self.api_client.get_current_job_status(job_id=job.job_id)

    def delete_job(self, *jobs):
        """Delete one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Deleting job(s) %s ...', job_ids)
        self.api_client.delete_jobs(job_ids)

    def start_job(self, *jobs, wait_for_data_collectors=False):
        """Start one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
            wait_for_data_collectors (:obj:`bool`, optional): Default: False.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Starting jobs (%s) ...', job_ids)
        start_jobs_command = self.api_client.start_jobs(job_ids)

        for job in jobs:
            self.api_client.wait_for_job_status(job_id=job.job_id, status='ACTIVE')
            if wait_for_data_collectors:
                def job_has_data_collector(job):
                    job.refresh()
                    job_data_collectors = job.data_collectors
                    logger.debug('Job Data Collectors: %s', job_data_collectors)
                    return len(job_data_collectors) > 0
                wait_for_condition(job_has_data_collector, [job])
            job.refresh()
        return start_jobs_command

    def stop_job(self, *jobs, force=False):
        """Stop one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
            force (:obj:`bool`, optional): Force job to stop. Default: ``False``.
        """
        jobs_ = {job.job_id: job for job in jobs}
        job_ids = list(jobs_.keys())
        logger.info('Stopping job(s) %s ...', job_ids)
        # At the end, we'll return the command from the job being stopped, so we hold onto it while we update
        # the underlying :py:class:`streamsets.sdk.sch_models.Job` instances.
        stop_jobs_command = self.api_client.force_stop_jobs(job_ids) if force else self.api_client.stop_jobs(job_ids)

        for job_id in job_ids:
            self.api_client.wait_for_job_status(job_id=job_id, status='INACTIVE')
        updated_jobs = self.api_client.get_jobs(body=job_ids).response.json()
        for updated_job in updated_jobs:
            job_id = updated_job['id']
            jobs_[job_id]._data = updated_job
        return stop_jobs_command

    def get_protection_policy_builder(self):
        """Get a protection policy builder instance with which a protection policy can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionPolicyBuilder`.
        """
        protection_policy = self.api_client.get_new_protection_policy().response.json()['response']['data']
        protection_policy.pop('messages', None)
        id_ = protection_policy['id']

        policy_procedure = self.api_client.get_new_policy_procedure(id_).response.json()['response']['data']
        policy_procedure.pop('messages', None)
        return ProtectionPolicyBuilder(protection_policy, policy_procedure)

    def get_protection_method_builder(self):
        """Get a protection method builder instance with which a protection method can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ProtectionMethodBuilder`.
        """
        return ProtectionMethodBuilder(self.get_pipeline_builder())

    def get_classification_rule_builder(self):
        """Get a classification rule builder instance with which a classification rule can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ClassificationRuleBuilder`.
        """
        classification_catalog_list_response = self.api_client.get_classification_catalog_list().response.json()
        classification_catalog_page_id = classification_catalog_list_response['response'][0]['data']['id']
        classification_rule = self.api_client.get_new_classification_rule(
            classification_catalog_page_id
        ).response.json()['response']['data']
        # Remove 'messages' from the classification rule JSON.
        classification_rule.pop('messages', None)
        classifier = self.api_client.get_new_classification_classifier(
            classification_catalog_page_id
        ).response.json()['response']['data']
        # Remove 'messages' from the classifier JSON.
        classifier.pop('messages', None)
        return ClassificationRuleBuilder(classification_rule, classifier)

    def add_protection_policy(self, protection_policy):
        """Add a protection policy.

        Args:
            protection_policy (:py:obj:`streamsets.sdk.sch_models.ProtectionPolicy`): Protection Policy object.
        """
        protection_policy._id = self.api_client.create_protection_policy(
            {'data': protection_policy._data}
        ).response.json()['response']['data']['id']
        for procedure in protection_policy.procedures:
            new_policy_procedure = self.api_client.get_new_policy_procedure(
                protection_policy._id
            ).response.json()['response']['data']
            procedure._id = new_policy_procedure['id']
            procedure._policy_id = protection_policy._id
            self.api_client.create_policy_procedure({'data': procedure._data})

    @property
    def protection_policies(self):
        """Protection policies.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.ProtectionPolicies`.
        """
        return ProtectionPolicies(self)

    def add_classification_rule(self, classification_rule, commit=False):
        """Add a classification rule.

        Args:
            classification_rule (:py:obj:`streamsets.sdk.sch_models.ClassificationRule`): Classification Rule object.
            commit (:obj:`bool`, optional): Whether to commit the rule after adding it. Default: ``False``.
        """
        self.api_client.create_classification_rule({'data': classification_rule._data})
        default_classifier_ids = [classifier['data']['id']
                                  for classifier
                                  in self.api_client.get_classification_classifier_list(
                                                                                        classification_rule._data['id']
                                                                                        ).response.json()['response']]
        for classifier_id in default_classifier_ids:
            self.api_client.delete_classification_classifier(classifier_id)

        for classifier in classification_rule.classifiers:
            self.api_client.create_classification_classifier({'data': classifier._data})

        if commit:
            catalog_id = self.api_client.get_classification_catalog_list().response.json()['response'][0]['data']['id']
            self.api_client.commit_classification_rules(catalog_id)

    def get_scheduled_task_builder(self):
        """Get a scheduled task builder instance with which a scheduled task can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.ScheduledTask`.
        """
        job_selection_types = self.api_client.get_job_selection_types(api_version=2).response.json()['response']['data']
        return ScheduledTaskBuilder(job_selection_types, self)

    def publish_scheduled_task(self, task):
        """Send the built scheduled task to Control Hub."""
        self.api_client.create_scheduled_task(data={'data': task._data}, api_version=2)

    @property
    def scheduled_tasks(self):
        """Scheduled Tasks.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.ScheduledTasks`.
        """
        return ScheduledTasks(self)

    def acknowledge_job_error(self, *jobs):
        """Acknowledge errors for one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Acknowledging errors for job(s) %s ...', job_ids)
        self.api_client.jobs_acknowledge_errors(job_ids)

    def sync_job(self, *jobs):
        """Sync one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Synchronizing job(s) %s ...', job_ids)
        self.api_client.sync_jobs(job_ids)

    def balance_job(self, *jobs):
        """Balance one or more jobs.

        Args:
            *jobs: One or more instances of :py:class:`streamsets.sdk.sch_models.Job`.
        """
        job_ids = [job.job_id for job in jobs]
        logger.info('Balancing job(s) %s ...', job_ids)
        self.api_client.balance_jobs(job_ids)

    def get_topology_builder(self):
        """Get a topology builder instance with which a topology can be created.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.TopologyBuilder`.
        """
        topology = {}
        # Update the TopologyJson with the API definitions from Swagger.
        topology.update({property: None
                         for property in self._topology_api['definitions']['TopologyJson']['properties']})
        topology['organization'] = self.organization

        return TopologyBuilder(topology)

    @property
    def topologies(self):
        """Topologies.

        Returns:
            An instance of :py:obj:`streamsets.sdk.sch_models.Topologies`.
        """
        return Topologies(self)

    def create_topology(self, topology):
        """Create a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Topology`.
        """
        logger.info('Creating topology %s ...', topology.topology_name)
        return Topology(self.api_client.create_topology(topology_json=topology._data).response.json())

    def edit_topology(self, topology):
        """Edit a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Topology`.
        """
        logger.info('Editing topology %s with commit id %s ...', topology.topology_name, topology.commit_id)
        return Topology(self.api_client.update_topology(commit_id=topology.commit_id,
                                                        topology_json=topology._data).response.json())

    def delete_topology_all_versions(self, topology):
        """Delete all versions of a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.
        """
        logger.info('Deleting topology %s with topology id %s ...', topology.topology_name, topology.topology_id)
        self.api_client.delete_topologies(topologies_json=[topology.topology_id])

    def delete_topology_selected_version(self, topology):
        """Delete selected version of topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.
        """
        logger.info('Deleting topology version %s for topology %s ...', topology.commit_id, topology.topology_name)
        self.api_client.delete_topology_versions(commits_json=[topology.commit_id])

    def publish_topology(self, topology):
        """Public a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_models.Topology`.
        """
        logger.info('Publish topology %s with topology id %s ...', topology.topology_name, topology.topology_name)
        return Topology(self.api_client.publish_topology(commit_id=topology.commit_id,
                                                         commit_message=None).response.json())

    def _get_topology_job_nodes(self, topology):
        # extract job nodes - based off of https://bit.ly/2M6sPLv
        topology_definition = json.loads(topology.topology_definition)
        return [topology_node for topology_node in topology_definition['topologyNodes']
                if topology_node['nodeType'] == 'JOB']

    def get_topology_jobs(self, topology):
        """Get jobs for given topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.

        Returns:
            A list of :py:class:`streamsets.sdk.sch_models.Job` instances.
        """
        job_ids = list({job_node['jobId'] for job_node in self._get_topology_job_nodes(topology)})
        return [Job(job) for job in self.api_client.get_jobs(job_ids).response.json()]

    def start_all_topology_jobs(self, topology):
        """Start all jobs of a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.
        """
        job_ids = list({job_node['jobId'] for job_node in self._get_topology_job_nodes(topology)})
        self.api_client.start_jobs(job_ids)
        for job_id in job_ids:
            self.api_client.wait_for_job_status(job_id=job_id, status='ACTIVE')

    def stop_all_topology_jobs(self, topology, force=False):
        """Stop all jobs of a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.
            force (:obj:`bool`, optional): Force topology jobs to stop. Default: ``False``.
        """
        job_ids = list({job_node['jobId'] for job_node in self._get_topology_job_nodes(topology)})
        if force:
            self.api_client.force_stop_jobs(job_ids)
        else:
            self.api_client.stop_jobs(job_ids)
        for job_id in job_ids:
            self.api_client.wait_for_job_status(job_id=job_id, status='INACTIVE')

    def acknowledge_topology_errors(self, topology):
        """Acknowledge errors of a topology.

        Args:
            topology (:py:class:`streamsets.sdk.sch_models.Topology`): Topology object.
        """
        job_ids = list({job_node['jobId'] for job_node in self._get_topology_job_nodes(topology)})
        self.api_client.jobs_acknowledge_errors(job_ids)

    def get_all_report_definitions(self, organization, offset=0, len=-1,
                                   order_by='NAME', order='ASC', filter_text=None):
        """Get all Report Definitions.

        Args:
            organization (:obj:`str`): Organization Id.
            offset (:obj:`int`, optional): Default: ``0``.
            len (:obj:`int`, optional): Default: ``-1``.
            order_by (:obj:`str`, optional): Default: ``'NAME'``.
            order (:obj:`str`, optional): Default: ``'ASC'``.
            filter_text (:obj:`str`, optional): Default: ``None``.

        Returns:
            A list of :py:class:`streamsets.sdk.sch_models.ReportDefinition` instances.
        """
        return [ReportDefinition(report_def)
                for report_def in self.api_client.return_all_report_definitions(
                                                                                organization=organization,
                                                                                offset=offset,
                                                                                len=len,
                                                                                order_by=order_by,
                                                                                order=order,
                                                                                filter_text=filter_text
                                                                                ).response.json()['data']]
