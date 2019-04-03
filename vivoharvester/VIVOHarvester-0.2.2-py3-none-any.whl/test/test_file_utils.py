import shutil
import tempfile
import os
import requests
import imghdr

from os import path
from unittest import TestCase
from vivotool.utils.file_utils import Utils


class TestFileUtils(TestCase):

    def setUp(self):
        self.utils = Utils()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        self.utils = None
        shutil.rmtree(self.test_dir)

    def test_save_photo_file(self):
        testfile = path.join(self.test_dir, 'test.png')
        content = requests.get(
            "https://www.iconfinder.com/icons/216359/download/png/128")

        self.utils.save_photo_file(content, testfile)
        output = imghdr.what(testfile)
        self.assertEqual(output, "png")

    def test_read_file(self):
        testfile = path.join(self.test_dir, 'test.txt')

        with open(testfile, "w") as f:
            f.write("some content")

        output = self.utils.read_file(testfile)
        self.assertEqual(output, "some content")

    def test_save_xml_file(self):
        testfile = path.join(self.test_dir, 'test.xml')
        content = "<xml>test</xml>"

        self.utils.save_xml_file(content, testfile)

        with open(testfile, 'r') as file:
            output = file.read()
        self.assertEqual(output, content)

    def test_listfiles(self):
        xmlfile = path.join(self.test_dir, 'test.xml')
        txtfile = path.join(self.test_dir, 'test.txt')

        with open(xmlfile, 'w') as f:
            f.write("some content")

        with open(txtfile, 'w') as f:
            f.write("some content")

        expected = ['test.xml']
        output = self.utils.listfiles(self.test_dir, ".xml")
        self.assertEqual(output, expected)

    def test_listdeletefiles(self):
        deletefile = path.join(self.test_dir, 'deletetest2.xml')
        deletefile1 = path.join(self.test_dir, 'deletetest1.xml')
        txtfile = path.join(self.test_dir, 'test.txt')

        with open(deletefile, 'w') as f:
            f.write("some content")

        with open(deletefile1, 'w') as f:
            f.write("some content")

        with open(txtfile, 'w') as f:
            f.write("some content")

        expected = ['deletetest1.xml', 'deletetest2.xml']
        output = self.utils.listdeletefiles(self.test_dir, "delete")
        self.assertEqual(output, expected)

    def test_segmentlist(self):

        inputlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        output = self.utils.segmentlist(inputlist, 3)
        expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

        self.assertEqual(output, expected)

        inputlist = [0]
        output = self.utils.segmentlist(inputlist, 3)
        expected = [[0]]

        self.assertEqual(output, expected)

    def test_mergefiles(self):

        inputlist = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt"]

        for x in range(1, 6):
            testfile = path.join(self.test_dir, str(x) + '.txt')
            with open(testfile, "w") as f:
                f.write("some content\n")

        testfilename = "mergefile.txt"
        mergefile = self.utils.mergefiles(
            self.test_dir, inputlist, testfilename)

        with open(path.join(self.test_dir, mergefile), "r") as file:
            output = file.read()

        self.assertEqual(
            output,
            "some content\nsome content\nsome content\nsome content\nsome content\n")

        inputlist = ["1.txt"]
        testfile = path.join(self.test_dir, '1.txt')
        with open(testfile, "w") as f:
            f.write("some content\n")

        testfilename = "mergefile.txt"
        mergefile = self.utils.mergefiles(
            self.test_dir, inputlist, testfilename)

        with open(path.join(self.test_dir, mergefile), "r") as file:
            output = file.read()

        self.assertEqual(
            output,
            "some content\n")
