import boto3

from .defaultvars import *


class DynamoDBTable():
    def __init__(self,*args,**kargs):
        self.tableName = kargs.get("tableName")
        self.primaryKey = kargs.get("primaryKey")
        self.sortKey = kargs.get("sortKey")
        self.ttl = int(kargs.get("ttl",defaultTtl))
        dynamodb = boto3.resource("dynamodb",region_name=region)
        self.table = dynamodb.Table(self.tableName)

    def __call__(self,classObj):
        def put(selfObj,data):
            self.table.put_item(Item=data)

        def get(selfObj,primaryKey,**kargs):
            key = {}
            key[self.primaryKey] = primaryKey
            sortKey = kargs.get(self.sortKey,None)
            columns = kargs.get("columns",None)
            column = kargs.get("column",None)
            if self.sortKey != None and sortKey != None:
                key.update({
                    self.sortKey : sortKey
                })

            response = self.table.get_item(Key=key)
            responseData = {}
            item = response.get("Item")
            if item != None:
                if columns != None:
                    for column in columns:
                        responseData.update({
                            column : item.get(column)
                        })
                    return responseData
                if column != None:
                    return item.get(column)
            return None
        classObj.put = put
        classObj.get = get
        return classObj
