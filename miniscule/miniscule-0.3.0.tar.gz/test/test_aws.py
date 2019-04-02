# pylint: disable=no-self-use
import mock
from botocore.exceptions import ClientError
from miniscule import load_config


@mock.patch('boto3.client')
class TestSecretsManagerConstructor:
    @staticmethod
    def mock_client(secret_string):
        client = mock.Mock()
        client.get_secret_value.return_value = {'SecretString': secret_string}
        return client

    def test_parses_json(self, client):
        client.return_value = self.mock_client(
            '{"user": "<user>", "password": "<password>"}')
        assert load_config('!aws/sm secret') == \
            {'user': '<user>', 'password': '<password>'}

    def test_correct_client_created(self, client):
        client.return_value = self.mock_client('')
        load_config('!aws/sm secret')
        client.return_value.get_secret_value.assert_called_once_with(
            SecretId='secret')

    def test_return_string_when_json_parsing_fails(self, client):
        client.return_value = self.mock_client('{')
        assert load_config('!aws/sm secret') == '{'

    def test_return_None_when_key_does_not_exist(self, client):
        client.return_value = mock.Mock()
        client.return_value.get_secret_value.side_effect = \
            ClientError({}, operation_name='GetSecretValue')
        assert load_config('!aws/sm secret') is None

    def test_return_string_as_string(self, client):
        client.return_value = self.mock_client('bogus')
        assert load_config('!aws/sm secret') == 'bogus'
