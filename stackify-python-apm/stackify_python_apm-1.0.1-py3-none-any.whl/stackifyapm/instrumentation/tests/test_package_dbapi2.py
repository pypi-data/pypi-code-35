from unittest import TestCase

from stackifyapm.instrumentation.packages.dbapi2 import Literal, extract_signature, scan, tokenize


class DBAPI2InstrumentationTest(TestCase):

    def test_scan_simple(self):
        sql = "Stackify Python APM"
        expected = ['Stackify', 'Python', 'APM']

        tokens = tokenize(sql)
        actual = [t[1] for t in scan(tokens)]

        assert actual == expected

    def test_scan_complex(self):
        sql = "Stackify 'Python' APM"
        expected = ['Stackify', Literal("'", "Python"), 'APM']

        tokens = tokenize(sql)
        actual = [t[1] for t in scan(tokens)]

        assert actual == expected

    def test_extract_signature_string(self):
        sql = "Stackify Python APM"
        expected = "STACKIFY"

        actual = extract_signature(sql)

        assert actual == expected
