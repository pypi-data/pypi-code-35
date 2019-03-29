from app.example_views import ExampleView
from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory
from flask import json

from datetime import date, datetime
from decimal import Decimal

import uuid

URLS = (
    ('/<uuid:key>', ExampleView, 'home_key'),
    ('/', ExampleView, 'home'),
)


class TestExampleEndpoints(FlaskPhiloTestCase):
    def setup(self):
        self.app = BaseTestFactory.create_test_app(urls=URLS)
        self.client = self.app.test_client()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def test_get_example(self):
        result = self.client.get('/', headers=self.headers)
        assert 200 == result.status_code
        j_content = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in j_content
        assert 'ok' == j_content['msg']

    def test_post_example(self):
        result = self.client.post('/', data='{}', headers=self.headers)
        assert 400 == result.status_code

        data = {
            'key': uuid.uuid4(),
            'msg': 'ok_post',
            'value': Decimal(666.666),
            'date': date.today().isoformat(),
            'date-time': datetime.utcnow().astimezone().isoformat()
        }

        result = self.client.post(
            '/', headers=self.headers, data=json.dumps(data))
        assert 201 == result.status_code
        j_content = json.loads(result.get_data().decode('utf-8'))
        assert 'ok_post' == j_content['msg']

    def test_put_example(self):
        result = self.client.put('/', data='{}', headers=self.headers)
        assert 400 == result.status_code

        data = {
            'key': uuid.uuid4(),
            'msg': 'ok_post',
            'value': Decimal(666.666),
            'date': date.today().isoformat(),
            'date-time': datetime.utcnow().astimezone().isoformat()
        }

        result = self.client.put(
            '/{}'.format(data['key']),
            headers=self.headers, data=json.dumps(data))
        assert 200 == result.status_code
        j_content = json.loads(result.get_data().decode('utf-8'))
        assert 'ok_post' == j_content['msg']

    def test_delete_example(self):
        result = self.client.delete('/', headers=self.headers)
        assert 400 == result.status_code

        result = self.client.delete(
            '/{}'.format(uuid.uuid4()), headers=self.headers)
        assert 200 == result.status_code
