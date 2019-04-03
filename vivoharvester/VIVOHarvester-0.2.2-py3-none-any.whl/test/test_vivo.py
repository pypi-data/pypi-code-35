import requests_mock

from unittest import TestCase

from vivotool.vivo.vivo import VIVO


class TestVIVO(TestCase):

    def setUp(self):
        self.vivo = VIVO()

    def tearDown(self):
        self.vivo = None

    @requests_mock.mock()
    def test_request_vivo(self, m):
        m.post('http://foo.com/', text='vivomock')
        output = self.vivo.request_vivo(
            'http://foo.com/', "", "", "", "")
        self.assertEqual(output, None)

        data = {
            'email': 'test@email.com',
        }

        output = self.vivo.request_vivo(
            "", "http://foo.com/", "", data, "update")
        self.assertEqual(output.status_code, 200)

    def test_get_query_content(self):

        output = self.vivo.get_query_content("", "otherop")
        self.assertEqual(output, "")

        output = self.vivo.get_query_content("test", "describe")
        expected = "DESCRIBE <test>"
        self.assertEqual(output, expected)

        output = self.vivo.get_query_content("test", "insert")
        expected = "INSERT DATA {\n" + \
            "GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {\n" + \
            "test}\n}\n"
        self.assertEqual(output, expected)

        output = self.vivo.get_query_content("test", "delete")
        expected = "DELETE DATA {\n" + \
            "GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {\n" + \
            "test}\n}\n"
        self.assertEqual(output, expected)
