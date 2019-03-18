import sys
from os.path import dirname, join, exists
import yaml
from six import StringIO
from ddls3utils.s3utils import S3Client
import os

from dccli.constants import TEMP_AUTH_TOKEN, USER_CODE_EXTENSIONS, MODEL_UPLOAD_EXTENSIONS

test_config_path = join(dirname(__file__), "test_config.yaml")
with open(test_config_path) as f:
    test_config = yaml.load(f)

s3_client = S3Client(region_name="us-west-2",
                     aws_access_key_id="AKIAJOHKUPVKMZ66GTSQ",
                     aws_secret_access_key="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",
                     download_file_extension_filter=USER_CODE_EXTENSIONS,
                     upload_file_extension_filter=MODEL_UPLOAD_EXTENSIONS)



def capture_console_log(func):
    def wrapper(console_out):
        if "TEST" in os.environ:
            old_stdout = sys.stdout
            sys.stdout = std_out = StringIO()
            console_out = std_out.getvalue()
            func(console_out)
            sys.stdout = old_stdout
            print(console_out)
        else:
            func(None)
    return wrapper


def clean_up_login_token():
    temp_token_path = join(dirname(__file__), TEMP_AUTH_TOKEN)
    if exists(temp_token_path):
        os.remove(temp_token_path)

