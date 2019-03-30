
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
