from unittest import TestCase
import os

import docker


class PipeTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.image_tag = 'bitbucketpipelines/demo-pipe-python:ci' + \
            os.getenv('BITBUCKET_BUILD_NUMBER', 'local')
        cls.docker_client = docker.from_env()
        cls.docker_client.images.build(
            path='.', tag=cls.image_tag, nocache=True)

    @classmethod
    def tearDownClass(cls):
        cls.docker_client.images.remove(image=cls.image_tag)

    def run_container(self, cmd=None, **kwargs):
        return self.docker_client.containers.run(self.image_tag, command=cmd, **kwargs)


class PipeTestCaseTestCase(PipeTestCase):

    @classmethod
    def setUpClass(cls):
        with open('Dockerfile', 'w') as f:
            f.write("FROM python:3.7")
        super().setUpClass()

    def test_the_test(self):
        result = self.run_container('echo hello world')
        self.assertIn(b'hello world', result)
