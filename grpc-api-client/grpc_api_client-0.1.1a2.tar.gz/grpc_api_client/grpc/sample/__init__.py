import string
from os import getenv
from numpy import random
from importlib import import_module
from random import getrandbits, choice, randint
from grpc_api_client.client import gRPC_API_Client_Settings, gRPC_API_Bindings

API_TEST_PARAMS = {
    'host': getenv('PY_GRPC_API_TEST_HOST', '127.0.0.1'),
    'port': getenv('PY_GRPC_API_TEST_PORT', 35557),
    'ca_cert': getenv('PY_GRPC_API_TEST_CA_CERT', 'docker_files/grpc_tls/ca.crt'),
    'client_cert': getenv('PY_GRPC_API_TEST_CLIENT_CERT', 'docker_files/grpc_tls/client.crt'),
    'client_key': getenv('PY_GRPC_API_TEST_CLIENT_KEY', 'docker_files/grpc_tls/client.key'),
    'server_cert': getenv('PY_GRPC_API_TEST_SERVER_CERT', 'docker_files/grpc_tls/server.crt'),
    'server_key': getenv('PY_GRPC_API_TEST_SERVER_KEY', 'docker_files/grpc_tls/server.key'),
    'api_proto': 'grpc_api_client.grpc.sample.api_pb2',
    'api_grpc': 'grpc_api_client.grpc.sample.api_pb2_grpc',
    'stub_name': 'APITestStub',
    'options': {}
}

class gRPC_API_Client_Test_Settings(object):
    """
    Generate a settings object for testing this module.
    """

    @staticmethod
    def secure():
        """
        Create test settings for a secure connection.
        """
        return gRPC_API_Client_Settings(API_TEST_PARAMS['host'], API_TEST_PARAMS['port'],
            ca_cert = API_TEST_PARAMS['ca_cert'],
            client_key = API_TEST_PARAMS['client_key'],
            client_cert = API_TEST_PARAMS['client_cert'],
            bindings = gRPC_API_Bindings(
                API_TEST_PARAMS['api_proto'],
                API_TEST_PARAMS['api_grpc']
            ))

    @staticmethod
    def insecure():
        """
        Create test settings for an insecure connection.
        """
        return gRPC_API_Client_Settings(API_TEST_PARAMS['host'], API_TEST_PARAMS['port'],
            bindings = gRPC_API_Bindings(
                API_TEST_PARAMS['api_proto'],
                API_TEST_PARAMS['api_grpc']
            ))

class gRPC_API_Test_Field(object):
    """
    Class object containing methods for representing a dummy test field.
    """
    def __init__(self, name, descriptor, repeated=False):
        """
        :param name: The field name
        :type name: str
        :param descriptor: The field descriptor object
        :type descriptor: object
        """
        self._repeated = repeated
        self._types = {
            'TYPE_BOOL': [8, self._random_bool],
            'TYPE_BYTES': [12, self._random_bytes],
            'TYPE_DOUBLE': [1, None],
            'TYPE_ENUM': [14, None],
            'TYPE_FIXED32': [7, None],
            'TYPE_FIXED64': [6, None],
            'TYPE_FLOAT': [2, self._random_float],
            'TYPE_GROUP': [10, None],
            'TYPE_INT32': [5, self._random_int32],
            'TYPE_INT64': [3, self._random_int64],
            'TYPE_MESSAGE': [11, None],
            'TYPE_SFIXED32': [15, None],
            'TYPE_SFIXED64': [16, None],
            'TYPE_SINT32': [17, None],
            'TYPE_SINT64': [18, None],
            'TYPE_STRING': [9, self._random_str],
            'TYPE_UINT32': [13, self._random_uint32],
            'TYPE_UINT64': [4, self._random_uint64]
        }

        # Field descriptor and name
        self.name = name
        self.descriptor = descriptor

        # Type integer and string label
        self._type_str = None
        self._type_int = None
        self._get_type()

    def _random_bool(self):
        """ Return a random boolean """
        return random.choice([True, False])

    def _random_bytes(self):
        """ Return a random bytes object """
        return random.bytes(128)

    def _random_float(self):
        """ Return a random floating point integer """
        return random.uniform(1, 2)

    def _random_int32(self):
        """ Return a random 32 bit integer """
        i = 2147483648
        return randint(-i, i)

    def _random_int64(self):
        """ Return a random 64 bit integer """
        i = 9223372036854775807
        return randint(-i, i)

    def _random_str(self):
        """ Return a random unicode string """
        letters = string.ascii_letters + string.digits
        return ''.join(choice(letters) for i in range(32))

    def _random_uint32(self):
        """ Generated a random unsigned 32 bit integer """
        return getrandbits(32)

    def _random_uint64(self):
        """ Generated a random unsigned 64 bit integer """
        return getrandbits(64)

    def _get_type(self):
        """
        Convenience method for getting the type of a field.
        """
        for type_str, type_attrs in self._types.items():
            if type_attrs[0] == self.descriptor.type:
                self._type_int = type_attrs[0]
                self._type_str = type_str

    def get_test_value(self):
        """
        Return a test value for the test field instance.
        """
        random_value_method = self._types[self._type_str][1]
        if random_value_method:

            # Repeated variable
            if self._repeated:
                return [random_value_method() for x in range(1,5)]
            else:
                return random_value_method()

        # Not implemented
        raise Exception('Generating test value for "{}" not implemented'.format(self_type_str))

class gRPC_API_Test_Fields(object):
    """
    Construct a collection of field arguments for a request object
    when running tests.
    """
    @classmethod
    def create(cls, method):
        """
        Create a new collection of test fields for the API method object.

        :param method: An instance of the API method handler
        :type api_object: gRPC_API_Path
        """
        input_fields = {}
        for name, descriptor in method.input_fields():
            repeated = True if descriptor.label == descriptor.LABEL_REPEATED else False
            field = gRPC_API_Test_Field(name, descriptor, repeated=repeated)

            # This field value is a another class
            if descriptor.message_type:
                continue
            else:
                input_fields[name] = field.get_test_value()
        return input_fields
