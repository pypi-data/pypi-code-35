# coding=utf-8
from __future__ import print_function
import logging
from ibm_ai_openscale_cli.openscale.lg_openscale_client import LGOpenScaleClient
from ibm_ai_openscale_cli.ops import Ops
from ibm_ai_openscale_cli.openscale_ops import OpenScaleOps
from ibm_ai_openscale_cli.enums import MLEngineType

logger = logging.getLogger(__name__)

class LGOps(OpenScaleOps):

    def execute(self):

        # Instantiate ml engine
        ml_engine = self.get_ml_engine_instance()

        # instantiate openscale
        openscale_credentials = self._credentials.get_openscale_credentials()
        database_credentials = self._credentials.get_database_credentials()
        openscale_client = LGOpenScaleClient(self._args, openscale_credentials, database_credentials)

        # model instance
        modeldata = self.get_modeldata_instance(self._args.model, self._args.lg_model_instance_num)
        openscale_client.set_model(modeldata)

        # ml_engine instance
        asset_details_dict = None
        if self._args.ml_engine_type is MLEngineType.WML:
            ml_engine.set_model(modeldata)
            asset_details_dict = ml_engine.get_existing_deployment(self._args.deployment_name)
        else:
            asset_details_dict = openscale_client.get_asset_details(self._args.deployment_name)

        # ai openscale operations
        openscale_client.use_existing_binding(asset_details_dict)
        openscale_client.use_existing_subscription(asset_details_dict)
        openscale_client.generate_scoring_requests(ml_engine)
        openscale_client.generate_explain_requests()
        openscale_client.trigger_monitors()
