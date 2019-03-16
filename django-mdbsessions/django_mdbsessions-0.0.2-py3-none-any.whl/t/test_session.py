import time
from unittest import TestCase
from django.conf import settings
from pymongo import MongoClient

from mdbsession.session import SessionStore


db = MongoClient()['mdbsession_test']


class TestSessionStore(TestCase):

    def setUp(self):
        # self.store = SessionStore()
        pass

    def tearDown(self):
        # clean up – remove database
        # print('Tested inside:', db.name)
        db.client.drop_database(db.name)

    def test_basic(self):
        store = SessionStore()
        self.assertFalse(store.modified)
        store['session_var'] = 'session_var_value'

        self.assertTrue(store.modified)
        self.assertEqual(store['session_var'], 'session_var_value')


    def test_we_can_save_session(self):
        store = SessionStore()
        store['var1'] = 'var1-value'
        store.save()

        self.assertIsNotNone(store.session_key)
        self.assertTrue(store.exists(store.session_key))


    def test_we_can_delete_session(self):
        store = SessionStore()
        store['var1'] = 'var1-value'
        store.save()
        store.delete()

        self.assertFalse(store.exists(store.session_key))
        self.assertIsNone(store.session_key)


    def test_we_can_flush_session(self):
        store = SessionStore()
        store['var1'] = 'var1-value'
        store.save()
        k = store.session_key
        store.flush()

        self.assertFalse(store.exists(k))
        self.assertIsNone(store.session_key)


    def test_we_can_store_and_retrieve_many_items(self):
        def make_pair(n):
            return 'bar-{}'.format(n), '{}-foo'.format(n)
        store = SessionStore()
        size = 12
        for n in range(12):
            k, v = make_pair(n)
            store[k] = v
        store.save()
        k = store.session_key
        store2 = SessionStore(session_key=k)
        store2.load()
        for n in range(12):
            k, v = make_pair(n)
            self.assertEqual(store2[k], v)


    def test_session_data_expires(self):
        store = SessionStore()
        store['key'] = 'value to expire'
        store.save()
        k = store.session_key
        self.assertTrue(store.exists(k))
        time.sleep(4)
        self.assertFalse(store.exists(k))
