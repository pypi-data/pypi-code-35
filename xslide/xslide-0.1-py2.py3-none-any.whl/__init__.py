#!/usr/bin/env python3
import codecs
import contextlib
import inspect
import os
import shutil

import grot
import markdown
import xplant
from markdown.extensions.fenced_code import FencedCodeExtension

SERVE_CODE = """\
#!/usr/bin/env python3
import sys

import http.server
import socketserver

target = ("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8000)

with socketserver.TCPServer(target, http.server.SimpleHTTPRequestHandler) as httpd:
    print("serving at http://{}:{}/index.html".format(*target))
    httpd.serve_forever()

"""


class Color:
    # NOKIA brand colors
    lo = "#124191"
    med = "#2e99e6"
    hi = "#00c9ff"
    dark_gray = "#68717a"
    med_gray = "#a8bbc0"
    light_gray = "#d8d9da"
    black = "#000000"
    white = "#ffffff"
    lo2 = "#0b285b"


JS_KEY_SHORTCUTS = """
document.onkeydown = function (e) {{
    e = e || window.event;
{left}{right}}}
"""


def _get_py_source_path():
    call_stack = inspect.stack()
    for frame_info in reversed(call_stack):
        if os.path.realpath(frame_info.filename) != os.path.realpath(__file__) and frame_info.filename != "<stdin>":
            return frame_info.filename
    raise ValueError("Something went wrong. Cannot extract source file.")


def eval_out_path(py_source_path):
    source_dir, file_name = os.path.split(os.path.abspath(py_source_path))
    base_name, _ = os.path.splitext(file_name)
    common_directory = os.path.join(source_dir, XSlide.common_output_directory_name)
    out_dir = os.path.join(common_directory, base_name)
    return common_directory, out_dir, base_name


class XSlide(object):
    common_output_directory_name = "output"
    css_name = 'xslide.css'
    footer_credits = "© All rights reserved 2019"

    def __init__(self, title=None):

        common_directory, self._output_directory, self._base_name = eval_out_path(_get_py_source_path())
        self.prepare_output_directory(common_directory)

        self.title = title or self._base_name
        self.current_doc_path = self.out_path("index.html")
        self.index_page = self.out_path("index.html")
        self.page_number = 1
        self.previous_doc_path = None

        self.x = xplant.html5_plant()

        self._css_file = self._distribute_css()
        self.distribute_serve()
        self._last_header = None

    def prepare_output_directory(self, common_directory):
        if not os.path.isdir(common_directory):
            print(" creating empty common directory {}".format(common_directory))
            os.makedirs(common_directory)

        if os.path.exists(self._output_directory):
            print(" removing {}".format(self._output_directory))
            shutil.rmtree(self._output_directory)
        os.makedirs(self._output_directory, exist_ok=True)

    def out_path(self, *path_parts):
        return os.path.join(self._output_directory, *path_parts)

    def _rel_url(self, *other):
        if not other or other == (None,):
            return None
        return os.path.relpath(os.path.join(*other), self._output_directory)

    def _distribute_css(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        src_css = os.path.join(this_dir, self.css_name)
        if not os.path.exists(src_css):
            raise ValueError("Expected to find {} file in {}, but it does not exist.".format(self.css_name, this_dir))

        shutil.copy(src_css, self.out_path())
        return self.out_path(self.css_name)

    def distribute_serve(self):
        serve_script = self.out_path("serve.py")
        with open(serve_script, "wt") as f:
            f.write(SERVE_CODE)
            try:
                mode = os.fstat(f.fileno()).st_mode
                mode |= 0o111
                os.fchmod(f.fileno(), mode & 0o7777)
            except OSError:
                pass

    def flush(self):
        """ Store current state, but keep the contents for the next slide. """
        next_file = self._eval_next_file_path()
        self.store(next_file)
        self.previous_doc_path = self.current_doc_path
        self.page_number += 1
        self.current_doc_path = next_file

    def next(self, next_header=""):
        """ Store current state and clean contents. """
        self.flush()
        self.x = xplant.html5_plant()
        if next_header or self._last_header:
            self.make_basic_header(next_header or self._last_header)
        self._last_header = next_header

    def make_basic_header(self, header_content):
        with self.x.div(klass="paper_header"):
            self.x.text(header_content)

    def store(self, next_file=None):
        """ Encapsulate contents with html document structure and save it under self.current_doc_path.
        next_file can be a path to a document that will be loaded after pressing right key or "next" button.
        """
        doc = xplant.html5_plant()
        with self._make_html_doc(doc, next_file):
            doc.replant(self.x)
        with codecs.open(self.current_doc_path, 'w', encoding='utf-8') as out_f:
            return out_f.write(str(doc))

    @contextlib.contextmanager
    def make_graph(self, graph_name, *args, html_style="min-width: 100%;", **kwargs):
        base_name = os.path.basename(self.current_doc_path)
        graph = DefaultGraph(
            name="{}_{}".format(base_name, graph_name),
            filename="{}_{}.dot".format(base_name, graph_name),
            directory=self._output_directory,
            format='svg',
            *args,
            **kwargs,
        )
        yield graph

        img = graph.render()
        self.x.img(src=os.path.relpath(img, self._output_directory), alt='graph {}'.format(graph_name),
                   klass='graph', style=html_style)

    def markdown(self, *md_text):
        for not_last, md in enumerate(md_text, 1 - len(md_text)):
            html = markdown.markdown(md, extensions=[FencedCodeExtension()])
            self.x.text(html)
            if len(md_text) > 1 and not_last:
                self.flush()

    def _eval_next_file_path(self):
        return self.out_path("{}_{:02}.html".format(self._base_name, self.page_number))

    @contextlib.contextmanager
    def _make_html_doc(self, x, next_file):
        home_url = self._rel_url(self.index_page)
        prev_url = self._rel_url(self.previous_doc_path)
        next_url = self._rel_url(next_file)
        title = "x{:02} {}".format(self.page_number, self.title)
        with x.html():
            with x.head():
                x.meta(charset="utf-8")
                x.meta(http_equiv="Content-Security-Policy")
                x.meta(("name", "viewport"), content="width=device-width, initial-scale=1.0, "
                                                     "maximum-scale=1.0, user-scalable=no")
                x.line("title", title)
                x.link(rel="stylesheet", href=self._rel_url(self._css_file))
                if prev_url or next_url:
                    event = "if (e.keyCode == '{key}') {{window.location.href = '{loc}';}}\n"
                    l_ = event.format(key='37', loc=prev_url) if prev_url else ""
                    r_ = event.format(key='39', loc=next_url) if next_url else ""
                    js = JS_KEY_SHORTCUTS.format(left=l_, right=r_)
                    with x.script(type="text/javascript"):
                        x.text(js)

            with x.body(), x.main():
                with x.div(klass="paper"):
                    yield x
                with x.nav(), x.table(width="100%", style="table-layout: fixed;"), x.tr():
                    with x.td():
                        if home_url and prev_url:
                            with x.a(href=home_url, target="_top"), x.button():
                                x.text("HOME")
                        if prev_url:
                            with x.a(href=prev_url, target="_top"), x.button():
                                x.text("< PREV")
                    with x.td(align="center", klass="footer_logo"):
                        with x.span(klass="xslide_logo"):
                            x.text("xslide")
                        x.text(self.footer_credits)
                    with x.td(align="right"):
                        if next_url:
                            with x.a(href=next_url, target="_top"), x.button():
                                x.text("NEXT >")


class DefaultGraph(grot.Grot):
    graph_attributes = {
        'rankdir': 'LR',
        'color': Color.lo,
        'nodesep': '0.35',
        'ranksep': None,
    }
    node_attributes = {
        'color': Color.lo,
        'penwidth': '2.1',
    }
    edge_attributes = {
        'color': Color.lo,
        'penwidth': '2.1',
    }
