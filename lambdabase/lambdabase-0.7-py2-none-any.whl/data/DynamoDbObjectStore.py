import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from lambdabase.LambdaException import ResourceNotFound, OptimisticLockException


class DynamoDbObjectStore(object):
    """
    Abstraction layer around the base storage mechanism. Provides
    a consistent mechanism for accessing arbitrary storage system
    such as memory, disk or nosql data store.
    """
    def __init__(self, namespace, index, secondary_index=None, secondary_key=None, lock_key=None):
        """
        The DynamoDB object store implementation connects and interacts
        with DynamoDB using the boto3 client.
        :param namespace: the namespace to be used for this data store
        :param index: the index key to use for this table
        :param secondary_index: the secondary index key for this table
        :param secondary_key: the secondary index key for this table
        """
        self.namespace = namespace
        self.index = index
        self.secondary_index = secondary_index
        self.secondary_key = secondary_key
        self.client = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.client.Table(self.namespace)
        self.lock_key = lock_key

    def get(self, key):
        """
        Retrieve an item from DynamoDB using the specified key
        :param key: the value of the index to lookup`
        :return: the item from DynamoDB
        """
        if not self.exists(key):
            raise ResourceNotFound('The specified resource does not exist [{}]'.format(key))
        response = self.table.get_item(Key={self.index: key})
        return response.get('Item')

    def delete(self, key):
        """
        Remove the item from the data store
        :param key: the key to remove
        """
        if not self.exists(key):
            raise ResourceNotFound('The specified resource does not exist [{}]'.format(key))
        self.table.delete_item(Key={self.index: key})

    def get_secondary(self, key):
        """
        Retrieve an item from DynamoDB using the specified key
        :param key: the value of the index to lookup`
        :return: the item from DynamoDB
        """
        if self.secondary_key is None or self.secondary_index is None:
            raise ValueError('Trying to query secondary index when '
                             'one has not been configured')

        response = self.table.query(
            IndexName=self.secondary_index,
            KeyConditionExpression=Key(self.secondary_key).eq(key)
        )
        return response.get('Items')

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

        self.table.put_item(Item=item)

    def exists(self, key):
        """
        Determine if the specified key exists in the store
        :param key: The index key to check
        :return: true if the key exists, false otherwise
        """
        try:
            response = self.table.get_item(Key={self.index: key})
        except ClientError as ex:
            if ex.response.get('Error').get('Code') == 'ResourceNotFoundException':
                return False
            else:
                raise ex
        return 'Item' in response

