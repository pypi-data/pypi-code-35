# config
DEBUG = False
FROM_S3 = True
UPLOAD_S3 = True
USE_COMPILED_CODE = False
CREATE_VENV_TIMEOUT = 300

ALLOWED_CODE_EXTENSION = ['.so', '.pyd', '.py']

ALLOWED_DATASET_EXTENSION = ['.tfrecords', '.csv', '.txt']

CODE_DIR_NAME = 'code'
DATASET_DIR_NAME = "dataset"
OUTPUT_DIR_NAME = "output"
LOG_DIR_NAME = 'log'

TF_CONFIG = 'TF_CONFIG'

MODEL_WIN_OUT_DIR = ".model.win.out"
MODEL_LINUX_OUT_DIR = ".model.linux.out"

EXTENSION_TAR_GZ = '.tar.gz'

DATASET_TAR_GZ = 'dataset.tar.gz'

VENV = 'venv'

# OS types
LINUX = "linux"
WIN = "win"

# File marker name
WORKER_FAILED_MARKER = "worker_run_failed"

REQUIREMENTS_TXT = "requirements.txt"

# TEMP variables
NUMBER_GPU_WORKER = 4
NUMBER_CPU_WORKER = 1

# Master server
DEFAULT_MASTER_SERVER = "http://dtf-masterserver-dev.us-west-1.elasticbeanstalk.com"

# Job type
JOB_TYPE_TENSORFLOW = "tensorflow"
JOB_TYPE_PYTORCH = "pytorch"
SUPPORTED_JOB_TYPES = [JOB_TYPE_TENSORFLOW, JOB_TYPE_PYTORCH]

# Job contents
JOB_CONTENT_TYPE_CODE = "code"
JOB_CONTENT_TYPE_DATASET = "dataset"
JOB_CONTENT_TYPE_OUTPUT = "output"
JOB_CONTENT_TYPE_SUPPORTED = [JOB_CONTENT_TYPE_CODE,
                              JOB_CONTENT_TYPE_DATASET,
                              JOB_CONTENT_TYPE_OUTPUT]

# Container settings
DDL_WORKER_USER_ID = 9999