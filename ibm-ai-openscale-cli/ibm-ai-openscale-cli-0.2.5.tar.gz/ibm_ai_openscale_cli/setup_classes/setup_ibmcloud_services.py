# coding=utf-8
from ibm_ai_openscale_cli.setup_classes.setup_services import SetupServices
import logging

logger = logging.getLogger(__name__)

class SetupIBMCloudServices(SetupServices):

    def __init__(self, args):
        super().__init__(args)

    def _aios_credentials(self, data_mart_id):
        aios_credentials = {}
        aios_credentials['apikey'] = self._args.apikey
        aios_credentials['url'] = self._args.env_dict['aios_url']
        aios_credentials['data_mart_id'] = data_mart_id
        return aios_credentials
