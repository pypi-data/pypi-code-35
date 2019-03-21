# coding=utf-8
import logging
import json
import time
import requests
from ibm_ai_openscale.supporting_classes import PayloadRecord
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class CustomMachineLearningEngine:

    _auth = None

    def __init__(self, credentials):
        self._credentials = credentials
        if 'username' in self._credentials and 'password' in self._credentials:
            CustomMachineLearningEngine._auth=HTTPBasicAuth(username=self._credentials['username'], password=self._credentials['password'] )

    def setup_scoring_metadata(self, subscription):
        subscription_details = subscription.get_details()
        CustomMachineLearningEngine._scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

    def score(self, data):
        body = str.encode(json.dumps(data))
        headers = {'Content-Type': 'application/json'}
        start_time = time.time()
        response = requests.post(url=CustomMachineLearningEngine._scoring_url, data=body, headers=headers, auth=CustomMachineLearningEngine._auth)
        response_time = time.time() - start_time
        if 'error' in str(response.json()):
           logger.warning('WARN: Found error in scoring response: {}'.format(str(response.json)))
        record = PayloadRecord(request=data, response=response.json(), response_time=int(response_time))
        return record