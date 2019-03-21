import json
import unittest

from smklog import SmkLog


class TestSmkLog(unittest.TestCase):
    platform = "youzan"
    service = "nomad_envoy_order"
    maxDiff = None

    def test_smklog(self):
        logger = SmkLog(self.platform, self.service)

        source = "odoo"
        category = "info"
        label = "get_all_orders"

        message = "Translated error message for youzan service not responding"

        data = """{"key":"value","键":"值"}"""

        timing = """{"total":3}"""

        user = "1234567"

        store_id = "samarkand.youzan.foreveryoung"
        request_id = "0EFD81C9-16BF-4FF6-8CF8-00FEB0619A47"

        msg1 = logger.info(source, category, label, message, data, timing, user)
        msg1line1 = msg1.splitlines()[0]
        msg1line2 = msg1.splitlines()[1]

        self.assertTrue(isinstance(json.loads(msg1line2), dict),
                        "Second line of message should be JSON format")
        self.assertEqual(len(json.loads(msg1line2)), 9,
                         "all fields should be included.")
        self.assertEqual(json.loads(msg1line2)["smklog.data"], data,
                         "Chinese characters should keep original, not escaped")
        self.assertFalse("smklog.store_id" in json.loads(msg1line2),
                         "store_id is optional.")
        self.assertFalse("smklog.request_id" in json.loads(msg1line2),
                         "request_id is also optional")

        msg2 = logger.info(source, category, label, message, data, timing, user,
                           store_id, request_id)
        msg2line1 = msg2.splitlines()[0]
        msg2line2 = msg2.splitlines()[1]

        self.assertEqual(len(json.loads(msg2line2)), 11,
                         "all fields should be included, including store_id "
                         "and request_id.")

        self.assertTrue("smklog.store_id" in json.loads(msg2line2),
                        "we passed store_id field")
        self.assertTrue("smklog.request_id" in json.loads(msg2line2),
                        "we passed request_id field")

        data_json = json.dumps({"key": "value", "键": "值"},
                      ensure_ascii=False,
                      separators=(',', ':')
                      )
        msg3 = logger.info(source, category, label, message, data_json, user,
                           store_id, request_id)
        msg3line1 = msg3.splitlines()[0]
        msg3line2 = msg3.splitlines()[1]
        self.assertEqual(json.loads(msg3line2)["smklog.data"], '{"key":"value","键":"值"}',
                         "Chinese characters should keep original even when "
                         "data is JSON data format.")
