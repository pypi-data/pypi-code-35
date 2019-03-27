import os
import tempfile
from pathlib import Path

"""
This is a temporary file with a constant that's identical to the contents of
the CivilServant Loader's .env.template. This is here as a temporary
workaround until I figure out why the .env.template file isn't being stored in
the python egg despite being listed in the correct sections of config.cfg from
what I can see. This will be removed once the issue is resolved.
"""

ENV_TEMPLATE = """
# Loader Configuration
CS_CORE_LIB_URL="git+file:///Users/penn/civilservant/civilservantlib-core#egg=civilservant-core"
CS_LOADER_ACTIVE=1
CS_PACKAGE_DIR_PREFIX="civilservantlib-"
CS_PACKAGE_PREFIX="civilservant-"
CS_PACKAGE_URL_PREFIX="git+https://github.com/mitmedialab/"
CS_PROJECT_LIBS_PATH="lib"
CS_TASK_ENTRY_POINTS_GROUP="civilservant_tasks"

"""

def _get_temp_root_env():
    """Create a temporary file containing the .env.template above."""
    filename = next(tempfile._get_candidate_names())
    temp_path = Path(tempfile.gettempdir(), filename)
    with open(str(temp_path), "w") as f:
        f.write(ENV_TEMPLATE)
    return Path(temp_path)

