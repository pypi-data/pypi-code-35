# -*- coding: utf-8 -*-
"""sample_test: thegmu_pypi_template single sample test."""

import unittest


from thegmu_pypi_template.sample import Sample


class SampleTest(unittest.TestCase):
    """SampleTest: run the provided sample.py file single method to test."""

    def test01_sample(self):
        """The GMU PyPi Template Sample test ONLY."""

        sample_test = Sample()
        test_name = "Test"
        expected_result = "Hello %s" % (test_name, )
        self.assertEqual(sample_test.hello(test_name), expected_result)
        print("sample_test...passed")
