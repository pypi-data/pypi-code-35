import os

from decouple import config
from flask import Flask


class GwapApp(Flask):

    def __init__(self, import_name, **kwargs):
        os.environ['FLASK_ENV'] = config('GWAP_ENVIRONMENT', default='hml')
        os.environ['FLASK_DEBUG'] = config('DEBUG', default='False')
        super(GwapApp, self).__init__(import_name, **kwargs)

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        for rule in self.url_map.iter_rules():
            print(f' * Url: {rule.rule}, '
                  f'Resource: {self.view_functions[rule.endpoint].view_class.__name__}, '
                  f'Endpoint: {rule.endpoint}, '
                  f'Methods: {", ".join(rule.methods)}')
        super(GwapApp, self).run(host, port, debug, load_dotenv, **options)
