from lambdabase.LambdaException import ResourceNotFound


class MultiMapDatastore(object):
    """
    Datastore class for managing many to many relationships
    in NoSQL. Two records are stored creating a mapping
    table to allow complex lookups
    """
    def __init__(self, datastore):
        if datastore.index != 'guid':
            raise ValueError('Datastore index for multimap must be [guid]')
        self.datastore = datastore

    def add(self, key1, key2):
        """
        Store two records using key1 as the primary in
        one record and key2 as the primary in the second
        :param key1: the first key
        :param key2: the second key
        """
        if self.datastore.exists(key1):
            data = self.datastore.get(key1)
            record1 = MapItem(data.get('guid'), data.get('items'))
            record1.add(key2)
        else:
            record1 = MapItem(key1, [key2])

        if self.datastore.exists(key2):
            data = self.datastore.get(key2)
            record2 = MapItem(data.get('guid'), data.get('items'))
            record2.add(key1)
        else:
            record2 = MapItem(key2, [key1])

        self.datastore.put(record1.unload())
        self.datastore.put(record2.unload())

    def get(self, key):
        """
        Returns the values associated with the given key
        :param key: the lookup key
        """
        if self.datastore.exists(key):
            data = self.datastore.get(key)
            return data.get('items')
        return []

    def delete(self, key):
        """
        Remove a key from the multimap
            - Find the key to delete
            - Load all mapped items
            - Remove key from mapped items
            - Finally delete the actual key
        :param key: the key to remove
        """
        items = self.get(key)
        for item in items:
            mapped = self.get(item)
            mapped.remove(key)

            if len(mapped) > 0:
                self.datastore.put(MapItem(item, mapped).unload())
            else:
                self.datastore.delete(item)

        try:
            self.datastore.delete(key)
        except ResourceNotFound:
            pass


class MapItem(object):
    def __init__(self, guid, items):
        self.guid = guid
        self.items = items

    def unload(self):
        return self.__dict__

    def add(self, item):
        if item not in self.items:
            self.items.append(item)








