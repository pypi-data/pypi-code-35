import json
import os
import sys
import traceback
from os.path import join, exists

###############################################################################

# global variables
WORKER_FAILED_MARKER = "worker_run_failed"
TF_CONFIG = 'TF_CONFIG'
WORKER_RUN_ENV_TASK_UUID = "task_uuid"
WORKER_RUN_ENV_TASK_INDEX = "task_index"
WORKER_RUN_ENV_TASK_CLUSTER_SPEC = "cluster_spec"
WORKER_RUN_ENV_TASK_ROLE = "task_role"
WORKER_RUN_ENV_WORKER_TYPE = "worker_type"
WORKER_RUN_ENV_WORKER_RESOURCE_ID = "resource_id"
WORKER_RUN_ENV_DATASET_DIR = "dataset_dir"
WORKER_RUN_ENV_CODE_DIR = "code_dir"
WORKER_RUN_ENV_OUTPUT_DIR = "output_dir"
WORKER_RUN_ENV_LOG_DIR = "log_dir"

###############################################################################

def worker_prepare_gpu(worker_type, resource_id):
    if worker_type != "gpu" or resource_id < 0:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(resource_id)
    return


def prepare_distributed_training(task_role, task_index, cluster_spec):
    worker_list = cluster_spec["worker"]
    ps_list = cluster_spec["ps"]
    cluster = {}
    cluster["chief"] = [worker_list[0]]
    cluster["worker"] = worker_list[1:]
    cluster["ps"] = ps_list
    tf_config = {
        "cluster": cluster
    }

    job_type = "worker"
    if task_role == "ps":
        job_type = "ps"
    elif task_index == 0:
        job_type = "chief"
    else:
        # worker index starts from 0
        task_index -= 1

    tf_config["task"] = {"type": job_type, "index": task_index}

    # set the TF_CONFIG in the env variable
    os.environ[TF_CONFIG] = str(tf_config).replace("'", '"')
    print("task_role: {}, task_index: {}, tf_config: {}".format(task_role, task_index, tf_config))


def worker_run():
    log_dir = None
    try:
        dataset_dir = os.environ[WORKER_RUN_ENV_DATASET_DIR]
        output_dir = os.environ[WORKER_RUN_ENV_OUTPUT_DIR]
        code_dir = os.environ[WORKER_RUN_ENV_CODE_DIR]
        log_dir = os.environ[WORKER_RUN_ENV_LOG_DIR]
        task_uuid = os.environ[WORKER_RUN_ENV_TASK_UUID]
        task_role = os.environ[WORKER_RUN_ENV_TASK_ROLE]
        task_index = int(os.environ[WORKER_RUN_ENV_TASK_INDEX])
        worker_type = os.environ[WORKER_RUN_ENV_WORKER_TYPE]
        resource_id = int(os.environ[WORKER_RUN_ENV_WORKER_RESOURCE_ID])
        cluster_spec = json.loads(os.environ[WORKER_RUN_ENV_TASK_CLUSTER_SPEC])

        print("Structure:")
        print(" - Dataset folder location: {}".format(dataset_dir))
        print(" - Code folder location: {}".format(code_dir))
        print(" - Output folder location: {}".format(output_dir))
        print(" - Log folder location: {}".format(log_dir))
        print("Task parameters:")
        print(" - task_uuid: {}".format(task_uuid))
        print(" - task_role: {}".format(task_role))
        print(" - task_index: {}".format(task_index))
        print(" - cluster_spec: {}".format(cluster_spec))
        print(" - worker_type: {}".format(worker_type))
        print(" - resource_id: {}".format(resource_id))

        # Prepare for distributed training mode.
        if task_index != -1:
            print("Distributed training mode")
            prepare_distributed_training(task_role, task_index, cluster_spec)
        else:
            print("Single worker training mode")

        worker_prepare_gpu(worker_type, resource_id)
        # Create files for user output.
        user_stdout = open(join(log_dir, "{}.log".format(task_uuid)), "w")
    except Exception as e:
        print("Exception occured: {}".format(e))
        traceback.print_exc()
        if exists(log_dir):
            with open(join(log_dir, WORKER_FAILED_MARKER), "w") as f:
                f.write(str(e))

        return

    try:
        # Starting at this point, redirect the stdout and stderr to log file
        # to pass out the user's outputs.
        sys.stdout = user_stdout
        sys.stderr = user_stdout

        # Insert the code dir into the path and import the main function.
        sys.path.insert(0, code_dir)
        p = __import__("main")

        # Invoke main function, <dataset_dir>, <output_dir>
        p.main(dataset_dir, output_dir)
    except:
        traceback.print_exc()
    finally:
        if user_stdout is not None:
            user_stdout.close()


if __name__ == '__main__':
    worker_run()
