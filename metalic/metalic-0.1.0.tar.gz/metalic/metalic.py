import sanic
from sanic import response
import uuid
import os
import jinja2
from .connection import Connection


_html_cache = {}
_metalic_html = """<!DOCTYPE html>
<html lang="en">
    <body>
        <script>
            // Metalic renderer. Copyright (C) Jake Gealer 2019.
            var Metalic = {};
            (function() {
                // This is set to your UUID by Metalic.
                var uuid = "UUID_HERE";

                // Initialises the WebSocket.
                var ws = new WebSocket((location.protocol === "http:" ? "ws://" : "wss://") + window.location.href.substr(location.protocol === "http:" ? 7 : 8, window.location.href.length - window.location.pathname.length) + "_metalic/" + uuid);

                // Sends the draw request to the WebSocket.
                ws.onopen = function () {
                    ws.send('{"type": "draw"}');
                };

               // Handles the WebSocket connection closing.
               ws.onclose = function() {
                   if (window.ondisconnect) {
                       window.ondisconnect();
                   }
               };

                // Handles WebSocket messages.
                ws.onmessage = function (msg) {
                    var jsonified = JSON.parse(msg.data);
                    switch (jsonified.type) {
                        case "redraw": {
                            document.open();
                            document.write(jsonified.html);
                            var newMetalic = {};
                            Object.entries(jsonified.data).forEach(function(entry) {
                                if (entry[1].f) {
                                    eval(`
                                        newMetalic[entry[0]] = function (${entry[1].a.join(",")}) {
                                            ws.send(JSON.stringify({
                                                "type": "call",
                                                "func": entry[0],
                                                "args": Array.from(arguments)
                                            }));
                                        }
                                    `);
                                } else {
                                    newMetalic[entry[0]] = entry[1].d;
                                }
                            });
                            Metalic = newMetalic;
                            document.close();
                            break;
                        }
                    }
                }
            })();
        </script>
    </body>
</html>
"""


class Metalic:
    """
    The main core of the reactivity library.
    """
    def __init__(self, app: sanic.Sanic, data: dict = None, **kwargs):
        """
        The initialisation for the Metalic library.
        :param app: The main Sanic application.
        :param data: A shortcut for kwargs if set. Will override anything set in kwargs if set.
        :param kwargs: This is all of the data which has been defined by the end user.
        """
        self.app = app
        if data:
            self.data = data
        else:
            self.data = kwargs
        self._call_on_reactions = []
        self._connections = {}

    @staticmethod
    def clear_html_cache():
        """This is used to clear the HTML cache."""
        _html_cache.clear()

    async def render(self, fp: str):
        """
        Used to render the basic JS front ends needed to support this library.
        :param fp: The file path to the HTML.
        """
        generated_uuid = str(uuid.uuid4())

        try:
            html = _html_cache[fp]
        except KeyError:
            html = await self.app.loop.run_in_executor(None, open(fp, "r").read)
            _html_cache[fp] = html

        j_template = jinja2.Template(html)

        self._connections[generated_uuid] = Connection(generated_uuid, self, j_template)
        return response.html(_metalic_html.replace("UUID_HERE", generated_uuid, 1))

    def update(self):
        """Called when individual objects in the dictionary are updated."""
        self._react(None)

    def on_react(self, func):
        """Allows you to add a function to be called when a reaction happens."""
        self._call_on_reactions.append(func)

    def _react(self, key):
        """Called when a reaction happens."""
        for reaction in self._call_on_reactions:
            self.app.add_task(reaction(self, key))

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def get(self, item, if_not=None):
        return self.data.get(item, if_not)

    def __setitem__(self, key, value):
        """Used to set a reactive item."""
        self.data[key] = value
        self._react(key)
