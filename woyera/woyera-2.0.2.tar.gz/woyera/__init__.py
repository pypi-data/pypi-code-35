name = "woyera"

import requests
import json

class API:

    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.url = "https://www.woyera.com/api/"
        self.result_url = "https://www.woyera.com/api/get-results/"
        self.results = None
        self.job_id = None

    def run_defect_process(self, data, columnNames=None, defectFunctions=None):
        data_dict = {'data': data}

        request_body = self.add_to_request_body(data_dict, columnNames, defectFunctions)

        r = requests.post(self.url, json=json.loads(json.dumps(request_body)),
                          headers={'accessKey': self.accessKey, 'secretKey': self.secretKey})

        status_code = r.status_code
        json_response = r.json()

        if status_code == 200:
            self.job_id = json_response['jobID']

        return r

    def get_results(self, job_id):
        r = requests.post(self.result_url, json=json.loads(json.dumps({'jobID': job_id})),
                          headers={'accessKey': self.accessKey, 'secretKey': self.secretKey})


        return r


    def add_to_request_body(self, data, columnNames, defectFunctions):
        if columnNames is not None:
            data['columnNames'] = columnNames

        if defectFunctions is not None:
            data['defectFunctions'] = defectFunctions

        return data