import django
from django.conf import settings
from django.test import Client as DjangoClient
from django.urls import reverse
from unittest import TestCase
try:
    from unittest import mock
except Exception:
    import mock

from stackifyapm.base import Client
from stackifyapm.instrumentation import control
from stackifyapm.contrib.django.tests.fixtures.testapp.settings import TEST_SETTINGS
from stackifyapm.contrib.django.apps import register_handlers

CONFIG = {
    "SERVICE_NAME": "service_name",
    "ENVIRONMENT": "production",
    "HOSTNAME": "sample_host",
    "FRAMEWORK_NAME": "framework",
    "FRAMEWORK_VERSION": "1.0",
    "APPLICATION_NAME": "sample_application",
    "BASE_DIR": "path/to/application/",
}


class StackifyAPMConfigTest(TestCase):
    def setUp(self):
        self.client = Client(**CONFIG)
        if not settings.configured:
            settings.configure(**TEST_SETTINGS)
            django.setup()

        # mock setup logging so it will not log any traces
        self.setup_logging = mock.patch('stackifyapm.contrib.flask.setup_logging')
        self.setup_logging.start()

        self.django_client = DjangoClient()

    def tearDown(self):
        control.uninstrument()
        self.setup_logging.stop()

    def test_begin_transaction(self):
        begin_transaction = mock.patch('stackifyapm.base.Client.begin_transaction')
        mock_begin_transaction = begin_transaction.start()
        register_handlers(self.client)

        self.django_client.get(reverse('index'))

        assert mock_begin_transaction.called
        assert mock_begin_transaction.call_args_list[0][0][0] == 'request'

        begin_transaction.stop()

    def test_end_transaction(self):
        end_transaction = mock.patch('stackifyapm.base.Client.end_transaction')
        mock_end_transaction = end_transaction.start()
        register_handlers(self.client)

        self.django_client.get(reverse('index'))

        assert mock_end_transaction.called

        end_transaction.stop()
