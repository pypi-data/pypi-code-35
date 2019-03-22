from lambdabase.LambdaException import ResourceNotFound, OptimisticLockException


class MemoryObjectStore(object):
    """
    In memory object store matching the behaviour of DynamoDB
    """
    def __init__(self, namespace, index, secondary_index=None, secondary_key=None, lock_key=None):
        """
        The DynamoDB object store implementation connects and interacts
        with DynamoDB using the boto3 client.
        :param namespace: the namespace to be used for this data store
        :param index: the index to use for this table
        :param secondary_index: the secondary index for this tabe
        :param secondary_key: the secondary index key for this table
        :param the lock key for this table (ignored for in-memory store)
        """
        self.store = {}
        self.namespace = namespace
        self.index = index
        self.secondary_index = secondary_index
        self.secondary_key = secondary_key
        self.lock_key = lock_key

    def get(self, key):
        """
        Returns the specified key
        :param key: the index of the object
        :return: the object retrieved from the store
        """
        if not self.exists(key):
            raise ResourceNotFound('The specified resource does not exist [{}]'.format(key))
        return self.store[key]

    def delete(self, key):
        """
        Remove the item from the data store
        :param key: the key to remove
        """
        if not self.exists(key):
            raise ResourceNotFound('The specified resource does not exist [{}]'.format(key))
        del self.store[key]

    def get_secondary(self, key):
        """
        Retrieve an item from DynamoDB using the specified key
        :param key: the value of the index to lookup`
        :return: the item from DynamoDB
        """
        matches = {k: v for k, v in self.store.iteritems()
                   if v[self.secondary_key] == key}
        return matches.values()

    def put(self, item):
        """
        Stores the specified value in the specified key
        :param item: the item to store
        """
        if self.exists(item.get(self.index)) and self.lock_key:
            key = item.get(self.index)
            db_item = self.get(key)
            db_version = db_item.get(self.lock_key)
            item_version = item.get(self.lock_key)
            if db_version != item_version:
                raise OptimisticLockException(item_version, db_version)
            item[self.lock_key] = item_version + 1

        key = item[self.index]
        self.store[key] = item

    def exists(self, key):
        """
        Tests if the specified itemn exists in the store
        """
        return key in self.store
