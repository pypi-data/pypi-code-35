DEBUG = False

CONFIG_FILE_NAME = "config.yaml"
CODE_TAR_GZ = 'code.tar.gz'
DATASET_TAR_GZ = 'dataset.tar.gz'
TAR_GZ_EXTENSION = 'tar.gz'

TEMP_AUTH_TOKEN = 'temp_token'

USER_CODE_EXTENSIONS = ['.py', '.gz']
MODEL_UPLOAD_EXTENSIONS = ['.pyd', '.so', '.build', '.txt', '.yaml']

SUPPORTED_JOB_TYPES = ['tensorflow', 'pytorch']
JOB_TYPE_TO_API = {
    'tensorflow': 'tf',
    'pytorch': 'pt'
}

JOB_CONTENT_TYPE_CODE = "code"
JOB_CONTENT_TYPE_DATASET = "dataset"
JOB_CONTENT_TYPE_OUTPUT = "output"

JOB_TIME_FMT = "%Y-%m-%d %H:%M:%S"

# Active job states
JOB_STATE_PENDING_UPLOAD = "pending upload"
JOB_STATE_UPLOADED = "job data uploaded"
JOB_STATE_READY = "job is ready"

# Inactive job states
JOB_STATE_CANNOT_UPLOAD = "cannot upload job data"
JOB_STATE_CANNOT_SIGNAL_JOB_READY = "failed to signal job ready"
JOB_STATE_SERVER_RESPONSE_UNEXPECTED = "unexpected server response"
JOB_STATE_SERVER_SIGNALED_STOPPED = "server signaled stop"
JOB_STATE_TERMINATED = "user stopped the job"
JOB_STATE_OUTPUT_DOWNLOADED = "output downloaded"
JOB_STATE_NO_OUTPUT = "job has no output"
