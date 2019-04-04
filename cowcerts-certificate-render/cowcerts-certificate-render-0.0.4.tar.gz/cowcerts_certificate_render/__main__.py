"""Cowcerts certificate render entry point."""
import pkgutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys

from jinja2 import Template
from bs4 import BeautifulSoup
import htmlmin
from inlinestyler.utils import inline_css

CURRENT_MODULE = "cowcerts_certificate_render"

DATA_DIR = "data"

TEMPLATES_DIR = os.path.join(
    DATA_DIR,
    "templates"
)

CERTIFICATES_DIR = os.path.join(
    DATA_DIR,
    "certificates"
)

DEFAULT_TEMPLATE_FILE = os.path.join(
    TEMPLATES_DIR,
    "cowcerts-for-education.html"
)

DEFAULT_CERTIFICATE_FILE = os.path.join(
    CERTIFICATES_DIR,
    "cowcerts-edu-20190403.json"
)

SERVER_HOST = ""

SERVER_PORT = 8081


class BasicHTTPRequestHandler(BaseHTTPRequestHandler):

    def _simple_response(self):
        pass

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._simple_response())


def main():
    html = read_html_template()
    certificate = read_certificate()
    render = render_html(html, certificate)
    if len(sys.argv) > 1 and sys.argv[1] in ("-s", "--serve"):
        render_beautified = BeautifulSoup(
            render,
            features="html.parser"
        ).prettify()
        request_handler = type(
            "GeneratedHTTPRequestHandler",
            (BasicHTTPRequestHandler,),
            {
                "_simple_response": lambda s: render_beautified.encode('utf-8')
            }
        )
        print("Serving certificate at \"%s\":%d" % (SERVER_HOST, SERVER_PORT))
        HTTPServer((SERVER_HOST, SERVER_PORT), request_handler).serve_forever()
    else:
        render_inlined = inline_css(render)
        render_body = ''.join(
            '%s' % l for l in BeautifulSoup(
                render_inlined,
                features="lxml"
            ).body.contents)
        render_minified = htmlmin.minify(
            render_body, remove_empty_space=True)
        certificate["displayHtml"] = render_minified
        print(json.dumps(certificate))


def read_html_template(template_file = DEFAULT_TEMPLATE_FILE):
    return load_file(template_file)


def load_file(filename):
    return pkgutil.get_data(CURRENT_MODULE, filename).decode("utf-8")


def read_certificate(certificate_file = DEFAULT_CERTIFICATE_FILE):
    return json.loads(load_file(certificate_file))


def render_html(html, context):
    return Template(html).render(context)


if __name__ == "__main__":
    main()
