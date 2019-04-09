from pathlib import Path
from pystache.renderer import Renderer
import pyquilted


DATA_PATH = str(Path(pyquilted.__file__).resolve().parent)


class TemplateRender:
    """A wrapper class that wraps rendering of mustache templates"""
    @staticmethod
    def render_mustache(template, data):
        pystache = Renderer(search_dirs=DATA_PATH + '/templates')
        html = pystache.render_path(template, data)
        return html
