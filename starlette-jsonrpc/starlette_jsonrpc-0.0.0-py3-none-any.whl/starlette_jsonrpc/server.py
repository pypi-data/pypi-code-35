from starlette.responses import Response
from starlette.requests import Request


class RpcServer:

    def __init__(self, scope):
        assert scope['type'] == 'http'
        self.scope = scope

    async def __call__(self, receive, send):
        request = Request(self.scope, receive)
        body = b''
        async for chunk in request.stream():
            body += chunk
        response = Response(body, media_type='text/plain')
        await response(receive, send)

    def add_method(self):

        def decorator(func):
            return func
        return decorator