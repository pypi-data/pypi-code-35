# coding=utf-8
import logging
import os
import requests
import time
from retry import retry
from ibm_ai_openscale_cli.enums import ResetType, MLEngineType
from ibm_ai_openscale import WatsonMachineLearningInstance4ICP
from ibm_ai_openscale.engines import AzureMachineLearningInstance, AzureMachineLearningAsset
from ibm_ai_openscale.engines import CustomMachineLearningInstance, CustomMachineLearningAsset
from ibm_ai_openscale.engines import SageMakerMachineLearningInstance, SageMakerMachineLearningAsset
from ibm_ai_openscale.engines import SPSSMachineLearningInstance, SPSSMachineLearningAsset
from ibm_ai_openscale.engines import WatsonMachineLearningInstance, WatsonMachineLearningAsset
from ibm_ai_openscale.supporting_classes import Feature, InputDataType, ProblemType, FeedbackFormat
from ibm_ai_openscale_cli.openscale.openscale import OpenScale
from ibm_ai_openscale_cli.openscale.openscale_reset import OpenScaleReset
from ibm_ai_openscale_cli.utility_classes.utils import get_iam_headers

logger = logging.getLogger(__name__)
parent_dir = os.path.dirname(__file__)

class OpenScaleClient(OpenScaleReset):

    def __init__(self, args, credentials, database_credentials):
        super().__init__(args, credentials, database_credentials)
        self._binding_id = None

    def set_model(self, model):
        self._model = model
        self._subscription = None
        self._asset_details_dict = None
        self._fairness_run_once = True
        self._explainability_run_once = True

    @retry(tries=5, delay=8, backoff=2)
    def create_datamart(self):
        '''
        Create datamart schema and datamart
        '''
        logger.info('Creating datamart {} ...'.format(self._datamart_name))

        if self._database is None:
            logger.info('PostgreSQL instance: internal')
            start = time.time()
            self._client.data_mart.setup(internal_db=True)
            elapsed = time.time() - start
        else:
            self._database.create_new_schema(self._datamart_name, self._keep_schema)
            start = time.time()
            self._client.data_mart.setup(db_credentials=self._database_credentials, schema=self._datamart_name)
            elapsed = time.time() - start
        logger.info('Datamart {} created successfully'.format(self._datamart_name))
        logger.debug('TIMER: data_mart.setup in {:.3f} seconds'.format(elapsed))

    @retry(tries=5, delay=4, backoff=2)
    def bind_mlinstance(self, credentials):
        '''
        Bind ML instance
        '''
        logger.info('Binding {} instance to {} ...'.format(self._args.ml_engine_type.name.lower(), self._args.service_name))
        binding_name = None
        if self._args.ml_engine_type is MLEngineType.WML:
            if self._args.is_icp:
                ml_instance = WatsonMachineLearningInstance4ICP()
            else:
                ml_instance = WatsonMachineLearningInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.AZUREML:
            ml_instance = AzureMachineLearningInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.SPSS:
            ml_instance = SPSSMachineLearningInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.CUSTOM:
            ml_instance = CustomMachineLearningInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            ml_instance = SageMakerMachineLearningInstance(credentials)
        binding_name = '{}{}Instance'.format(self._args.ml_engine_type.name, 'ICP' if self._args.is_icp else ' ')
        start = time.time()
        self._binding_id = self._client.data_mart.bindings.add(binding_name, ml_instance)
        elapsed = time.time() - start
        logger.info('Binding completed successfully')
        logger.debug('TIMER: data_mart.bindings.add in {:.3f} seconds'.format(elapsed))

    @retry(tries=5, delay=4, backoff=2)
    def use_existing_binding(self, asset_details_dict):
        if self._args.is_icp:
            self._binding_id = '999'
        else:
            self._binding_id = asset_details_dict['binding_uid']

    @retry(tries=5, delay=4, backoff=2)
    def subscribe_to_model_deployment(self, asset_details_dict):
        '''
        Create subscription for the given model
        '''
        logger.info('Subscribing ML deployment to {} ...'.format(self._args.service_name))
        asset_metadata = self._model.configuration_data['asset_metadata']
        asset_params = {
            'binding_uid' : self._binding_id,
            'source_uid' : asset_details_dict['source_uid'],
            'input_data_type' : self._get_input_data_type_object(asset_metadata['input_data_type']),
            'problem_type' : self._get_problem_type_object(asset_metadata['problem_type']),
            'label_column' : asset_metadata['label_column'],
            'prediction_column' : asset_metadata['prediction_column'],
            'feature_columns' : asset_metadata['feature_columns'],
            'categorical_columns' : asset_metadata['categorical_columns']
        }
        if self._model.training_data_reference:
            asset_params['training_data_reference'] = self._model.training_data_reference
        ml_asset = None
        if self._args.ml_engine_type is MLEngineType.WML:
            asset_params['probability_column'] = asset_metadata['probability_column']
            ml_asset = WatsonMachineLearningAsset( **asset_params )
        elif self._args.ml_engine_type is MLEngineType.AZUREML:
            asset_params['probability_column'] = asset_metadata['probability_column']
            ml_asset = AzureMachineLearningAsset( **asset_params )
        elif self._args.ml_engine_type is MLEngineType.SPSS:
            asset_params['class_probability_columns'] = asset_metadata['class_probability_columns']
            ml_asset = SPSSMachineLearningAsset( **asset_params )
        elif self._args.ml_engine_type is MLEngineType.CUSTOM:
            asset_params['probability_column'] = asset_metadata['probability_column']
            ml_asset = CustomMachineLearningAsset( **asset_params )
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            asset_params['probability_column'] = asset_metadata['probability_column']
            ml_asset = SageMakerMachineLearningAsset( **asset_params )
        start = time.time()
        self._subscription = self._client.data_mart.subscriptions.add(ml_asset)
        elapsed = time.time() - start
        self._asset_details_dict = asset_details_dict
        logger.info('Subscription completed successfully')
        logger.debug('TIMER: data_mart.subscriptions.add in {:.3f} seconds'.format(elapsed))

    def _get_input_data_type_object(self, data):
        if data == 'structured':
            return InputDataType.STRUCTURED
        return None

    def _get_problem_type_object(self, data):
        if data == 'binary':
            return ProblemType.BINARY_CLASSIFICATION
        elif data == 'multiclass':
            return ProblemType.MULTICLASS_CLASSIFICATION
        elif data == 'regression':
            return ProblemType.REGRESSION
        return None

    @retry(tries=5, delay=8, backoff=2)
    def configure_subscription(self):
        '''
        Configure payload logging plus performance, fairness, explainability, and accuracy monitoring
        '''
        logger.info('Enablng payload logging ...')
        start = time.time()
        self._subscription.payload_logging.enable()
        elapsed = time.time() - start
        logger.debug('TIMER: subscription.payload_logging.enable in {:.3f} seconds'.format(elapsed))
        logger.info('Payload logging enabled successfully')

        logger.info('Enabling performance monitoring ...')
        start = time.time()
        self._subscription.performance_monitoring.enable()
        elapsed = time.time() - start
        logger.debug('TIMER: subscription.performance_monitoring.enable in {:.3f} seconds'.format(elapsed))
        logger.info('Performance monitoring enabled successfully')

    def configure_subscription_monitors(self):
        def _get_config_params(param_key_name):
            params = self._model.configuration_data[param_key_name]
            param_name = param_key_name.split('_')[0]
            if not params:
                logger.info('{} configuration not available for this model'.format(param_name))
            else:
                logger.info('Configuring {} ...'.format(param_name))
            return params
        self.configure_fairness(_get_config_params('fairness_configuration'))
        self.configure_quality(_get_config_params('quality_configuration'))
        self.add_feedback_data()
        self.configure_explainability()

    @retry(tries=5, delay=8, backoff=2)
    def configure_fairness(self, params):
        if params:
            if self._fairness_run_once: # in case of retry
                feature_list = []
                for elem in params['features']:
                    feature_list.append(Feature(elem['feature'], elem['majority'], elem['minority'], float(elem['threshold'])))
                params['features'] = feature_list
                if not self._model.training_data_reference:
                    if self._model.training_data_statistics:
                        params['training_data_statistics'] = self._model.training_data_statistics
                    else:
                        params['training_data'] = self._model.training_data
                self._fairness_run_once = False
            start = time.time()
            self._subscription.fairness_monitoring.enable(**params)
            elapsed = time.time() - start
            logger.debug('TIMER: subscription.fairness_monitoring.enable in {:.3f} seconds'.format(elapsed))
            logger.info('Fairness configured successfully')

    @retry(tries=5, delay=8, backoff=2)
    def configure_quality(self, params):
        if params:
            start = time.time()
            self._subscription.quality_monitoring.enable(**params)
            elapsed = time.time() - start
            logger.debug('TIMER: subscription.quality_monitoring.enable in {:.3f} seconds'.format(elapsed))
            logger.info('Quality configured successfully')

    @retry(tries=5, delay=8, backoff=2)
    def add_feedback_data(self):
        logger.info('Adding feedback data ...')
        start = time.time()
        self._subscription.feedback_logging.store(self._model.feedback_data, feedback_format=FeedbackFormat.DICT)
        elapsed = time.time() - start
        logger.debug('TIMER: subscription.feedback_logging.store in {:.3f} seconds'.format(elapsed))
        logger.info('Feedback data added successfully')

    @retry(tries=5, delay=8, backoff=2)
    def configure_explainability(self):
        logger.info('Configuring explainability ...')
        params = {}
        if self._explainability_run_once: # in case of retry
            if not self._model.training_data_reference:
                if self._model.training_data_statistics:
                    params['training_data_statistics'] = self._model.training_data_statistics
                else:
                    params['training_data'] = self._model.training_data
            self._explainability_run_once = False
        start = time.time()
        self._subscription.explainability.enable(**params)
        elapsed = time.time() - start
        logger.debug('TIMER: subscription.explainability.enable in {:.3f} seconds'.format(elapsed))
        logger.info('Explainability configured successfully')

    def generate_sample_metrics(self):
        if self._args.history > 0:
            logger.info('Loading historical performance metrics to {} ...'.format(self._args.service_name))
            for day in range(self._args.history):
                logger.info(' - Loading day {}'.format(day + 1))
                history = self._model.get_performance_history(day)
                self.reliable_post_metrics('performance', history)
            logger.info('Historical performance metrics loaded successfully')

            logger.info('Loading historical fairness metrics to {} ...'.format(self._args.service_name))
            for day in range(self._args.history):
                logger.info(' - Loading day {}'.format(day + 1))
                history = self._model.get_fairness_history(day)
                self.reliable_post_metrics('fairness', history)
            logger.info('Historical fairness metrics loaded successfully')

            logger.info('Loading historical debiased fairness metrics to {} ...'.format(self._args.service_name))
            for day in range(self._args.history):
                logger.info(' - Loading day {}'.format(day + 1))
                history = self._model.get_debias_history(day)
                self.reliable_post_metrics('debiased_fairness', history)
            logger.info('Historical debiased fairness metrics loaded successfully')

            logger.info('Loading historical quality metrics to {} ...'.format(self._args.service_name))
            for day in range(self._args.history):
                logger.info(' - Loading day {}'.format(day + 1))
                history = self._model.get_quality_history(day)
                self.reliable_post_metrics('quality', history)
            logger.info('Historical quality metrics loaded successfully')

            logger.info('Loading historical manual labeling data to {} ...'.format(self._args.service_name))
            for day in range(self._args.history):
                logger.info(' - Loading day {}'.format(day + 1))
                history = self._model.get_manual_labeling_history(day)
                self.reliable_post_manual_labeling(history)
            logger.info('Historical manual labeling data loaded successfully')

    @retry(tries=5, delay=4, backoff=2)
    def generate_sample_scoring(self, engine_client, numscores=100):
        logger.info('Generating {} new scoring requests ...'.format(numscores))
        records_list = []
        if self._args.ml_engine_type is MLEngineType.WML:
            engine_client = self._client.data_mart.bindings.get_native_engine_client(binding_uid=self._binding_id)
            deployment_details = engine_client.deployments.get_details(self._asset_details_dict['source_entry_metadata_guid'])
            deployment_url = engine_client.deployments.get_scoring_url(deployment_details)
            if self._args.is_icp and ':31002' not in deployment_url:
                deployment_url_host = ':'.join(deployment_url.split(':')[:2])
                args_url_host = ':'.join(self._args.env_dict['aios_url'].split(':')[:2])
                deployment_url = deployment_url.replace('{}:16600'.format(deployment_url_host), '{}:31002'.format(args_url_host))
            for _ in range(numscores):
                fields, values = self._model.get_score_input()
                score_input = {'fields': fields, 'values': values }
                start = time.time()
                engine_client.deployments.score(deployment_url, score_input)
                elapsed = time.time() - start
                logger.debug('TIMER: WML deployments.score in {:.3f} seconds'.format(elapsed))
        elif self._args.ml_engine_type is MLEngineType.AZUREML:
            engine_client.setup_scoring_metadata(self._subscription)
            for _ in range(numscores):
                fields, values = self._model.get_score_input()
                values = values[0]
                value_dict = {}
                for (index, field) in enumerate(fields):
                    value_dict[field] = values[index]
                start = time.time()
                record = engine_client.score({'Inputs':{'input1': [value_dict] },'GlobalParameters':{}})
                elapsed = time.time() - start
                logger.debug('TIMER: AzureML score in {:.3f} seconds'.format(elapsed))
                records_list.append(record)
        elif self._args.ml_engine_type is MLEngineType.SPSS:
            engine_client.setup_scoring_metadata(self._subscription)
            subscription_details = self._subscription.get_details()
            model_name_id = subscription_details['entity']['asset']['name']
            input_table_id = subscription_details['entity']['asset_properties']['input_data_schema']['id']
            for _ in range(numscores):
                spss_data = {'requestInputTable':[{'id': input_table_id, 'requestInputRow':[{'input':[]}]}],'id':model_name_id}
                fields, values = self._model.get_score_input()
                values = values[0]
                value_dict = {}
                for (index, field) in enumerate(fields):
                    entry_dict = {'name':str(field),'value':str(values[index])}
                    spss_data['requestInputTable'][0]['requestInputRow'][0]['input'].append(entry_dict)
                start = time.time()
                record = engine_client.score(spss_data)
                elapsed = time.time() - start
                logger.debug('TIMER: SPSS score in {:.3f} seconds'.format(elapsed))
                records_list.append(record)
        elif self._args.ml_engine_type is MLEngineType.CUSTOM:
            engine_client.setup_scoring_metadata(self._subscription)
            for _ in range(numscores):
                fields, values = self._model.get_score_input()
                score_input = {'fields': fields, 'values': values }
                start = time.time()
                record = engine_client.score(score_input)
                elapsed = time.time() - start
                logger.debug('TIMER: Custom score in {:.3f} seconds'.format(elapsed))
                records_list.append(record)
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            records_list = []
            engine_client.setup_scoring_metadata(self._subscription)
            for _ in range(numscores):
                fields, values = self._model.get_score_input_sagemaker()
                start = time.time()
                record = engine_client.score(fields, values)
                elapsed = time.time() - start
                logger.debug('TIMER: Sagemaker score in {:.3f} seconds'.format(elapsed))
                records_list.append(record)
        if records_list:
            start = time.time()
            self._subscription.payload_logging.store(records=records_list)
            elapsed = time.time() - start
            logger.debug('TIMER: subscription.payload_logging.store in {:.3f} seconds'.format(elapsed))
        logger.debug('DEBUG: Pause 5 seconds to allow payload logging to complete')
        time.sleep(5.0)
        logger.info('Scoring requests generated successfully')

    def trigger_monitors(self):
        background_mode = not self._args.sync_checks
        logger.info('Triggering immediate fairness check ...')
        params = self._model.configuration_data['fairness_configuration']
        if params == 'None':
            logger.info('Skip fairness check for model')
        else:
            start = time.time()
            self._subscription.fairness_monitoring.run(background_mode=background_mode)
            elapsed = time.time() - start
            logger.debug('TIMER: subscription.fairness_monitoring.run in {:.3f} seconds'.format(elapsed))
            logger.info('Fairness check triggered successfully')

        logger.info('Triggering immediate quality check ...')
        quality_monitoring_params = self._model.configuration_data['quality_configuration']
        if quality_monitoring_params == 'None':
            logger.info('Skip quality check for model')
        else:
            start = time.time()
            self._subscription.quality_monitoring.run(background_mode=background_mode)
            elapsed = time.time() - start
            logger.debug('TIMER: subscription.quality_monitoring.run in {:.3f} seconds'.format(elapsed))
            logger.info('Quality check triggered successfully')

    @retry(tries=5, delay=4, backoff=2)
    def payload_logging(self):
        logger.info('Loading historical payload records to {} ...'.format(self._args.service_name))
        records = None
        for day in range(1 if self._args.history == 0 else self._args.history):
            if self._args.history > 0:
                logger.info(' - Loading day {}'.format(day + 1))
            records = self._model.get_payload_history(day)
            start = time.time()
            self._subscription.payload_logging.store(records=records)
            elapsed = time.time() - start
            logger.debug('TIMER: subscription.payload_logging.store in {:.3f} seconds'.format(elapsed))
        logger.debug('DEBUG: Pause 5 seconds to allow payload logging to complete')
        time.sleep(5.0)
        logger.info('Historical payload records loaded successfully'.format(self._args.service_name))

    @retry(tries=5, delay=4, backoff=2)
    def reliable_post_metrics(self, metric_type, records):
        '''
        Retry the loading metrics so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        if not records:
            logger.debug('No {} history available to load'.format(metric_type))
            return
        metrics_url = '{0}/v1/data_marts/{1}/metrics'.format(self._credentials['url'], self._credentials['data_mart_id'])
        iam_headers = get_iam_headers(self._credentials, self._args.env_dict)
        deployment_guid = None
        model_guid = None
        model_guid = self._asset_details_dict['source_uid']
        deployment_guid = self._asset_details_dict['source_entry_metadata_guid']
        record_json = []
        for record in records:
            # update historical manual labeling table reference to be correct
            if metric_type in ['fairness', 'debiased_fairness']:
                if 'manual_labelling_store' in record:
                    record['manual_labelling_store'] = 'Manual_Labeling_' + model_guid
            record_json.append( {
                'binding_id': self._binding_id,
                'metric_type': metric_type,
                'timestamp': record['timestamp'],
                'subscription_id': model_guid,
                'asset_revision': model_guid,
                'value': record['value'],
                'deployment_id': deployment_guid
            })
        start = time.time()
        response = requests.post(metrics_url, json=record_json, headers=iam_headers, verify=self._verify)
        elapsed = time.time() - start
        logger.debug('TIMER: post data_mart {} metrics in {:.3f} seconds'.format(metric_type, elapsed))
        words = ['error', 'exception']
        if any(word in str(response.json()) for word in words):
            logger.warning('WARNING: while posting {} metrics: {}'.format(metric_type, str(response.json())))

    @retry(tries=5, delay=4, backoff=2)
    def reliable_post_manual_labeling(self, records):
        '''
        Retry the loading so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        if not records:
            logger.debug('No manual labeling history available to load')
            return
        manual_labeling_url = '{0}/v1/data_marts/{1}/manual_labelings'.format(self._credentials['url'], self._credentials['data_mart_id'])
        iam_headers = get_iam_headers(self._credentials, self._args.env_dict)

        binding_id = self._binding_id
        model_guid = self._asset_details_dict['source_uid']
        deployment_guid = self._asset_details_dict['source_entry_metadata_guid']

        record_json = []
        for record in records:
            # update the record to include required metadata
            record['binding_id'] = binding_id
            record['subscription_id'] = model_guid
            record['asset_revision'] = model_guid
            record['deployment_id'] = deployment_guid
            record_json.append(record)
        start = time.time()
        response = requests.post(manual_labeling_url, json=record_json, headers=iam_headers, verify=self._verify)
        elapsed = time.time() - start
        logger.debug('TIMER: post data_mart manual_labeling history in {:.3f} seconds'.format(elapsed))
        words = ['error', 'exception']
        if any(word in str(response.json()) for word in words):
            logger.warning('WARNING: while posting manual labeling history: {}'.format(str(response.json())))

    def get_asset_details(self, name):
        logger.info('Retrieving assets ...')
        asset_details = self._client.data_mart.bindings.get_asset_details()
        asset_details_dict = {}
        for detail in asset_details:
            if name in detail['name']:
                if self._args.ml_engine_type is MLEngineType.SPSS:
                    asset_details_dict['id'] = detail['name']
                asset_details_dict['binding_uid'] = detail['binding_uid']
                asset_details_dict['source_uid'] = detail['source_uid']
                if self._args.ml_engine_type is not MLEngineType.WML: # For WML, the scoring URL is not in the asset
                    asset_details_dict['scoring_url'] = detail['source_entry']['entity']['scoring_endpoint']['url']
                asset_details_dict['source_entry_metadata_guid'] = detail['source_entry']['metadata']['guid']
                break
        if not 'source_uid' in asset_details_dict:
            logger.error('ERROR: Could not find a deployment with the name: {}'.format(name))
            exit(1)
        return asset_details_dict
