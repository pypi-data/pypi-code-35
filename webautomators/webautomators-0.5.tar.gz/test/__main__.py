import unittest
import HtmlTestRunner
from instances_test import TestInstancesChrome


unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='htmlcov'))
