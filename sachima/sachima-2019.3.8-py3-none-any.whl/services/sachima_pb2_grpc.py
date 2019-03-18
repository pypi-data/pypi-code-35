# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import sachima_pb2 as sachima__pb2


class ReporterStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.RunReport = channel.unary_unary(
            "/sachima.Reporter/RunReport",
            request_serializer=sachima__pb2.ReportRequest.SerializeToString,
            response_deserializer=sachima__pb2.ReportReply.FromString,
        )


class ReporterServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def RunReport(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ReporterServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "RunReport": grpc.unary_unary_rpc_method_handler(
            servicer.RunReport,
            request_deserializer=sachima__pb2.ReportRequest.FromString,
            response_serializer=sachima__pb2.ReportReply.SerializeToString,
        )
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "sachima.Reporter", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
