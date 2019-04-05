import logging
from apimas.errors import GenericException, InvalidInput
from django.db import transaction
import specular
from apimas_django.predicates import domain

runtimespec = domain.compile_spec({'.runtime.django': {}})

logger = logging.getLogger('apimas')


class ApimasAction(object):
    def __init__(self, collection, url, action_name, status_code, content_type,
                 processors):
        self.collection = collection
        self.action_name = action_name
        self.url = url
        self.status_code = status_code
        self.content_type = content_type
        self.processors = processors

    def handle_error(self, runtime, exc):
        status = exc.http_code if isinstance(exc, GenericException) \
                 else 500
        if status == 500:
            import traceback
            print traceback.format_exc()

        headers = getattr(exc, 'response_headers', {}) or {}
        details = getattr(exc, 'kwargs', {}).get('details')
        content = details if details else {'details': exc.message}
        response = {
            'response': {
                'content': specular.Data(content),
                'meta': {
                    'content_type': specular.Data(self.content_type),
                    'status_code': specular.Data(status),
                    'headers': specular.Data(headers),
                },
            },
        }
        runtime.insert(response)

    def process(self, request_data):
        runtime = specular.Runtime(runtimespec)
        for processor in self.processors:
            runtime.add_processor(processor)

        init_data = {
            'request': request_data,
            'response': {
                'meta': {
                    'content_type': specular.Data(self.content_type),
                    'status_code': specular.Data(self.status_code),
                },
            },
            'exportable': {
                'meta': specular.Data({})
            },
        }

        try:
            logger.info('Collection: %s, Action: %s',
                        self.collection, self.action_name)
            runtime.process_all(docdata=init_data)
        except Exception as exc:
            if isinstance(exc, specular.Error):
                err = exc.errs[0] if exc.errs else exc
            else:
                err = exc
            self.handle_error(runtime, err)

        return runtime
