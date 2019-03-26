from django.test import TestCase
import json
import os


class WebhookHandlerTestCase(TestCase):
    path = '/wh/gitlab/'

    def fixture(self, name):
        filename = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    __file__
                )
            ),
            'fixtures',
            'test_gitlab_%s.json' % name
        )

        with open(filename, 'rb') as f:
            return f.read()

    def post(self, fixture):
        response = self.client.generic(
            'POST',
            self.path,
            data=self.fixture(fixture)
        )

        return response, json.loads(response.content.decode('utf-8'))


class IssueOpenedTests(WebhookHandlerTestCase):
    def test_public(self):
        response, data = self.post('issue_opened')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.category', 1],
                    ['blog.tag', 1],
                    ['blog.tag', 2],
                    ['blog.tag', 3],
                    ['blog.post', 1]
                ],
                'updated': [],
                'deleted': []
            }
        )

    def test_confidential(self):
        response, data = self.post('issue_confidential_opened')
        self.assertEqual(
            data,
            {
                'created': [],
                'updated': [],
                'deleted': []
            }
        )


class IssueClosedTests(WebhookHandlerTestCase):
    fixtures = ('test_issue_open',)

    def test_post_issue_closed(self):
        response, data = self.post('issue_closed')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.post', 2]
                ],
                'updated': [
                    ['blog.tag', 1],
                    ['blog.tag', 2],
                    ['blog.tag', 3],
                    ['blog.post', 1]
                ],
                'deleted': []
            }
        )


class IssueCommentedTests(WebhookHandlerTestCase):
    fixtures = ('test_issue_open',)

    def test_post_comment(self):
        response, data = self.post('issue_comment')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.post', 2]
                ],
                'updated': [],
                'deleted': []
            }
        )


class IssueRelabeledTests(WebhookHandlerTestCase):
    fixtures = ('test_issue_open',)

    def test_post_todo(self):
        response, data = self.post('issue_todo')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.tag', 4]
                ],
                'updated': [
                    ['blog.tag', 1],
                    ['blog.tag', 2],
                    ['blog.tag', 3],
                    ['blog.post', 1]
                ],
                'deleted': []
            }
        )

    def test_post_doing(self):
        response, data = self.post('issue_doing')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.tag', 4]
                ],
                'updated': [
                    ['blog.tag', 1],
                    ['blog.tag', 2],
                    ['blog.tag', 3],
                    ['blog.post', 1]
                ],
                'deleted': []
            }
        )


class IssueReopenedTests(WebhookHandlerTestCase):
    fixtures = ('test_issue_closed',)

    def test_post_reopen(self):
        response, data = self.post('issue_reopened')
        self.assertEqual(
            data,
            {
                'created': [
                    ['blog.tag', 4],
                    ['blog.post', 3],
                ],
                'updated': [
                    ['blog.tag', 1],
                    ['blog.tag', 2],
                    ['blog.tag', 3],
                    ['blog.post', 1]
                ],
                'deleted': []
            }
        )

        # from django.core.management import call_command
        # call_command('dumpdata', 'blog', indent=2)
