
from .image import Image, take_photos
from .ui import show_question, show_message

import atexit
import os
import signal
import platform
import sys

# the lib mxnet should be imported as the last lib to fix some subporcess issue in Windows-7
#TODO:fix mxnet import problem by fix its subprocess
def _terminate_mxnet():
    # Fix issue https://github.com/apache/incubator-mxnet/issues/9271
    if "mxnet" in sys.modules and platform.platform().startswith("Windows-7"):
        os.kill(os.getpid(), signal.SIGTERM)

atexit.register(_terminate_mxnet)
