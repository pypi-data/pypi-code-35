# coding=utf-8
from __future__ import print_function
import logging
from ibm_ai_openscale_cli.enums import ResetType, MLEngineType
from ibm_ai_openscale_cli.openscale.openscale_client import OpenScaleClient
from ibm_ai_openscale_cli.openscale.openscale_reset import ResetType
from ibm_ai_openscale_cli.ops import Ops

logger = logging.getLogger(__name__)

class OpenScaleOps(Ops):

    def __init__(self, args):
        super().__init__(args)
        self._model_names = Ops._wml_modelnames

    def _validate_model_name(self):
        def _is_model_name_valid(valid_names_list):
            if self._args.model not in valid_names_list:
                logger.error('Invalid model name specified. Only the following models are supported {}: {}'.format(self._args.ml_engine_type.value, valid_names_list))
                exit(1)
        if self._args.ml_engine_type is MLEngineType.AZUREML:
            _is_model_name_valid(valid_names_list=Ops._azure_modelnames)
        elif self._args.ml_engine_type is MLEngineType.SPSS:
            _is_model_name_valid(valid_names_list=Ops._spss_modelnames)
        elif self._args.ml_engine_type is MLEngineType.CUSTOM:
            _is_model_name_valid(valid_names_list=Ops._custom_modelnames)
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            _is_model_name_valid(valid_names_list=Ops._sagemaker_modelnames)
        elif self._args.ml_engine_type is MLEngineType.WML:
            _is_model_name_valid(valid_names_list=Ops._wml_modelnames)

    def _validate_custom_model(self):
        if self._args.custom_model and not self._args.custom_model_directory:
            logger.error('Custom model {} must also specify a model directory'.format(self._args.custom_model))
            exit(1)
        elif not self._args.custom_model and self._args.custom_model_directory:
            logger.error('Custom model name must also be specified for custom model directory {}'.format(self._args.custom_model_directory))
            exit(1)

    def execute(self):

        # validations
        if self._args.custom_model or self._args.custom_model_directory:
            self._validate_custom_model()
            self._model_names = [self._args.custom_model]
            self._args.model = self._args.custom_model
        elif self._args.model != 'all':
            self._validate_model_name()
            self._model_names = [self._args.model]

        # instantiate openscale
        openscale_credentials = self._credentials.get_openscale_credentials()
        database_credentials = self._credentials.get_database_credentials()
        openscale_client = OpenScaleClient(self._args, openscale_credentials, database_credentials)
        if not self._args.is_icp:
            logger.debug('Watson OpenScale data mart id: {}'.format(openscale_credentials['data_mart_id']))

        # Instantiate ml engine
        logger.info('Using {}'.format(self._args.ml_engine_type.value))
        ml_engine = self.get_ml_engine_instance()

        # reset datamart if not extending
        if not self._args.extend:
            openscale_client.reset(ResetType.DATAMART)
            openscale_client.create_datamart()
            ml_engine_credentials = self._credentials.get_ml_engine_credentials()
            openscale_client.bind_mlinstance(ml_engine_credentials)

        modeldata = None
        run_once = True
        for modelname in self._model_names:
            logger.info('--------------------------------------------------------------------------------')
            logger.info('Model: {}, Engine: {}'.format(modelname, self._args.ml_engine_type.value))
            logger.info('--------------------------------------------------------------------------------')
            for model_instance_num in range(self._args.model_first_instance, self._args.model_first_instance + self._args.model_instances):

                # model instance
                modeldata = self.get_modeldata_instance(modelname, model_instance_num)
                openscale_client.set_model(modeldata)

                asset_details_dict = None
                # ml engine instance
                if self._args.ml_engine_type is MLEngineType.WML:
                    ml_engine.set_model(modeldata)
                    if not self._args.deployment_name:
                        asset_details_dict = ml_engine.create_model_and_deploy()
                    else:
                        asset_details_dict = ml_engine.get_existing_deployment(self._args.deployment_name)
                else:
                    asset_details_dict = openscale_client.get_asset_details(self._args.deployment_name)

                if self._args.extend and run_once:
                    run_once = False
                    openscale_client.use_existing_binding(asset_details_dict)

                # ai openscale operations
                openscale_client.subscribe_to_model_deployment(asset_details_dict)
                openscale_client.configure_subscription()
                openscale_client.payload_logging()
                openscale_client.configure_subscription_monitors()
                openscale_client.generate_sample_metrics()
                openscale_client.generate_sample_scoring(ml_engine)
                openscale_client.trigger_monitors()
