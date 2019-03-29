
import logging
import os
import boto3
logger = logging.getLogger("summer-aws")
from pspring import *

@Bean()
class SecretsManager():
    def __init__(self):
        self.secretName = os.environ.get("summer.aws.secretsMngr.secretName")
        if os.environ.get("summer.aws.secretsMngr.region") != None:
            self.region = os.environ.get("summer.aws.secretsMngr.region")
        elif os.environ.get("summer.aws.region") != None:
            self.region = os.environ.get("summer.aws.region")
        else:
            self.region = "us-east-1"
        if self.secretName == None:
            logger.error("secretName required")
        logger.info("Getting secret : "+self.secretName)
        self.client = boto3.client('secretsmanager')
        self.secretResponse = self.getSecret()
        logger.info("Secret status : OK")

    def getSecret(self):
        return self.client.get_secret_value(SecretId=self.secretName)

    def getSecretValue(self):
        return self.secretResponse
