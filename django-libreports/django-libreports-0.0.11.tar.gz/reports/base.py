import tempfile

from pypandoc import convert_text
from django.core.files.base import ContentFile
from hardcopy import bytestring_to_pdf


class BaseReport(object):
    id = ''
    name = ''

    def get_report_name(self, **kwargs):
        return ' '.join([kwargs['organization'].name, self.id.capitalize(),
                         'Report'])

    def get_report_filename(self, **kwargs):
        return '{0} {1} to {2}.{3}'.format(self.get_report_name(**kwargs),
                                           kwargs['start_datetime'].date(),
                                           kwargs['end_datetime'].date(),
                                           kwargs['typ'])

    def markdown_to_doc(self, markdown, typ, reference=None):
        """
        :param markdown: markdown document as a string
        :param typ: document conversion output extension
        :param reference: path to the reference docx, if different from default
        :return: path to a temporary file
        """

        with tempfile.NamedTemporaryFile(suffix='.{0}'.format(typ)) as temp:
            extra_args = ['--dpi=180']
            if typ == 'docx':
                if reference:
                    extra_args.append('--reference-docx={}'.format(reference))
                extra_args.append('--toc')
            convert_text(markdown, typ, 'markdown_phpextra',
                         outputfile=temp.name, extra_args=extra_args)
            with open(temp.name, 'r') as document:
                return ContentFile(document.read())

    def html_to_pdf(self, html, delay=5000):
        """
        :param html: html document as a bytestring
        :param delay: time to wait for javascript loading in ms
        :return: path to a temporary file
        """

        with tempfile.NamedTemporaryFile(suffix='.pdf') as temp:
            extra_args = {
                'virtual-time-budget': delay
            }

            bytestring_to_pdf(html, temp, **extra_args)
            with open(temp.name, 'r') as document:
                return ContentFile(document.read())
