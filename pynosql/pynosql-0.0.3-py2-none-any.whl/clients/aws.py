import boto3
from botocore.exceptions import ClientError
from pynosql.clients.base_client import BaseClient, \
    InitializationError, ClientException
from pynosql.credentials.aws import AWSCredentials, InvalidCredentials
from time import sleep


class AWSClient(BaseClient):
    """ AWS Session for DynamoDB """

    RETRY_EXCEPTIONS = (
        'ProvisionedThroughputExceededException',
        'ThrottlingException'
    )

    def __init__(self, credentials, region, retries=5,
                 endpoint=None, mock=None):
        """ AWS Session for DynamoDB

        :param credentials: obj credentials
        :param region: str region name
        :param retries: int client retries
        :param endpoint: str endpoint url
        :param mock: obj method to mock responses
        """
        self.credentials = credentials
        self.region = region
        self.retries = retries
        self.endpoint = endpoint
        self._client = self.initialize()
        if mock is not None:
            # if mock enabled the stub out
            # responses to dynamo for testing.
            mock(self._client)

    @property
    def client(self):
        """ DymamoDB Session

        :return: obj session
        """
        return self._client

    def initialize(self):
        """ Initialize DynamoDB Session

        :return: obj session
        :raises: InvalidCredentials
        """
        session = None
        if not isinstance(self.credentials, AWSCredentials):
            raise InvalidCredentials(
                'Credentials must be instance of AWSCredentials.'
            )
        try:
            session = boto3.Session(
                aws_access_key_id=self.credentials.access_key,
                aws_secret_access_key=self.credentials.secret_key,
                region_name=self.region
            )
        except Exception as e:
            raise InitializationError(
                'Error initializing AWS session: {}.'.format(str(e))
            )

        try:
            if self.endpoint:
                return session.resource(
                    'dynamodb',
                    region_name=self.region,
                    endpoint_url=self.endpoint
                )
            else:
                return session.resource('dynamodb', region_name=self.region)
        except Exception as e:
            raise InitializationError(
                'Error initializing AWS session: {}.'.format(str(e))
            )

    def call(self, client_method, **kwargs):
        """ Call client method

        :param client_method: str method
        :param kwargs: obj args
        :return: obj restuls
        :raises: ClientExecption
        """
        recoverable = True
        retry_count = 0

        while recoverable and retry_count < self.retries:

            try:
                return client_method(**kwargs)
            except ClientError as e:
                if e.response['Error']['Code'] not in self.RETRY_EXCEPTIONS:
                    raise ClientException(
                        '{}: {}.'.format(
                            e.response['Error']['Code'],
                            e.response['Error']['Message']
                        )
                    )
                pass
            except Exception as e:
                raise ClientException(
                    'Unhandled exception calling '
                    'client: {}.'.format(str(e.message))
                )

            sleep(2 ** retry_count)
            retry_count += 1
