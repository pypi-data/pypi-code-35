import os
import sys
sys.path.append("./deps")

from pspring import *
from pspringaws import *

@LambdaHandler()
class TestLambdaHandler():
    def handler(self,event,context):
        raise RedirectException()

handler = TestLambdaHandler().handler

print(handler({},{}))
