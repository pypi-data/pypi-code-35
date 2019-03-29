import unittest
import six

import yatom.processor

from . import meta


class TestHTMLSyntax(six.with_metaclass(meta.TestFileMeta, unittest.TestCase)):
    processor_class = yatom.processor.HTMLProcessor
    meta_module = 'yatom'
    meta_prefix = 'yaml'
    meta_file_extensions = ('.html',)

    def meta_test(self, module, filename):
        name = filename[:-5]
        input = self.read_text(module, '%s.yml' % name)
        output = self.read_text(module, filename).strip()
        parser = self.processor_class.from_source(input)
        parsed = parser.render()
        self.assertEqual(parsed, output)
