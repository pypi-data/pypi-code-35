# coding=utf-8
from __future__ import print_function
import logging
from ibm_ai_openscale_cli.openscale.openscale_client import OpenScaleClient
from ibm_ai_openscale_cli.enums import ResetType, MLEngineType
from ibm_ai_openscale_cli.ops import Ops

logger = logging.getLogger(__name__)

class ResetOps(Ops):

    def __init__(self, args):
        super().__init__(args)

    def _reset_model(self):
        ml_engine = self.get_ml_engine_instance()
        for modelname in Ops._wml_modelnames:
            logger.info('--------------------------------------------------------------------------------')
            logger.info('Model: {}, Engine: {}'.format(modelname, self._args.ml_engine_type.value))
            logger.info('--------------------------------------------------------------------------------')
            for model_instance_num in range(self._args.model_first_instance, self._args.model_first_instance + self._args.model_instances):
                modeldata = self.get_modeldata_instance(modelname, model_instance_num)
                ml_engine.set_model(modeldata)
                ml_engine.model_cleanup()

    def _reset_openscale(self):
        openscale_credentials = self._credentials.get_openscale_credentials()
        database_credentials = self._credentials.get_database_credentials()
        openscale_client = OpenScaleClient(self._args, openscale_credentials, database_credentials)
        openscale_client.reset(self._args.reset_type)

    def execute(self):
        if self._args.reset_type is ResetType.MODEL and self._args.ml_engine_type is MLEngineType.WML:
            self._reset_model()
        else:
            self._reset_openscale()
