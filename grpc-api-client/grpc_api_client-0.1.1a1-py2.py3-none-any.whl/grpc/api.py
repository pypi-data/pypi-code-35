import json
from importlib import import_module
from google.protobuf.json_format import MessageToJson

class gRPC_API_Response(object):
    """
    Class object for handling responses from Dex gRPC server.
    """
    def __init__(self, response, output_handler, fields):
        self.json        = json.loads(MessageToJson(response))
        self.protobuf    = output_handler(**self._get_field_values(response, fields))

    def _get_field_values(self, response, fields):
        """
        Return an object of field/key values from a request object post-request.
        """
        response_fields = {}
        for field in fields:
            if hasattr(response, field[0]):
                response_fields[field[0]] = getattr(response, field[0])
        return response_fields

class gRPC_API_Method_IO_Map(object):
    """
    Map the i/o type (from the descriptor) and the *pb2.py file
    """
    def __init__(self, io_type, io_handler):
        self.type = io_type
        self.handler = io_handler

class gRPC_API_Path(object):
    """
    Class object for storing API path attributes and objects.
    """
    def __init__(self, method, settings):
        """
        Initialize and store the stub object for later use.
        """
        self.name = method['name']

        # Client settings
        self._settings = settings

        # Input and output objects
        self.input = gRPC_API_Method_IO_Map(method['input_type'], method['input_handler'])
        self.output = gRPC_API_Method_IO_Map(method['output_type'], method['output_handler'])

        # Stub instance
        self.stub = self._settings.bindings.stub_object

    def input_fields(self):
        """
        Return an iterator for available input fields.
        """
        return self.input.type.fields_by_name.items()

    def __call__(self, **kwargs):
        """
        Call the underlying stub method for this API path.
        """
        response = getattr(self.stub, self.name)(self.input.handler(**kwargs))
        return gRPC_API_Response(response, self.output.handler, self.input_fields())

class gRPC_API_Collection(object):
    """
    Class object for storing API path objects.
    """
    def __init__(self, settings):
        """
        :param settings: The generated settings object
        :type settings: gRPC_API_Client_Settings
        """
        self._settings = settings
        self._methods  = []

    def __iter__(self):
        """
        Return a dictionary of gRPC methods.
        """
        for method_name in self._methods:
            yield(method_name, getattr(self, method_name))

    def add(self, method):
        """
        Add a new gRPC method.

        :param service: The generated gRPC service method object
        :type name: str
        """
        self._methods.append(method['name'])

        # Store the API method
        setattr(self, method['name'], gRPC_API_Path(method, self._settings))
