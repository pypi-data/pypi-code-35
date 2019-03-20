# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
import uuid

import soniclib
from mock import patch
from soniclib import config

from soniclib.context import Context
from test import TestCaseBase


class TestContext(TestCaseBase):

    def setUp(self):
        super(TestContext, self).setUp()
        self.test_dir = tempfile.mkdtemp()
        soniclib.context._mock_load_in_unittest = False

    def tearDown(self):
        super(TestContext, self).tearDown()
        shutil.rmtree(self.test_dir)
        soniclib.context._mock_load_in_unittest = True

    @patch('soniclib.context.Context.load')
    def test_singleton_state(self, load_mock):
        context1 = Context()
        context2 = Context()
        context1.pipe_id = str(uuid.uuid4())
        self.assertEqual(context1.pipe_id, context2.pipe_id)

        context2.task_id = str(uuid.uuid4())
        self.assertEqual(context1.task_id, context2.task_id)

    def test_unicode(self):
        config.SONIC_PATH = os.path.join(self.basedir, "yaml")
        soniclib.context.CONTEXT_FILE_NAME = "context_with_tags.yml"
        context = Context(force_load=True)
        self.assertEqual(context["basic"], "value")
        self.assertEqual(context["with_tag"], None)
        self.assertEqual(context["unicode_value"], u"value")

    def test_refresh(self):
        config.SONIC_PATH = self.test_dir

        with open(os.path.join(self.test_dir, 'context.yml'), 'w') as context_file:
            context_file.write('status: 0')

        context = Context(force_load=True)
        self.assertEqual(context["status"], 0)

        with open(os.path.join(self.test_dir, 'context.yml'), 'w') as context_file:
            context_file.write('status: 1')

        context.refresh()
        context.status = 2
        context.save()
        self.assertEqual(context["status"], 2)


if __name__ == "__main__":
    unittest.main()
