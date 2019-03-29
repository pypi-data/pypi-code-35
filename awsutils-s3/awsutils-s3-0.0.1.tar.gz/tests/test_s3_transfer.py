import unittest
import os
from looptools import Timer
from dirutility import DirPaths
from awsutils.s3 import S3
from tests import S3_BUCKET, LOCAL_BASE, printer


class TestS3Transfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s3 = S3(S3_BUCKET)

    @Timer.decorator
    def test_s3_upload(self):
        target = 'test_s3_transfer.py'
        self.s3.upload(os.path.join(LOCAL_BASE, 'tests', target))
        self.assertTrue(target in self.s3.list())

        self.s3.delete(target)
        self.assertFalse(target in self.s3.list())

    @Timer.decorator
    def test_s3_download(self):
        target = 'helpers.py'
        self.s3.download('awsutils/s3/helpers.py')
        self.assertTrue(os.path.isfile(target))

        os.remove(target)
        self.assertFalse(os.path.isfile(target))

    @Timer.decorator
    def test_s3_sync(self):
        target = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'awsutils')
        self.s3.sync(target)

        s3_files = self.s3.list(recursive=True)
        local_files = [os.path.join('awsutils', path) for path in DirPaths(os.path.join(LOCAL_BASE, 'awsutils')).walk()]
        # printer('Remote S3 Files', s3_files)
        # printer('Local Files', local_files)
        self.assertEqual(set(s3_files), set(local_files))


if __name__ == '__main__':
    unittest.main()
