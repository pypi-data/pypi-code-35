import json

class LambdaException(Exception):
    def __init__(self,**kargs):
        super().__init__(**kargs)
        self.code = kargs.get("code","500")
        self.msg = kargs.get("msg","Internal Server Error : "+str(self))
        self.errorCode = kargs.get("errorCode")

    def getResponse(self):
        return {
            "statusCode": self.code,
            "body": json.dumps({
                "message" : self.msg,
                "code" : self.errorCode
            })
        }

class NotFoundException(LambdaException):
    def __init__(self,**kargs):
        super().__init__(**kargs)
        self.code="404"

class UnAuthorizedException(LambdaException):
    def __init__(self,**kargs):
        super().__init__(**kargs)
        self.code="401"

class InternalServerException(LambdaException):
    def __init__(self,**kargs):
        super().__init__(**kargs)
        self.code="500"

class CreatedException(LambdaException):
    def __init__(self,**kargs):
        super().__init__(**kargs)
        self.code="201"

class RedirectException(LambdaException):
    def __init__(self,**kargs):
        super().__init__(**kargs)
        self.code="301"
