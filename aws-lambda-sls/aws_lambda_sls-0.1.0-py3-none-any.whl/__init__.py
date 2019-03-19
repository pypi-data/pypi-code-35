from aws_lambda_sls.app import LambdaSls, register_function
from aws_lambda_sls.invoke import LambdaService, KinesisService


__version__ = '0.1.0'


__all__ = [
    "LambdaSls",
    "LambdaService",
    "KinesisService",
    "register_function"
]
