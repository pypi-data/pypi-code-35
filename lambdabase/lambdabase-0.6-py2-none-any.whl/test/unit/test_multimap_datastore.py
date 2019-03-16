from unittest import TestCase

from lambdabase.data.MultiMapDatastore import MultiMapDatastore
from lambdabase.local.data.MemoryObjectStore import MemoryObjectStore


class MultiMapDatastoreTests(TestCase):
    """
    Validate the multimap datastore functions correctly
    """
    def setUp(self):
        self.datastore = MemoryObjectStore('namespace', 'guid')

    def test_adding_single_key(self):
        """
        Validate a single key can be added to the MultiMap
        """
        map_store = MultiMapDatastore(self.datastore)
        map_store.add('key_1', 'key_a')
        items_1 = map_store.get('key_1')
        items_a = map_store.get('key_a')

        self.assertTrue(items_1[0] == 'key_a')
        self.assertTrue(items_a[0] == 'key_1')

    def test_adding_multiple_keys(self):
        """
        Validate multiple keys can be added to the MultiMap
        """
        map_store = MultiMapDatastore(self.datastore)
        map_store.add('key_1', 'key_a')
        map_store.add('key_2', 'key_b')
        items_1 = map_store.get('key_1')
        items_2 = map_store.get('key_2')

        self.assertTrue(items_1[0] == 'key_a')
        self.assertTrue(items_2[0] == 'key_b')

    def test_adding_shared_keys(self):
        """
        Validate the same value can be added to multiple keys in the MultiMap
        """
        map_store = MultiMapDatastore(self.datastore)
        map_store.add('key_1', 'key_a')
        map_store.add('key_2', 'key_a')
        map_store.add('key_3', 'key_a')
        items_1 = map_store.get('key_1')
        items_2 = map_store.get('key_2')
        items_3 = map_store.get('key_3')
        items_a = map_store.get('key_a')

        self.assertTrue(items_1[0] == 'key_a')
        self.assertTrue(items_2[0] == 'key_a')
        self.assertTrue(items_3[0] == 'key_a')
        self.assertTrue(items_a[0] == 'key_1')
        self.assertTrue(items_a[1] == 'key_2')
        self.assertTrue(items_a[2] == 'key_3')

    def test_adding_multiple_items(self):
        """
        Validate multiple items can be added to multiple keys
        """
        map_store = MultiMapDatastore(self.datastore)
        map_store.add('key_1', 'key_a')
        map_store.add('key_1', 'key_b')
        map_store.add('key_1', 'key_c')
        map_store.add('key_2', 'key_d')
        map_store.add('key_2', 'key_e')
        items_1 = map_store.get('key_1')
        items_2 = map_store.get('key_2')

        self.assertTrue(items_1[0] == 'key_a')
        self.assertTrue(items_1[1] == 'key_b')
        self.assertTrue(items_1[2] == 'key_c')
        self.assertTrue(items_2[0] == 'key_d')
        self.assertTrue(items_2[1] == 'key_e')

    def test_bidirectional_mapping(self):
        """
        Test multi-directional mapping for keys and values
        """
        map_store = MultiMapDatastore(self.datastore)
        map_store.add('key_1', 'key_a')
        map_store.add('key_1', 'key_b')
        map_store.add('key_a', 'key_c')

        items_1 = map_store.get('key_1')
        items_a = map_store.get('key_a')
        items_b = map_store.get('key_b')
        items_c = map_store.get('key_c')

        self.assertTrue(items_1[0] == 'key_a')
        self.assertTrue(items_1[1] == 'key_b')
        self.assertTrue(items_a[0] == 'key_1')
        self.assertTrue(items_a[1] == 'key_c')
        self.assertTrue(items_b[0] == 'key_1')
        self.assertTrue(items_c[0] == 'key_a')

    def test_simple_removal(self):
        """
        Test the simple case of removing a key
        """
        map_store = MultiMapDatastore(self.datastore)
        map_store.add('key_1', 'key_a')
        map_store.delete('key_1')

        items_1 = map_store.get('key_1')
        items_a = map_store.get('key_a')

        self.assertTrue(len(items_1) == 0)
        self.assertTrue(len(items_a) == 0)

    def test_multi_item_delete(self):
        """
        Test removing a key when it exists in multiple other key maps
        """
        map_store = MultiMapDatastore(self.datastore)
        map_store.add('key_1', 'key_a')
        map_store.add('key_1', 'key_b')
        map_store.add('key_1', 'key_c')

        map_store.add('key_2', 'key_a')
        map_store.add('key_2', 'key_d')
        map_store.add('key_2', 'key_e')

        map_store.delete('key_a')

        items_1 = map_store.get('key_1')
        items_2 = map_store.get('key_2')
        items_a = map_store.get('key_a')

        self.assertTrue(len(items_a) == 0)
        self.assertTrue(items_1[0] == 'key_b')
        self.assertTrue(items_1[1] == 'key_c')
        self.assertTrue(items_2[0] == 'key_d')
        self.assertTrue(items_2[1] == 'key_e')
