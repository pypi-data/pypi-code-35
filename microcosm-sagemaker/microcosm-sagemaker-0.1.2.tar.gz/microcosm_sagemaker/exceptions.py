"""
SageMaker-specific exception handling.

"""
from sys import exit, stderr
from traceback import format_exc

from microcosm_sagemaker.constants import SagemakerPath


def handle_sagemaker_exception(exception):
    traceback = format_exc()
    description = "Exception during training: " + str(exception) + "\n" + traceback + "\n"

    if not SagemakerPath.OUTPUT.exists():
        return

    # Record the failure in a format that is saved along with the training run
    with open(SagemakerPath.OUTPUT / "failure", "w") as error_log:
        error_log.write(description)

    # Also display the status in the job logs
    stderr.write(description)

    # Mark training job as failed
    exit(255)
