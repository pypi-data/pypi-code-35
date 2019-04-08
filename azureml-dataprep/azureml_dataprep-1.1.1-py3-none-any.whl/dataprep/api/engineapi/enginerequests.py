import json
import socketserver
import threading
from uuid import uuid4
from azureml.dataprep.api.engineapi.api import EngineAPI, get_engine_api


class EngineRequestsChannel:
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            with self.request.makefile() as reader:
                with self.request.makefile('w') as writer:
                    request = json.loads(reader.readline())
                    request_secret = request.get('host_secret')
                    if request_secret is None or request_secret != self.server.host_secret:
                        writer.write(json.dumps({'result': 'error', 'error': 'Unauthorized'}))
                    else:
                        operation = request['operation']
                        callback = self.server.handlers.get(operation)
                        if callback is None:
                            writer.write(json.dumps({'result': 'error', 'error': 'InvalidOperation'}))
                        else:
                            callback(request, writer)

    def __init__(self, engine_api: EngineAPI):
        self._handlers = {}
        self._server = socketserver.TCPServer(("localhost", 0), EngineRequestsChannel.Handler)
        self._server.handlers = self._handlers
        self._server.host_secret = str(uuid4())
        self._server_thread = threading.Thread(target=self._server.serve_forever)
        self._server_thread.daemon = True
        self._server_thread.start()
        engine_api.set_host_secret(self._server.host_secret)
        engine_api.set_host_channel_port(self._server.server_address[1])

    def register_handler(self, message: str, callback):
        self._handlers[message] = callback


_requests_channel = None


def get_requests_channel() -> EngineRequestsChannel:
    global _requests_channel
    if not _requests_channel:
        _requests_channel = EngineRequestsChannel(get_engine_api())

    return _requests_channel
