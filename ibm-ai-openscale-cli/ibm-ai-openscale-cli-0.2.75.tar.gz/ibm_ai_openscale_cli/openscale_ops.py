# coding=utf-8
from __future__ import print_function
from ibm_ai_openscale_cli.utility_classes.fastpath_logger import FastpathLogger
from ibm_ai_openscale_cli.enums import ResetType, MLEngineType
from ibm_ai_openscale_cli.openscale.openscale_client import OpenScaleClient
from ibm_ai_openscale_cli.ops import Ops

logger = FastpathLogger(__name__)

class OpenScaleOps(Ops):

    def __init__(self, args):
        super().__init__(args)
        self._model_names = Ops._wml_modelnames

    def _validate_model_name(self):
        def _is_model_name_valid(valid_names_list):
            if self._args.model not in valid_names_list:
                error_msg = 'Invalid model name specified. Only the following models are supported {}: {}'.format(self._args.ml_engine_type.value, valid_names_list)
                logger.log_error(error_msg)
                raise Exception(error_msg)
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
            error_msg = 'Custom model must specify --custom-model-directory'
            logger.log_error(error_msg)
            raise Exception(error_msg)
        if self._args.custom_model_directory and not self._args.custom_model:
            error_msg = 'Custom model must specify --custom-model model name'
            logger.log_error(error_msg)
            raise Exception(error_msg)

    def _model_validations(self):
        if self._args.custom_model or self._args.custom_model_directory:
            self._validate_custom_model()
            self._model_names = [self._args.custom_model]
            self._args.model = self._args.custom_model
        elif self._args.model != 'all':
            self._validate_model_name()
            self._model_names = [self._args.model]

    def _instantiate_openscale_client(self):
        openscale_credentials = self._credentials.get_openscale_credentials()
        database_credentials = self._credentials.get_database_credentials()
        openscale_client = OpenScaleClient(self._args, openscale_credentials, database_credentials)
        if not self._args.is_icp:
            logger.log_debug('Watson OpenScale data mart id: {}'.format(openscale_credentials['data_mart_id']))
        return openscale_client

    def _reset_datamart(self, openscale_client):
        if not self._args.extend:
            openscale_client.reset(ResetType.DATAMART)
            openscale_client.create_datamart()
            ml_engine_credentials = self._credentials.get_ml_engine_credentials()
            openscale_client.bind_mlinstance(ml_engine_credentials)

    def execute(self):

        # validations
        self._model_validations()

        # credentials
        openscale_client = self._instantiate_openscale_client()

        # Instantiate ml engine
        ml_engine = self.get_ml_engine_instance()

        # reset datamart
        self._reset_datamart(openscale_client)

        modeldata = None
        run_once = True
        for modelname in self._model_names:
            logger.log_info('--------------------------------------------------------------------------------')
            logger.log_info('Model: {}, Engine: {}'.format(modelname, self._args.ml_engine_type.value))
            logger.log_info('--------------------------------------------------------------------------------')
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
                if self._args.history_only:
                    openscale_client.use_existing_subscription(asset_details_dict)
                else:
                    openscale_client.subscribe_to_model_deployment(asset_details_dict)
                    openscale_client.generate_sample_scoring(ml_engine, numscores=1, values_per_score=1, to_init_payload_logging=True)
                    openscale_client.configure_subscription_monitors()
                openscale_client.generate_sample_metrics()
                openscale_client.generate_sample_scoring(ml_engine, numscores=self._args.num_scores, values_per_score=self._args.values_per_score)
                openscale_client.trigger_monitors()
