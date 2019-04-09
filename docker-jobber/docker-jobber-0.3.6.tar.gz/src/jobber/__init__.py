# NOTE Keep synced with version in setup.py
# Also rebuild repository in runner_image/ and upload to dockerhub (mentice/jobber-runner)
__version__ = '0.3.6'

from .Jobber import Jobber, parse_tag
from .config import get_config