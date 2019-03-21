from flask import Flask
from flask import jsonify
from unittest import TestCase
try:
    from unittest import mock
except Exception:
    import mock

from stackifyapm.base import Client
from stackifyapm.contrib.flask import make_client
from stackifyapm.contrib.flask import StackifyAPM
from stackifyapm.instrumentation import control


class MakeClientTest(TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['ENV'] = 'test'

    def test_should_return_client(self):
        client = make_client(self.app)

        assert isinstance(client, Client)

    def test_client_config(self):
        client = make_client(self.app)

        assert client.config.application_name == 'tests'
        assert client.config.environment == 'test'
        assert client.config.framework_name == 'flask'
        assert client.config.framework_version


class StackifyAPMTest(TestCase):
    def setUp(self):
        # mock setup logging so it will not log any traces
        self.setup_logging = mock.patch('stackifyapm.contrib.flask.setup_logging')
        self.setup_logging.start()

        self.app = Flask('asfadsa')
        self.app.config['ENV'] = 'test'

        @self.app.route('/', methods=['GET'])
        def index():
            return jsonify(result='index')

        @self.app.route('/exception', methods=['GET'])
        def exception():
            1 / 0

    def tearDown(self):
        control.uninstrument()
        self.setup_logging.stop()

    def test_begin_transaction(self):
        begin_transaction = mock.patch('stackifyapm.base.Client.begin_transaction')
        mock_begin_transaction = begin_transaction.start()
        StackifyAPM(self.app)

        self.app.test_client().get('/')

        assert mock_begin_transaction.called
        assert mock_begin_transaction.call_args_list[0][0][0] == 'request'

        begin_transaction.stop()

    def test_end_transaction(self):
        end_transaction = mock.patch('stackifyapm.base.Client.end_transaction')
        mock_end_transaction = end_transaction.start()
        StackifyAPM(self.app)

        self.app.test_client().get('/')

        assert mock_end_transaction.called

        end_transaction.stop()

    def test_capture_exception(self):
        capture_exception = mock.patch('stackifyapm.base.Client.capture_exception')
        end_transaction = mock.patch('stackifyapm.base.Client.end_transaction')
        mock_capture_exception = capture_exception.start()
        end_transaction.start()
        StackifyAPM(self.app)

        self.app.test_client().get('/exception')

        assert mock_capture_exception.called
        assert mock_capture_exception.call_args_list[0][1]['exception']
        assert mock_capture_exception.call_args_list[0][1]['exception']['frames']
        assert mock_capture_exception.call_args_list[0][1]['exception']['timestamp']
        assert mock_capture_exception.call_args_list[0][1]['exception']['exception']
        assert mock_capture_exception.call_args_list[0][1]['exception']['caughtBy']
        assert mock_capture_exception.call_args_list[0][1]['exception']['message']

        capture_exception.stop()
        end_transaction.stop()
