import os
region = os.environ.get("pspring.aws.region","us-east-2") or os.environ.get("region","us-east-2")
defaultTtl = os.environ.get("pspring.aws.dynamodb.ttl","3600")

import logging
logger = logging.getLogger("pspring-aws")
