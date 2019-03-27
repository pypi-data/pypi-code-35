from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from jinja2 import Environment, PackageLoader, select_autoescape

from snakeway import Stats

j2env = Environment(
    loader=PackageLoader('snakeway', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def get_handler(stats: Stats):
    class SnakeHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            j2env = Environment(
                loader=PackageLoader('snakeway', 'templates'),
                autoescape=select_autoescape(['html', 'xml'])
            )
            template = j2env.get_template('index.html')
            self.wfile.write(template.render(stats=stats.get_stats()).encode())
            self.server.path = self.path

    return SnakeHandler


class Server(Thread):
    def __init__(self, stats: Stats, server_address=('', 2208)):
        super().__init__()
        self.daemon = True
        self.stats = stats
        self.httpd = HTTPServer(server_address, get_handler(stats))

    def run(self):
        self.httpd.serve_forever()
