from sciduct.sciduct_service import SciDuctServiceClientBase
import requests
import json
from urllib.parse import urljoin

class JobService(SciDuctServiceClientBase):
    """
    Job Service
    """

    __service_name__ = 'job'

    def _get_json(self, path):
        """
        Extend :py:func:`sciduct.sciduct_service._get` to check for errors, then
        return the json if there is none.
        """
        resp = self._get(path)
        return resp.json()

    def list(self):
        """
        :returns: A list of jobs.
        """
        return self._get_json('job/')

    def show(self, job_id):
        """
        :returns: Job with given id.
        """
        return self._get_json('job/' + job_id)

    def submit(self, name, definition, input_json, output):
        if type(name) is not str:
            raise TypeError('job name must be str')

        if type(definition) is not str:
            raise TypeError('job definition must be str') 

        if type(input_json) is str:
            input_json = json.loads(input_json)
        elif type(input_json) is not dict:
            raise TypeError('input must be json dict or str')

        if type(output) is not str:
            raise TypeError('output location must be str')

        new_job = {
            'output_name': name,
            'job_definition': definition,
            'input': input_json,
            'output_container': output
        }

        resp = self._post_json('job/', new_job, accept='application/json')
        return resp.json()

    def cancel(self, job):
        raise NotImplementedError('cancel is not implemented on the server side')

    def hold(self, job):
        raise NotImplementedError('hold is not implemented on the server side')

    def list_def(self):
        return self._get_json('job_definition/')

    def show_def(self, def_id):
        return self._get_json('job_definition/' + def_id)

    def create_jobdef(self, name, jd_type='task', description=None,
            ignore_stdout=False, ignore_stderr=False, schema=None):
        job_def = {
            'id': name, 
            'type': jd_type
        }

        if description is not None:
            job_def['description'] = description

        if ignore_stdout:
            job_def['ignore_stdout'] = True

        if ignore_stderr:
            job_def['ignore_stderr'] = True

        if schema is not None:
            job_def['input'] = schema

        resp = self._post_json('job_definition/', job_def,\
            accept='application/json')
        return resp.json()

    def modify_jobdef(self, name, **kwargs):
        patch_set = []

        def try_add_patch(key, op, path):
            if key in kwargs:
                patch = {
                    'op': op,
                    'path': path,
                    'value': kwargs['key']
                }

                patch_set.append(patch)

        try_add_patch('inputSchema', 'add', '/input')
        try_add_patch('output', 'add', '/output')
        try_add_patch('type', 'replace', '/type')
        try_add_patch('desc', 'replace', '/description')
        try_add_patch('ignoreStdout', 'add', '/ignore_stdout')
        try_add_patch('ignoreStderr', 'add', '/ignore_stderr')
        try_add_patch('enabled', 'replace', '/enabled')

        url = urljoin(self.url, 'job_definition/' + name)
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json-patch+json',
            'authorization': self.session.token
        }
        resp = requests.patch(url, headers=headers, json=patch_set)
        return resp
