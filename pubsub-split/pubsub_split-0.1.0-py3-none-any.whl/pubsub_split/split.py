import json
import logging
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from google.cloud import pubsub_v1 as pubsub

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
BATCH_MAX_ITEMS = 10000
BATCH_MAX_SIZE = 10 * 1024 * 1024


def send(topic_path, items, **kwargs):
    if len(items) == 0:
        logger.warning("No items to send")
        return

    if len(items) > BATCH_MAX_ITEMS:
        total = len(items) // BATCH_MAX_ITEMS
        logger.info(f"Too many items to publish, splitting into {total} batches")
        for begin_index in range(0, len(items), BATCH_MAX_ITEMS):
            batch = items[begin_index : begin_index + BATCH_MAX_ITEMS]
            send(topic_path, batch, **kwargs)
        return

    data = json.dumps(items).encode("utf-8")
    if len(data) > BATCH_MAX_SIZE:
        items_left_half, items_right_half = split_list(items)
        if len(items) == 1:
            logger.warning("Item is too big to be sent via pubsub")
        else:
            logger.info(f"Items of size {len(data)} too large, splitting in half")
            send(topic_path, items_left_half, **kwargs)
            send(topic_path, items_right_half, **kwargs)
        return

    publisher = pubsub.PublisherClient()
    publisher.publish(topic_path, data, **kwargs)


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]
