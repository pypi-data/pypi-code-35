# NOTE Keep synced with version in setup.py
# Also rebuild repository in runner_image/ and upload to dockerhub (mentice/jobber-runner)
# Also update DESCRIPTION.md history section
__version__ = '0.3.8'

from .Jobber import Jobber, parse_tag
from .config import get_config