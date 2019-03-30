import boto3

from .defaultvars import *

dynamodb = boto3.resource("dynamodb")

class DynamoDBTable():
    def __init__(self,*args,**kargs):
        self.tableName = kargs.get("tableName")
        self.primaryKey = kargs.get("primaryKey")
        self.sortKey = kargs.get("sortKey")
        self.ttl = int(kargs.get("ttl",defaultTtl))
        self.table = dynamodb.table(sel.tableName,region_name=region)

    def __call__(self,classObj):
        def put(self,data):
            self.table.put_item(Item=data)

        def get(self,primaryKey,**kargs):
            key = {
                self.primaryKey : primaryKey
            }
            sortKey = kargs.get(self.sortKey,None)
            columns = kargs.get("columns",[])
            if self.sortKey != None and sortKey != None:
                key.update({
                    self.sortKey : sortKey
                })

            response = self.table.get_item(Key=key)
            responseData = {}
            item = response.get("Item")
            if item != None:
                for column in columns:
                    responseData.update({
                        column : item.get("column")
                    })
                return responseData
            return None
