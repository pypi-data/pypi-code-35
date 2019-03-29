import unittest
from looptools import Timer
from awsutils.s3 import S3
from tests import S3_BUCKET, printer


class TestS3PreSign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

    @Timer.decorator
    def test_s3_pre_sign(self):
        sign = self.s3.pre_sign('awsutils/s3/helpers.py', 10)
        self.assertTrue(len(sign) > 0)


if __name__ == '__main__':
    unittest.main()
