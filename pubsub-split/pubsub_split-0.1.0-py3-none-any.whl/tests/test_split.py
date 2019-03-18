import json
import unittest
from unittest.mock import MagicMock, patch

from pubsub_split import split


class TestSplit(unittest.TestCase):
    @patch("pubsub_split.split.pubsub")
    def test_send(self, pubsub):
        publisher = MagicMock()
        pubsub.PublisherClient.return_value = publisher
        items = [dict(name="item1")]
        split.send("path1", items, param="param1")
        expected_items = json.dumps(items).encode("utf-8")
        publisher.publish.assert_called_with("path1", expected_items, param="param1")

    @patch("pubsub_split.split.pubsub")
    def test_send_item_count(self, pubsub):
        publisher = MagicMock()
        pubsub.PublisherClient.return_value = publisher
        item = dict(item_id=1, name="test", variable1="whatever")
        items = [item] * 20000
        split.send("topic_path", items, param="param1")
        self.assertEqual(2, publisher.publish.call_count)

    @patch("pubsub_split.split.pubsub")
    def test_send_item_size(self, pubsub):
        publisher = MagicMock()
        pubsub.PublisherClient.return_value = publisher
        items = []
        for j in range(0, 6):
            item = dict(item_id=1, variable1="whatever")
            for i in range(0, split.BATCH_MAX_SIZE // 100):
                item[str(i)] = str(i)
            items.append(item)
        split.send("topic_path", items, param="param1")
        self.assertEqual(2, publisher.publish.call_count)

    @patch("pubsub_split.split.pubsub")
    def test_send_empty(self, pubsub):
        publisher = MagicMock()
        pubsub.PublisherClient.return_value = publisher
        split.send("topic_path", [])
        self.assertEqual(0, publisher.publish.call_count)

    @patch("pubsub_split.split.logger")
    @patch("pubsub_split.split.pubsub")
    def test_send_large(self, pubsub, logger):
        publisher = MagicMock()
        pubsub.PublisherClient.return_value = publisher
        item = {}
        for i in range(0, split.BATCH_MAX_SIZE // 10):
            item[i] = str(i)
        split.send("topic_path", [item])
        self.assertEqual(0, publisher.publish.call_count)
        self.assertTrue(logger.warning.called)

    def test_split_list(self):
        original = ["a"] * 20000
        result_left, result_right = split.split_list(original)
        self.assertEqual(10000, len(result_left))
        self.assertEqual(10000, len(result_right))
