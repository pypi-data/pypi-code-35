from pathlib import Path
import pyquilted
from pyquilted.builder.resume import ResumeBuilder
from pyquilted.template_render import TemplateRender
from pyquilted.yaml_loader import YamlLoader


DATA_PATH = str(Path(pyquilted.__file__).resolve().parent)


class ResumeToHtml:
    """A mixin that mixes the converting from data to resume to html"""
    def resume_to_html(self):
        self._yaml_load()
        self._resume_build()
        self._html_render()

    def _yaml_load(self):
        with open(self.resume_file) as f:
            self.resume_odict = YamlLoader.ordered_load(f)

    def _resume_build(self):
        builder = ResumeBuilder(self.resume_odict, style_options=self.style_options,
                                section_options=self.section_options)
        self.resume = builder.section_map()

    def _html_render(self):
        self.html = TemplateRender.render_mustache(
                DATA_PATH + '/templates/base.mustache', self.resume)
