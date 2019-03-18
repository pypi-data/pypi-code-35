import os
import logging
import pycodestyle

from test import TestCaseBase


class TestCodeStyle(TestCaseBase):

    def test_conformance(self):
        logging.info("Codestyle should be consistent (per module, since this is a multi-cultural project)")
        style = pycodestyle.StyleGuide(quiet=False, config_file=os.path.join(self.basedir, '../tox.ini'))
        python_files = []
        excluded_dirs = ['.eggs', 'build', '.sonic', 'venv']
        for root, dirs, files in os.walk(os.path.join(self.basedir, '..')):
            python_files += [os.path.join(root, f) for f in files if
                             f.endswith('.py') and all(dir not in root for dir in excluded_dirs)]
        result = style.check_files(python_files)
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings)")
