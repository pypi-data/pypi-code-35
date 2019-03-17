import unittest
from pynosql.credentials.base_credentials import InvalidCredentials
from pynosql.credentials.aws import AWSCredentials
from pynosql.clients.aws import AWSClient


class TestSetup(unittest.TestCase):
    """ Credentials Test """

    def test_valid_aws_client(self):
        """ Test valid AWS Credentials """
        try:
            credentials = AWSCredentials(
                'AKIAIOSFODNN7EXAMPLE',
                'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
            )
            AWSClient(credentials, 'us-west-2')
        except InvalidCredentials:
            self.fail('Unexpected exception initializing AWSClient')

    def test_invalid_aws_client_credentials(self):
        """ Test invalid AWS client credentials """

        try:
            credentials = "testing"
            AWSClient(credentials, 'us-west-2')
            self.fail('Expected InvalidCredentials exception did not ocurr.')
        except InvalidCredentials:
            pass
