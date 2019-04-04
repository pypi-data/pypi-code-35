from .dataclass import FieldConverter
from .dataclass import Schema
from .dataclass import Transmit
from .exceptions import EloquaError
from structlog import get_logger

import attr
import requests


@attr.s
class HandlerFactory:
    session: requests.Session = attr.ib()
    base_url: str = attr.ib()
    logger = attr.ib()

    @classmethod
    def get(cls, session: requests.Session):
        if not hasattr(cls, '_factory'):
            logger = get_logger()
            json_response = session.get('https://login.eloqua.com/id').json()
            if isinstance(json_response, str):
                logger.error(json_response)
                raise EloquaError(json_response)
            try:
                base_url = json_response['urls']['base']
            except KeyError as ex:
                logger.error(
                    'Eloqua returned unexpected json content', ex=ex,
                    problems=json_response
                )
                raise

            cls._factory = cls(
                session=session, base_url=base_url, logger=logger
            )
        return cls._factory

    def __call__(self, form_id):
        schema = Schema.from_id(
            form_id=form_id,
            base_url=self.base_url,
            session=self.session,
        )
        transmitter = Transmit.from_id(
            form_id=form_id,
            base_url=self.base_url,
            session=self.session,
        )

        return self._make_handler(schema, transmitter)

    def _make_handler(self, schema, transmitter):
        def handler(request_data):
            field_converter = None
            try:
                field_converter = FieldConverter.from_schema(schema())
                log = self.logger.bind(field_converter=field_converter)
                try:
                    data_to_send = field_converter(request_data)
                except KeyError:
                    json_response = {
                        'errors': 'Unknown field',
                        'field_mapping': field_converter.field_mapping
                    }
                    return json_response, 400
                log = log.bind(data_to_send=data_to_send)
                log.debug("Sending the data to send")
                transmitter(field_converter(request_data))
                return None, 201
            except requests.exceptions.RequestException as ex:
                json_response = {'errors': ex.response.json()}
                log.error('Unable to submit form', problems=json_response)
                if field_converter:
                    json_response['field_mapping'
                                  ] = field_converter.field_mapping
                return json_response, ex.response.status_code

        return handler
