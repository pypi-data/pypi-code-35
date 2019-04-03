from importlib import import_module
from inspect import getmembers, isclass

_GRPC_STUB_SSTR='Stub'
_GRPC_SERVICE_SSTR='Servicer'

class gRPC_API_Bindings(object):
    """
    Class object to store pb2 and pb2_grpc Python bindings.
    """
    def __init__(self, api_proto, api_grpc):
        self.proto     = import_module(api_proto)
        self.grpc      = import_module(api_grpc)

        # Stub and service name
        self.stub_name = None
        self.service_name = None
        self.stub_class = None

        # Get the stub and service name
        for a in getmembers(self.grpc):
            name = a[0]
            if isclass(a[1]):

                # Stub class
                if _GRPC_STUB_SSTR in name:
                    self.stub_name = name

                # Service name
                if _GRPC_SERVICE_SSTR in name:
                    self.service_name = name.replace(_GRPC_SERVICE_SSTR, '')

    def set_stub(self, stub):
        """
        Set the stub object from the interface.
        """
        self.stub_object = stub

    def get_stub(self):
        """
        Return the stub object.
        """
        return self.stub_object

    def get_service_methods(self):
        """
        Return an iterable object for looping through services.
        """
        service_name = self.service_name

        # Generate the service methods list
        service_methods = []
        for method in self.proto.DESCRIPTOR.services_by_name[service_name].methods_by_name.items():
            service_methods.append({
                'name': method[0],
                'stub': getattr(self.grpc, self.stub_name),
                'descriptor': method[1],
                'input_type': method[1].input_type,
                'input_handler': getattr(self.proto, method[1].input_type.name),
                'output_type': method[1].output_type,
                'output_handler': getattr(self.proto, method[1].output_type.name)
            })
        return service_methods
