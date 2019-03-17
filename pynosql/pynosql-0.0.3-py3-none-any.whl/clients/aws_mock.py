from botocore.stub import Stubber


class AWSMockResponses(object):
    """ Stubber for DynamoDB Mock Responses """

    @staticmethod
    def get_item_response(client):
        """ Mock GetItem Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'Item': {
                'test1': {'S': 'value1'},
                'test2': {'S': 'value2'},
                'test3': {'S': 'value3'},
                'test4': {'S': 'value4'},
            },
            'ConsumedCapacity': {
                'TableName': 'TestTable',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('get_item', response)
        stub.activate()

    @staticmethod
    def get_empty_item_response(client):
        """ Mock Empty GetItem Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'ConsumedCapacity': {
                'TableName': 'TestTable',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('get_item', response)
        stub.activate()

    @staticmethod
    def query_response(client):
        """ Mock Query Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'Items': [
                {
                    'test1': {'S': 'value1'},
                    'test2': {'S': 'value2'},
                    'test3': {'S': 'value3'},
                    'test4': {'S': 'value4'},
                },
                {
                    'test1': {'S': 'value5'},
                    'test2': {'S': 'value6'},
                    'test3': {'S': 'value7'},
                    'test4': {'S': 'value8'},
                },
                {
                    'test1': {'S': 'value9'},
                    'test2': {'S': 'value10'},
                    'test3': {'S': 'value11'},
                    'test4': {'S': 'value12'},
                },
                {
                    'test1': {'S': 'value13'},
                    'test2': {'S': 'value14'},
                    'test3': {'S': 'value15'},
                    'test4': {'S': 'value16'},
                },
            ],
            'ConsumedCapacity': {
                'TableName': 'TestTable',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('query', response)
        stub.activate()

    @staticmethod
    def empty_query_response(client):
        """ Mock Empty Query Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'Items': [],
            'ConsumedCapacity': {
                'TableName': 'TestTable',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('query', response)
        stub.activate()

    @staticmethod
    def scan_response(client):
        """ Mock Scan Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'Items': [
                {
                    'test1': {'S': 'value1'},
                    'test2': {'S': 'value2'},
                    'test3': {'S': 'value3'},
                    'test4': {'S': 'value4'},
                },
                {
                    'test1': {'S': 'value5'},
                    'test2': {'S': 'value6'},
                    'test3': {'S': 'value7'},
                    'test4': {'S': 'value8'},
                },
                {
                    'test1': {'S': 'value9'},
                    'test2': {'S': 'value10'},
                    'test3': {'S': 'value11'},
                    'test4': {'S': 'value12'},
                },
                {
                    'test1': {'S': 'value13'},
                    'test2': {'S': 'value14'},
                    'test3': {'S': 'value15'},
                    'test4': {'S': 'value16'},
                },
            ],
            'ConsumedCapacity': {
                'TableName': 'TestTable',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('scan', response)
        stub.activate()

    @staticmethod
    def empty_scan_response(client):
        """ Mock Empty Scan Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'Items': [],
            'ConsumedCapacity': {
                'TableName': 'TestTable',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('scan', response)
        stub.activate()

    @staticmethod
    def put_item_response(client):
        """ Mock PutItem Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'Attributes': {
                'test1': {'S': 'value1'},
                'test2': {'S': 'value2'},
                'test3': {'S': 'value3'},
                'test4': {'S': 'value4'},
            },
            'ConsumedCapacity': {
                'TableName': 'string',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('put_item', response)
        stub.activate()

    @staticmethod
    def delete_item_response(client):
        """ Mock DeleteItem Response

        :param client: obj AWS Client
        :return: None
        """
        response = {
            'Attributes': {
                'test1': {'S': 'value1'},
                'test2': {'S': 'value2'},
                'test3': {'S': 'value3'},
                'test4': {'S': 'value4'},
            },
            'ConsumedCapacity': {
                'TableName': 'string',
                'CapacityUnits': 123.0,
                'Table': {
                    'CapacityUnits': 123.0
                },
                'LocalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                },
                'GlobalSecondaryIndexes': {
                    'string': {
                        'CapacityUnits': 123.0
                    }
                }
            }
        }
        stub = Stubber(client.meta.client)
        stub.add_response('delete_item', response)
        stub.activate()
