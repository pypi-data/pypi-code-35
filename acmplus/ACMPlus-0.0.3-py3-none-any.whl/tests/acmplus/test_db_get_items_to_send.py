from acmplus.item import ACMPlusItem
from buoy.tests.item_db_to_send_thread import DBToSendThreadTest


class TestACMPlusDBToSendThread(DBToSendThreadTest):
    item_cls = ACMPlusItem
    db_tablename = "acmplus"
