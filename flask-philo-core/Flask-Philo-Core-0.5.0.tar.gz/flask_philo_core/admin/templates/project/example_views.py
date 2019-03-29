from flask_philo_core.views import BaseResourceView
from flask import request
from flask_philo_core.serializers import (
    uuid_schema, BaseSerializer
)

from datetime import date, datetime
from decimal import Decimal
from jsonschema import ValidationError

import uuid


class ExampleSerializer(BaseSerializer):
    _schema = inner_output_schema = {
        'type': 'object',
        'properties': {
            'key': uuid_schema,
            'msg': {'type': 'string'},
            'date': {'type': 'string', 'format': 'date'},
            'date-time': {'type': 'string', 'format': 'date-time'},
            'value': {'type': 'number'}
        },
        'required': [
            'key', 'msg', 'value', 'date'
        ]
    }


class ExampleView(BaseResourceView):
    def get(self):

        data = {
            'key': uuid.uuid4(),
            'msg': 'ok',
            'value': Decimal(666.666),
            'date': date.today(),
            'date-time': datetime.utcnow()
        }

        serializer = ExampleSerializer(data=data)
        return self.json_response(status=200, data=serializer.json)

    def post(self):
        try:
            serializer = ExampleSerializer(request=request)
            return self.json_response(status=201, data=serializer.json)

        except ValidationError as e:
            self.app.logger.error(e)
            return self.json_response(status=400)

    def put(self, key=None):
        try:
            serializer = ExampleSerializer(request=request)
            return self.json_response(status=200, data=serializer.json)

        except ValidationError as e:
            self.app.logger.error(e)
            return self.json_response(status=400)

    def delete(self, key=None):
        if key is None:
            return self.json_response(status=400)
        else:
            return self.json_response(status=200)
