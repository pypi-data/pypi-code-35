APP_VERSION = '1.0'


TEMPLATE_APP = """\
# -*- coding: utf-8 -*-
from aws_lambda_sls.app import LambdaSls


app = LambdaSls("%s")
app.run()
"""


DEFAULT_STAGE_NAME = 'dev'
DEFAULT_PACKAGE_DIST = 'dist'
DEFAULT_LOCAL_DIST = '.aws_lambda_sls/project'
DEFAULT_LAMBDA_TIMEOUT = 60
DEFAULT_LAMBDA_MEMORY_SIZE = 128
DEFAULT_LAMBDA_RUN_TIME = "python3.6"
MAX_LAMBDA_DEPLOYMENT_SIZE = 50 * (1024 ** 2)

DEFAULT_AWS_S3_BUCKET = "aws_serverless-deploys"
DEFAULT_AWS_CONNECTION_TIMEOUT = 60
DEFAULT_AWS_READ_TIMEOUT = 60
DEFAULT_AWS_MAX_RETRY = 3
DEFAULT_PACKAGE_FILE = "deployment.zip"


WELCOME_PROMPT = r"""
Please enter the project name"""


MISSING_DEPENDENCIES_TEMPLATE = r"""
Could not install dependencies:
%s
You will have to build these yourself and vendor them in the vendor folder.
"""

DEFAULT_SAM_FILE = "sam.json"

GITIGNORE = """\
sample/
.cache
venv
docs/build/
.idea
__pycache__/
.coverage
.hypothesis/
.pytest_cache/
.mypy_cache/
*.pyc
dist/
src/
.git
"""

REQUIRE_PYTHON_VERSION = "python3.6"


PACKAGE_EXLUDE_LIB = [
    "importreqs",
    "pip",
    "wheel",
    "easy_install"
]
