import unittest
from pynosql.credentials.base_credentials import InvalidCredentials
from pynosql.credentials.aws import AWSCredentials
from pynosql.credentials.mongo import MongoDBSSLCredentials, MongoDBCredentials


class TestSetup(unittest.TestCase):
    """ Credentials Test """

    def test_valid_aws_credentials(self):
        """ Test valid AWS Credentials """
        try:
            AWSCredentials(
                'AKIAIOSFODNN7EXAMPLE',
                'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
            )
        except InvalidCredentials:
            self.fail('Unexpected exception initializing AWSCredentials')

    def test_invalid_aws_credentials(self):
        """ Test invalid AWS Credentials """
        try:
            AWSCredentials(
                None,
                'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
            )
            self.fail('Expected AWSCredentials exception did not occur.')
        except InvalidCredentials:
            return

    def test_valid_mongo_basic_credentials(self):
        """ Test basic username and password MongoDB credentials """
        try:
            MongoDBCredentials('test', 'user', 'mysource', 'mymechanism')
        except InvalidCredentials:
            self.fail('Unexpected exception initializing MongoDBCredentials')

    def test_valid_mongo_ssl_credentials(self):
        """ Test valid MongoDB SSL credentials """
        try:
            ssl_creds = MongoDBSSLCredentials(
                '/my/cert.pem',
                MongoDBSSLCredentials.SSL.CERT_REQUIRED,
                'my/ca.pem'
            )
            MongoDBCredentials(ssl_obj=ssl_creds)
        except InvalidCredentials:
            self.fail('Unexpected exception initializing MongoDBCredentials')

    def test_invalid_mongo_ssl_credentials(self):
        """ Test invalid MongoDB SSL credentials """
        try:
            MongoDBSSLCredentials(
                None,
                MongoDBSSLCredentials.SSL.CERT_REQUIRED,
                'my/ca.pem'
            )
            self.fail(
                'Expected MongoDBSSLCredentials exception did not occur.')
        except InvalidCredentials:
            return

    def test_invalid_mongo_credentials(self):
        """ Test invalid MongoDB credentials """
        try:
            MongoDBCredentials(ssl_obj='testing')
            self.fail('Expected MongoDBCredentials exception did not occur.')
        except InvalidCredentials:
            return
