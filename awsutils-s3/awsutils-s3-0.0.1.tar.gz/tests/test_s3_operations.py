import unittest
import os
from looptools import Timer
from awsutils.s3 import S3
from tests import S3_BUCKET, printer


class TestS3Operations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

        cls.target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')
        cls.s3.sync(cls.target)

    @classmethod
    def tearDownClass(cls):
        cls.s3.delete(cls.target)

    @Timer.decorator
    def test_s3_copy(self):
        target = 'helpers.py'
        self.s3.copy('awsutils/s3/helpers.py', target)
        self.assertTrue(target in self.s3.list())
        self.s3.delete(target)

    @Timer.decorator
    def test_s3_move(self):
        target = 'helpers2.py'
        self.s3.copy('awsutils/s3/helpers.py', 'awsutils/s3/helpers2.py')
        self.assertTrue(target in self.s3.list('awsutils/s3'))

        self.s3.move('awsutils/s3/helpers2.py', target)
        self.s3.delete(target)
        self.assertFalse(target in self.s3.list())

    @Timer.decorator
    def test_s3_delete(self):
        target = 'helpers.py'
        self.s3.copy('awsutils/s3/helpers.py', target)

        self.s3.delete(target)
        self.assertFalse(target in self.s3.list())


if __name__ == '__main__':
    unittest.main()
