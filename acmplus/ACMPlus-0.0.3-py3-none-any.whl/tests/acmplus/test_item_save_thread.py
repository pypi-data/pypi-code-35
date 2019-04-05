import unittest
from datetime import datetime, timezone
from buoy.tests.item_save_thread import ItemSaveThreadTest
from acmplus.item import ACMPlusItem


def get_item():
    data = {
        'date': datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        'vx': '19.57',
        'vy': '69.24',
        'speed': '71.9525016938258',
        'direction': '15.7824191508417',
        'water_temp': '24.1'
    }
    return ACMPlusItem(**data)


class TestACMPlusItemSaveThread(ItemSaveThreadTest):
    __test__ = True


if __name__ == '__main__':
    unittest.main()
