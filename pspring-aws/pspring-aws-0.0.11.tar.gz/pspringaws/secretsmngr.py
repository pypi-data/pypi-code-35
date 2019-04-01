
import logging
import os
import boto3
logger = logging.getLogger("pspring-aws")
from .defaultvars import *
from pspring import *

@Bean()
class SecretsManager():
    def __init__(self):
        self.secretName = secretName
        self.region = region

        if self.secretName == None:
            logger.error("secretName required")
        logger.info("Getting secret : "+self.secretName)
        self.client = boto3.client('secretsmanager',region_name=self.region)
        self.secretResponse = self.getSecret()
        logger.info("Secret status : OK")

    def getSecret(self):
        return self.client.get_secret_value(SecretId=self.secretName)

    def getSecretValue(self):
        return self.secretResponse


class SecretValue():
    def __init__(self,*args,**kargs):
        self.secretName = kargs.get("name")
        self.region = kargs.get("region")
        if self.region == None:
            self.region = region
        self.column = kargs.get("column")
        self.columns = kargs.get("columns")
        self.client = boto3.client('secretsmanager',region_name=self.region)

    def __call__(self,classObj):
        def getSecretValue(selfObj):
            logger.info("Getting secret : "+self.secretName)
            self.secretResponse = self.getSecret()
            response = self.client.get_secret_value(SecretId=self.secretName)
            logger.info("Secret status : OK")
            responseData = {}
            columns = self.columns
            column = self.column
            if response != None:
                if columns != None:
                    for column in columns:
                        responseData.update({
                            column : item.get(column)
                        })
                    return responseData
                if column != None:
                    return item.get(column)
            return response
