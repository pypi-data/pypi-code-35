# coding=utf-8
import logging
import time
import requests
from ibm_ai_openscale.supporting_classes import PayloadRecord
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class SPSSMachineLearningEngine:

    def __init__(self, credentials):
        SPSSMachineLearningEngine._auth = HTTPBasicAuth( username=credentials['username'], password=credentials['password'] )

    def setup_scoring_metadata(self, subscription):
        subscription_details = subscription.get_details()
        SPSSMachineLearningEngine._scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

    def score(self, data):
        start_time = time.time()
        response = requests.post(url=SPSSMachineLearningEngine._scoring_url, json=data, auth=SPSSMachineLearningEngine._auth)
        response_time = time.time() - start_time
        if 'error' in str(response.json()):
           logger.warning('WARN: Found error in scoring response: {}'.format(str(response.json)))
        record = PayloadRecord(request=data, response=response.json(), response_time=int(response_time))
        return record