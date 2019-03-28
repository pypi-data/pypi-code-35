from webplatform_cli.containers import *
from webplatform_cli.lib import *
from webplatform_cli.dependencies import *
from webplatform_cli.tasks import *
from webplatform_cli import cli
from webplatform_cli import handler

import os, sys

controller_path = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.abspath(os.path.join(controller_path))

if base_path not in sys.path:
   sys.path.append(base_path)

if controller_path not in sys.path:
   sys.path.append(controller_path)
