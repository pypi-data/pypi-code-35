import ujson
import jinja2
from functools import partial
from asyncio import iscoroutinefunction


class Connection:
    """Defines a connection to a Metalic session."""
    def __init__(self, uuid: str, instance, template: jinja2.Template):
        self.instance = instance
        self.uuid = uuid
        self.template = template
        self.active = True
        self._ws = None

        self.instance.app.add_websocket_route(self._handle_ws, "/_metalic/%s" % self.uuid)
        self.instance.on_react(self._handle_reaction)

    async def _handle_reaction(self, *_):
        """Handles a reaction in the main application instance."""
        if not self._ws:
            return

        await self._issue_redraw(self._ws)

    def kill(self):
        """This is used to kill the connection."""
        del self.instance._connections[self.uuid]
        self.active = False
        self.instance.app.remove_route("/_metalic/%s" % self.uuid)
        self.instance._call_on_reactions.remove(self._handle_reaction)

    async def _issue_redraw(self, ws):
        """Used to issue a redraw to the WebSocket."""
        rendered = await self.instance.app.loop.run_in_executor(
            None, partial(self.template.render, **self.instance.data)
        )
        await ws.send(ujson.dumps({
            "type": "redraw",
            "html": rendered,
            "data": self._jsify_data()
        }))

    def _jsify_data(self):
        """Puts the data in a form which the JavaScript on the client-side can understand."""
        _jsified = {}
        for key in self.instance.data:
            x = {
                "f": callable(self.instance.data[key])
            }
            if x['f']:
                x['a'] = self.instance.data[key].__code__.co_varnames[1:]
            else:
                x['d'] = self.instance.data[key]
            _jsified[key] = x

        return _jsified

    async def _process_data(self, ws, data):
        """Used to process the given data."""
        try:
            data = ujson.loads(data)
        except:
            # This is probably invalid JSON.
            return

        if type(data) is not dict:
            # Nope.
            return

        try:
            req_type = data['type']
        except KeyError:
            # Invalid request.
            return

        if req_type == "draw":
            await self._issue_redraw(ws)
        elif req_type == "call":
            if not data.get("func"):
                return

            try:
                alleged_func = self.instance.data[data['func']]
            except KeyError:
                return

            if not callable(alleged_func):
                return

            args = []
            if data.get("args") and type(data['args']) is list:
                args = data['args']

            async def run_func():
                """We should run this in a separate task in case shit hits the fan."""
                if iscoroutinefunction(alleged_func):
                    await alleged_func(self.instance, *args)
                else:
                    alleged_func(self.instance, *args)

            self.instance.app.add_task(run_func())

    async def _handle_ws(self, _, ws):
        """Handles WebSocket requests."""
        self._ws = ws
        try:
            while self.active:
                data = await ws.recv()
                await self._process_data(ws, data)
        finally:
            self.kill()
