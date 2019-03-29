
import logging

logger = logging.getLogger("summer-aws")

@Bean(name="awsSecretMngr")
class SecretsManager():
    def __init__(self,**kargs):
        if kargs.get("secretName") == None:
            logger.error("secretName required")
