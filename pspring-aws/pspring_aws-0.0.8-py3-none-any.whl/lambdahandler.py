from .defaultvars import *
from pspring import PayloadException
from .lambdaexceptions import *
import json
import logging

logger = logging.getLogger("pspring-aws")

class LambdaHandler():

    def __init__(self,*args,**kargs):
        self.type = kargs.get("type","proxy")

    def __call__(self,classObj):
        handlerOrig = classObj.handler
        constructorOrig = classObj.__init__
        def constructor(*args,**kargs):
            selfObj = args[0]
            selfObj.logattrs = {}
            constructorOrig(*args,**kargs)

        def logtemplate(selfObj,logObj):
            logdict=dict()
            if type(logObj) == type(str):
                logdict.update(selfObj.logattrs)
                logdict.update({
                    "message" : logObj
                })
                return logdict
            else:
                logdict.update(selfObj.logattrs)
                logdict.update(logObj)
                return logdict

        def debug(selfObj,logObj):
            logger.debug(selfObj.logtemplate(logObj))
        def info(selfObj,logObj):
            logger.info(selfObj.logtemplate(logObj))
        def error(selfObj,logObj):
            logger.error(selfObj.logtemplate(logObj))
        def warn(selfObj,logObj):
            logger.warn(selfObj.logtemplate(logObj))

        def addToLogger(selfObj,fieldName,fieldValue):
            selfObj.logattrs.update({
                fieldName : fieldValue
            })

        def handler(*args,**kargs):
            try:
                selfObj = args[0]
                event = args[1]
                context = args[2]
                econtext = event.get('context')
                requestId = str(econtext.get('requestId'))
                selfObj.addToLogger("requestId",requestId)
                response = handlerOrig(*args,**kargs)
                return {
                    "statusCode" : "200",
                    "body" : json.dumps(response)
                }
            except LambdaException as le:
                return le.getResponse()
            except PayloadException as pe:
                return LambdaException(str(pe),pe.statusCode,pe.response).getResponse()
            except Exception as e:
                return LambdaException(str(e)).getResponse()

        classObj.handler = handler
        classObj.__init__ = constructor
        classObj.addToLogger = addToLogger
        classObj.debug = debug
        classObj.info = info
        classObj.warn = warn
        classObj.error = error
        classObj.logtemplate = logtemplate
        return classObj
