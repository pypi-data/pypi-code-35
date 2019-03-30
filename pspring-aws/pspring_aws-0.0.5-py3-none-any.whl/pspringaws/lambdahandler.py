from .defaultvars import *
from .lambdaexceptions import *
import json

class LambdaHandler():

    def __init__(self,*args,**kargs):
        self.type = kargs.get("type","proxy")

    def __call__(self,classObj):
        handlerOrig = classObj.handler
        def handler(*args,**kargs):
            try:
                response = handlerOrig(*args,**kargs)
                return {
                    "statusCode" : "200",
                    "body" : json.dumps(response)
                }
            except LambdaException as le:
                return le.getResponse()
            except Exception as e:
                return LambdaException(msg=str(e)).getResponse()

        classObj.handler = handler
        return classObj
