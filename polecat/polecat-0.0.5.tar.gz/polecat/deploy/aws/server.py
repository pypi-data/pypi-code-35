import ujson

from ...project import load_project
from .event import LambdaEvent


class Server:
    def __init__(self):
        self.project = load_project()
        self.project.prepare()

    async def handle(self, event, context):
        return self.encode_result(
            await self.project.handle_event(LambdaEvent(event))
        )

    def encode_result(self, result):
        return ujson({
            'statusCode': result[1],
            'data': result[0]
        })
