import factornado

class Handler(factornado.RequestHandler):
    def get(self):
        self.write('This is GET')

some_app = factornado.Application(
    {'name': 'test', 'threads_nb': 1, 'log': {'stdout': False}},
    [('/', Handler)],
    )

# some_app.request(method='GET', uri='/')


async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')