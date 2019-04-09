from pyquilted.resume_to_html import ResumeToHtml


class HtmlApp(ResumeToHtml):
    """App to load yaml and output resume in html"""
    def __init__(self, resume_file, path, style_options=None, section_options=None):
        self.style_options = style_options
        self.section_options = section_options
        self.resume_file = resume_file
        self.path = path

    def run(self):
        self.resume_to_html()
        self._print_html()

    def _print_html(self):
        with open(self.path, 'w') as f:
            f.write(self.html)
