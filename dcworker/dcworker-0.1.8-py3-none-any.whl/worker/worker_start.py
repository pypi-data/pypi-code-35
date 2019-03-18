import copy
import hashlib
import os.path
from datetime import datetime
from multiprocessing import Process
from os.path import exists, join, realpath, dirname, isfile, \
    isdir, getsize
from sys import platform
from time import sleep
import requests
from typing import Dict, Any
import docker

from common.dbinterface import *
from common.global_variable import *
from common.training_task import TrainingTask
from common.util.common_utils import *
from worker.worker_log.user_logger import UserLogStream
from worker.worker_log.worker_logger import worker_logger
from worker.worker_runtime import *
from worker.worker_util.worker_util import download_file_from_s3, upload_output, upload_log

###############################################################################

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

CONTAINER_WORK_DIR = "/runtime"
CONTAINER_DATASET_DIR_LOCATION = "/data"
CONTAINER_CODE_DIR_LOCATION = "{}/{}".format(CONTAINER_WORK_DIR, CODE_DIR_NAME)
CONTAINER_OUTPUT_DIR_LOCATION = "{}/{}".format(CONTAINER_WORK_DIR, OUTPUT_DIR_NAME)
CONTAINER_LOG_DIR_LOCATION = "{}/{}".format(CONTAINER_WORK_DIR, LOG_DIR_NAME)
CONTAINER_VENV_LOCATION = "{}/{}".format(CONTAINER_WORK_DIR, VENV)

CONTAINER_TENSORFLOW = "wshen1991/ddl_worker_tf_gpu:latest"
CONTAINER_PYTORCH = "wshen1991/ddl_worker_pt_gpu:latest"

###############################################################################

os_platform = None
if platform.startswith("linux"):
    os_platform = LINUX
elif platform.startswith("win"):
    os_platform = WIN
else:
    raise Exception("{} is not supported".format(str(platform)))


###############################################################################

class TaskContext(object):
    exec_process = None
    log_process = None
    retry_count = 10
    logdir = None
    container_alive_states = ["running", "created"]
    user_log_stream = None
    is_alive = True

    def __init__(self, logger, logdir, exec_process=None, exec_container=None):
        self.exec_process = exec_process
        self.exec_container = exec_container
        self.logger = logger
        self.logdir = logdir
        # Sanity check: exactly one of exec_process and exec_container must be
        # present.
        if exec_process is not None and exec_container is not None:
            raise RuntimeError("cannot run in both bare metal and container mode")
        elif exec_process is None and exec_container is None:
            raise RuntimeError("no running context")

    def monitor(self):
        if self.exec_process is not None:
            alive = True if self.exec_process.poll() is None else False
        else:
            self.exec_container.reload()
            self.logger.log_info(
                "TaskContext",
                "container state: {}".format(self.exec_container.status))

            alive = True if self.exec_container.status in self.container_alive_states else False

        # If there is a failure marker, this run is not graceful (i.e. our
        # code failed).
        graceful = True
        failure_path = join(self.logdir, WORKER_FAILED_MARKER)
        if exists(failure_path):
            graceful = False
            with open(failure_path, "r") as f:
                self.logger.log_error(
                    "TaskContext",
                    "monitor error: {}".format(f.read()))

        self.is_alive = alive
        return alive, graceful

    def terminate(self):
        if self.exec_process is not None and self.exec_process.poll() is None:
            self.exec_process.kill()
        elif self.exec_container is not None:
            self.exec_container.reload()
            if self.exec_container.status in self.container_alive_states:
                try:
                    self.exec_container.kill()
                except:
                    pass

        if self.log_process.is_alive():
            self.log_process.terminate()
            self.log_process.join()

        return

    def can_retry(self):
        if self.retry_count <= 0:
            return False

        self.retry_count -= 1
        return True

    def dump_output(self):
        if self.exec_process is not None:
            self.exec_process.wait()
            while self.exec_process.poll() is None:
                line = self.exec_process.stdout.readline().decode('utf-8')
                if line and line != "":
                    self.logger.log_info("exec_process", line.rstrip('\n'))
        else:
            self.exec_container.wait()
            output = self.exec_container.logs().decode().split('\n')
            for line in output:
                self.logger.log_info("exec_container", line.rstrip('\n'))


###############################################################################

class Worker(object):
    # local ip and port
    auth_token = None
    worker_type = None
    resource_id = None
    last_error = None
    worker_logger = None
    temp_token = None
    tensorboard_process = None
    task = None
    task_uuid = None
    task_context = None

    def __init__(self,
                 master_server,
                 port,
                 workdir,
                 toplevel_datadir,
                 worker_uuid,
                 gpu_id=-1,
                 worker_type="gpu",
                 passcode=None):

        # local endpoint http://127.0.0.1:8000
        self.master_endpoint = master_server
        self.port = port
        self.workdir = workdir
        self.toplevel_datadir = toplevel_datadir
        self.worker_logger = worker_logger(worker_uuid)
        self.resource_id = gpu_id
        self.worker_uuid = worker_uuid
        self.worker_type = worker_type
        self.passcode = passcode

    # --------------------------------------------------------------------------

    # register worker to create account
    # return {success}, {uuid}
    @classmethod
    def register(cls, master_endpoint, worker_type="gpu", secret=None):
        register_logger = worker_logger(os.getpid())
        request_body = {"machine_spec_cpu": 0, "machine_spec_gpu": 1}
        if secret is not None:
            request_body["secret"] = secret

        success, status_code, response_body, error_message = request_server(
            master_endpoint + "/api/v1/worker/register/",
            'post',
            **{"data": request_body})

        if not success:
            register_logger.log_error("register", error_message)
            return False, None, None

        if status_code == 200:
            uuid = response_body.get("uuid", None)
            if not uuid:
                register_logger.log_error("register", "unexpected uuid from server")
                return False, None, None

            register_logger.log_info("register", "worker uuid: {0}".format(uuid))
            passcode = response_body.get("passcode", None)
            if not uuid:
                register_logger.log_error("register", "unexpected passcode from server")
                return False, None, None

            register_logger.worker_id = uuid
            register_logger.worker_type = worker_type
            register_logger.log_info("register", "worker register succeed")
            return True, uuid, passcode
        else:
            register_logger.log_error("register", "status {0}, error '{1}'".format(
                status_code,
                response_body.get("error")))

            return False, None, None

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                self.master_endpoint: <str>
                self.worker_uuid: <str>
                self.worker_type: <str> ("cpu" | "gpu")
                self.resource_id: <int>
                self.passcode: <str>
                self.workdir: <str>

            Produce:
                All files inside self.workdir will be deleted.
                self.auth_token: <TokenAuth> will contain the token for
                interacting with the master server.
                self.task set to None.
                self.task_uuid set to None.

        @returns
            success
            - success: <bool> Whether the enroll was successful.

    '''

    def enroll(self, fake_enroll_response: Dict[str, Any] = None):
        self.task_uuid = None
        self.task = None
        if self.worker_uuid is None:
            self.worker_logger.log_error("enroll", "missing worker uuid")
            return False

        # Get uuid of the worker, update the logger.
        self.worker_logger.worker_id = self.worker_uuid

        # Validate workdir
        if self.workdir is None:
            self.worker_logger.log_error("enroll", "None workdir")
            return False

        if not isdir(self.workdir):
            self.worker_logger.log_warning(
                "enroll",
                "invalid workdir: {}. Attempt to make a new one".format(
                    self.workdir))

            try:
                os.mkdir(self.workdir)
            except Exception as e:
                self.worker_logger.log_error(
                    "enroll",
                    "failed to create workdir at {}, error: {}".format(
                        self.workdir,
                        str(e)))

                traceback.print_exc()
                return False

        # Clear the workdir.
        self._cleanup_workdir()

        # Get type of the worker, update the logger.
        if self.worker_type != "cpu" and self.worker_type != "gpu":
            self.worker_logger.log_error(
                "enroll",
                "unexpected type for the worker: {}".format(self.worker_type))

            return False

        self.worker_logger.worker_type = self.worker_type
        self.worker_logger.resource_id = self.resource_id

        # Get passcode of the worker.
        if self.passcode is None:
            self.worker_logger.log_error(
                "enroll",
                "cannot find passcode for the worker")

            return False

        # First attempt to see if there is a simulated enroll. If not, request
        # the server for real enroll.
        request_body = {'uuid': self.worker_uuid, 'passcode': self.passcode}
        success, \
        status_code, \
        response_body, \
        error_message = request_server(
            self.master_endpoint + "/api/v1/worker/enroll/",
            'post',
            **{"data": request_body})

        # if there is fake_enroll_response
        # update corresponding values in the actual response
        if fake_enroll_response is not None:
            response_body.update(fake_enroll_response)
            status_code = 200
            success = True

        if not success:
            self.worker_logger.log_error("enroll", error_message)
            return False

        if status_code == 200:
            auth_token = response_body.get('auth_token', None)
            if not auth_token:
                self.worker_logger.log_error(
                    "enroll",
                    "no auth token from server")

                return False

            self.auth_token = TokenAuth(auth_token)
            self.worker_logger.log_info("enroll", "success")
            return True
        else:
            self.worker_logger.log_error("enroll",
                                         "status code {0}, error {1}".format(
                                             status_code,
                                             response_body.get("error")))

            return False

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                self.auth_token: <TokenAuth>
                self.master_endpoint: <str>

            Produce:
                self.task_uuid: <str> will contain the uuid of the task.
                self.task: <TrainTask> will contain the task information.
                self.temp_token: <dict> will contain the S3 authentication for
                fetching code and data.

        @returns
            success, task_ready, re_enroll, need_cleanup
            - success: <bool> Whether API is successful.
            - task_ready: <bool> Whether polled a task.
            - re_enroll: <bool> Whether need to re-enroll.
            - need_cleanup: <bool> Whether task_cleanup must be called.

    '''

    def poll(self, is_poll_no_task: bool = False, simulate_job_response: Dict[str, Any] = None):
        self.task = None
        self.task_uuid = None
        if self.auth_token is None:
            self.worker_logger.log_error(
                "poll",
                "worker has no auth token, need enroll")

            return False, False, True, False

        if is_poll_no_task:
            self.worker_logger.log_info(
                "poll",
                "no task is ready for the worker [simulated]")

            return True, False, False, False

        request_body = {'port': self.port}

        success, \
        status_code, \
        response_body, \
        error_message = request_server(
            self.master_endpoint + "/api/v1/worker/poll/",
            'post',
            **{"data": request_body,
               "auth": self.auth_token})

        # if there is simulated job response
        # update corresponding values in the actual response
        if simulate_job_response is not None:
            response_body.update(simulate_job_response)

            # Set status code to 200.
            success = True
            status_code = 200

        if not success:
            self.worker_logger.log_error("poll", error_message)
            # Requesting server failed. Since we are in poll, there must
            # not be a task associated with the worker. Exit.
            # Note: in this case, there is no need to call task_cleanup
            # as there is no real task polled.
            return False, False, False, False

        # Server indicates that no task is ready for the worker.
        if status_code == 202:
            self.worker_logger.log_info(
                "poll",
                "no task is ready for the worker")

            return True, False, False, False

        # Server indicates that a task is ready for the worker.
        elif status_code == 200:
            self.worker_logger.log_info("poll", "task is ready for the worker")

            try:
                # config is a required key in response body,
                # raise exception if it does not exist
                config =  json.loads(response_body["config"])
                task = TrainingTask(**config)
            except Exception as e:
                self.worker_logger.log_error(
                    "poll",
                    "unexpected task config from server: {}".format(str(e)))

                # Note that here we need to clean up the task as we've
                # already polled it.
                return False, False, False, True

            self.task = task
            self.task_uuid = self.task.task_uuid
            return True, True, False, False

        # Server indicates that the current auth_token is no longer valid.
        elif status_code == 401:
            self.worker_logger.log_error(
                "poll",
                "auth_token expired. worker needs to enroll again")

            return False, False, True, False

        # Other errors from server.
        else:
            self.worker_logger.log_error(
                "poll",
                "status code {}, error {}".format(
                    status_code,
                    response_body.get("error")))

            return False, False, False, False

    # --------------------------------------------------------------------------

    '''

        @abstract

            Wait for a while before attempt polling again.

        @returns
            None. This routine always succeeds.

    '''

    def poll_wait(self):
        sleep(30)

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                self.task_uuid: <str>
                self.temp_token: <dict>
                self.task: <TrainingTask>
                self.toplevel_datadir: <str>

            Produce:
                code is downloaded to /workdir/CODE_DIR_NAME/
                dataset is downloaded to /toplevel_datadir/dataset_name/
                self.task.dataset_name: <str> will contain the name of the
                dataset referenced.
                self.task.dataset_local_path: <str> will contain the local path
                to the dataset.

        @returns
            success
            - success: <bool> Whether successfully downloaded everything.

    '''

    def fetch(self, download_code: bool = True, download_dataset: bool = True):
        # Download code to /workdir/CODE_DIR_NAME/
        try:
            if download_code:
                success = self._download_code()
                if not success:
                    return False
        except Exception as e:
            self.worker_logger.log_error(
                "fetch",
                "failed to fetch code: {}".format(str(e)))

            traceback.print_exc()
            return False

        # download dataset
        try:
            if download_dataset:
                success = self._download_dataset()
                if not success:
                    return False
        except Exception as e:
            self.worker_logger.log_error(
                "fetch",
                "failed to fetch dataset: {}".format(str(e)))

            traceback.print_exc()
            return False

        return True

    def _download_unzip_in_dir(self, dir):
        # This routine unzip the TAR.GZ files inside the given dir. And it will
        # delete all the zip files.
        for item in os.listdir(dir):
            path = join(dir, item)
            if isfile(path):
                if item.lower().endswith(EXTENSION_TAR_GZ):
                    # TODO: This routine does not handle nested zip files.
                    # Should it? Also, it does not check whether the files
                    # unzipped will be a collision with the existing files.
                    unzip_tarfile(path, dir)
                    os.remove(path)

    def _download_from_presigned_url(self, download_to, download_urls):
        try:
            for (hint, url) in download_urls:
                response = requests.get(url, allow_redirects=True)
                if not response.ok:
                    self.worker_logger.log_error(
                        "download",
                        "cannot download dataset from {}".format(url))

                    return False

                file_loc = join(download_to, hint)
                with open(file_loc, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=128):
                        fd.write(chunk)

                # Sanity check the file is written.
                if not isfile(file_loc):
                    self.worker_logger.log_error(
                        "download",
                        "cannot find downloaded code at {}".format(file_loc))

                    return False

                self.worker_logger.log_info(
                    "download",
                    "download code from {} to {}".format(
                        url,
                        file_loc))

            return True
        except Exception as e:
            self.worker_logger.log_error(
                "download",
                "cannot download dataset: {}".format(str(e)))
            traceback.print_exc()
            return False

    def _download_code(self):
        code_dir = self._get_code_dir_location()
        os.makedirs(code_dir)

        # Get code PreSigned URLs. Note that code must always be in the download
        # urls as validated already inside poll.
        code_download_urls = self.task.download_urls[JOB_CONTENT_TYPE_CODE]
        success = self._download_from_presigned_url(code_dir, code_download_urls)
        if not success:
            return False

        # Finally unzip the code downloaded.
        self._download_unzip_in_dir(code_dir)
        return True

    def _download_dataset(self):
        # Only worker needs to download datasets.
        if self.task.task_role != "worker":
            return True

        # First check if there is a dataset matches with the given datase
        dataset_name = self.task.dataset_name
        dataset_persist = 1 if self.task.is_dataset_persisted else 0
        # Note that for worker role, dataset must be in the download urls as
        # validated by poll.
        dataset_download_urls = self.task.download_urls[JOB_CONTENT_TYPE_DATASET]
        self.worker_logger.log_info(
            "download_dataset",
            "Download {} From {} [p:{}]".format(dataset_name,
                                                dataset_download_urls,
                                                dataset_persist))

        # Get the local path to the dataset
        wait_for_dataset_ready = False
        download_dataset = False
        dataset_local_path = self._get_dataset_local_path(dataset_name)
        self.task.dataset_local_path = dataset_local_path

        # If there does not exist a local folder containing the dataset, then
        # the current worker will attempt to download.
        if not isdir(dataset_local_path):
            download_dataset = True
        else:
            wait_for_dataset_ready = True

        dataset_downloaded = False
        if download_dataset:
            # First attempt to create an entry in the datasets table. If this
            # fails, it is possible that someone else won the race. Just
            # wait.

            dataset_to_insert = (dataset_name,
                                 dataset_local_path,
                                 str(dataset_persist),
                                 "0",  # Not ready
                                 "1")  # +1 ref count

            success, _ = insert_table(DATASET_INSERT_COMMAND,
                                      values=dataset_to_insert)

            if not success:
                self.worker_logger.log_warning(
                    "download_dataset",
                    "failed to insert an entry for {}, start waiting!".format(
                        dataset_name))

                wait_for_dataset_ready = True
            else:
                self.worker_logger.log_info(
                    "download_dataset",
                    "insert an entry for {}, start downloading!".format(
                        dataset_name))

                wait_for_dataset_ready = False

            if not wait_for_dataset_ready:
                # We really need to download. Make a sanity check that the
                # dataset_local_path is still not existing.
                if isdir(dataset_local_path):
                    # This should not happen. Log this error, nuke the dataset
                    # from the db and exit.
                    self.worker_logger.log_error(
                        "download_dataset",
                        "{} already exists before downloading for {}".format(
                            dataset_local_path,
                            dataset_name))

                    shutil.rmtree(dataset_local_path, ignore_errors=True)
                    delete_from_table(DATASET_DELETE_COMMAND,
                                      values=(dataset_name,))

                    return False

                os.makedirs(dataset_local_path)

                # Download from dataset_download_urls into dataset_local_path.
                try:
                    success = self._download_from_presigned_url(
                                        dataset_local_path,
                                        dataset_download_urls)

                    if not success:
                        # If we cannot download, nothing more we can do but
                        # delete the entry from db and exit.
                        shutil.rmtree(dataset_local_path, ignore_errors=True)
                        delete_from_table(DATASET_DELETE_COMMAND,
                                          values=(dataset_name,))
                        return False

                    # Unzip the dataset file.
                    self._download_unzip_in_dir(dataset_local_path)

                    # We are all set. Update the db so that the dataset is
                    # now ready to use.
                    success, _ = update_table_sync(
                        DATASET_SET_READY_LOCK_COMMAND,
                        DATASET_SET_READY_COMMAND,
                        (dataset_name,))

                    if success:
                        self.worker_logger.log_info(
                            "download_dataset",
                            "{} download successful! local path: {}".format(
                                dataset_name,
                                dataset_local_path))

                        return True

                    else:
                        self.worker_logger.log_error(
                            "download_dataset",
                            "{} failed to update dataset entry".format(
                                dataset_name))

                        raise RuntimeError("Failed to set dataset_ready")

                except Exception as e:
                    self.worker_logger.log_error(
                        "download_dataset",
                        "failed to download dataset {} from {}: {}!".format(
                            dataset_name,
                            None,
                            str(e)))

                    traceback.print_exc()

                    # If we fail to download the dataset, it is fatal. Clean up
                    # the db and dataset local directory.
                    shutil.rmtree(dataset_local_path, ignore_errors=True)
                    delete_from_table(DATASET_DELETE_COMMAND,
                                      values=(dataset_name,))

                    return False

        if wait_for_dataset_ready:
            refcount_added = False
            # Wait for a maximum of 10 minutes.
            wait_count = 60
            while wait_count > 0:
                # If we are waiting for the dataset to be downloaded by some other
                # worker, first try to take a reference on the dataset.
                success, output = query_from_table(DATASET_QUERY_BY_DATASET_NAME_COMMAND,
                                                   conditions=(dataset_name,))

                if not success:
                    self.worker_logger.log_error(
                        "download_dataset",
                        "failed to execute query for {} from dataset table!".format(
                            dataset_name))

                    return False

                if not output:
                    # This should not happen. The entry representing this
                    # dataset should have been inserted into the datasets table.
                    self.worker_logger.log_error(
                        "download_dataset",
                        "failed to find entry for {} from dataset table!".format(
                            dataset_name))

                    return False

                if len(output) != 1:
                    self.worker_logger.log_error(
                        "download_dataset",
                        "malformed datasets table entry detected: {}".format(output))

                    return False

                dataset_ready = int(output[0][3])
                # Attempt to take a refcount for the dataset.
                if not refcount_added:
                    success, _ = update_table_sync(
                        DATASET_TAKE_REFERENCE_COUNT_LOCK_COMMAND,
                        DATASET_TAKE_REFERENCE_COUNT_COMMAND,
                        (dataset_name,))

                    if not success:
                        # If the update failed. Do not attempt further.
                        self.worker_logger.log_error(
                            "download_dataset",
                            "unable to add refcount for {}.".format(
                                dataset_name))

                        return False

                    else:
                        self.worker_logger.log_info(
                            "download_dataset",
                            "add refcount for {}. wait_count: {}".format(
                                dataset_name,
                                wait_count))

                        refcount_added = True

                # If the refcount has been added, check if the dataset is
                # ready for use.
                if dataset_ready != 0:
                    self.worker_logger.log_info(
                        "download_dataset",
                        "dataset {} is ready. location: {}".format(
                            dataset_name,
                            dataset_local_path))

                    dataset_downloaded = True
                    break

                else:
                    self.worker_logger.log_info(
                        "download_dataset",
                        "dataset {} is still downloading. wait_count: {}".format(
                            dataset_name,
                            wait_count))

                wait_count -= 1
                sleep(10)
                continue

        return dataset_downloaded

    def _unreference_dataset(self):
        # Only worker needs to use datasets.
        if self.task.task_role != "worker":
            return

        dataset_name = self.task.dataset_name
        if dataset_name is None:
            self.worker_logger.log_error(
                "unreference_dataset",
                "get empty dataset name!")

            return

        success, delete_local = delete_dataset_sync(dataset_name)
        if not success:
            self.worker_logger.log_error(
                "unreference_dataset",
                "db error for unreference the dataset: {}!".format(dataset_name))

        elif delete_local:
            if self.task.dataset_local_path is None:
                self.worker_logger.log_error(
                    "unreference_dataset",
                    "dataset: {} does not locate on disk!".format(dataset_name))
            elif not isdir(self.task.dataset_local_path):
                self.worker_logger.log_error(
                    "unreference_dataset",
                    "dataset: {} local path: {} invalid!".format(
                        dataset_name,
                        self.task.dataset_local_path))
            else:
                self.worker_logger.log_info(
                    "unreference_dataset",
                    "dataset: {} local path: {} will be removed!!".format(
                        dataset_name,
                        self.task.dataset_local_path))

                shutil.rmtree(self.task.dataset_local_path, ignore_errors=True)

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                self.task_uuid: <str>
                self.task: <TrainingTask>

            Produce:
                user environment is installed to /workdir/VENV/
                output folder is created at /workdir/OUTPUT_DIR_NAME/
                log folder is created at /workdir/LOG_DIR_NAME/

        @returns
            success
            - success: <bool> Whether successfully prepared for run.

    '''

    def pre_run(self, in_container: bool = True):
        # Make a output_dir
        os.mkdir(self._get_output_dir_location())
        # Make a log_dir
        os.mkdir(self._get_log_dir_location())

        # Note that even if there is not requirements.txt, a VENV will be created.
        requirements_file = join(self._get_code_dir_location(),
                                 REQUIREMENTS_TXT)

        if exists(requirements_file):
            self.worker_logger.log_info(
                "pre_run",
                "requirements_file at {} with size = {} bytes".format(
                    requirements_file,
                    getsize(requirements_file)))
        else:
            self.worker_logger.log_info(
                "pre_run",
                "requirements_file does not exist".format(
                    requirements_file))

        if not in_container:
            # If the worker is configured to run bare metal, directly install
            # the requirements to /workdir/VENV/.
            success = self._install_user_requirements_direct(requirements_file)
        else:
            success = self._install_user_requirements_container(requirements_file)

        return success

    def _install_user_requirements_direct(self, requirements_file):
        # Use the current python in the PATH for creating the virtualenv.
        p = subprocess.Popen(["python",
                              "-m",
                              VENV,
                              self._get_venv_location(),
                              "--system-site-packages"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        while p.poll() is None:
            line = p.stdout.readline().decode('utf-8')
            if line and line != "":
                self.worker_logger.log_info("pre_run::venv", line.rstrip('\n'))

        p.wait()

        # requirements.txt is expected to be put at the top level of the user's
        # code directory. Do not bother going further if this file is not found,
        # or if the size is 0.

        if not exists(requirements_file):
            return True

        if getsize(requirements_file) == 0:
            return True

        if os_platform == WIN:
            python_path = join(self._get_venv_location(), "Scripts", "python")
        else:
            python_path = join(self._get_venv_location(), "bin", "python")

        # Install the user's requirements
        p = subprocess.Popen([python_path,
                              "-m",
                              "pip",
                              "install",
                              "-r",
                              requirements_file],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        while p.poll() is None:
            line = p.stdout.readline().decode('utf-8')
            if line and line != "":
                self.worker_logger.log_info("pre_run::req", line.rstrip('\n'))

        p.wait()
        return True

    def _install_user_requirements_container(self, requirements_file_host):
        requirements_file_container = join(self._get_container_code_dir_location(),
                                           REQUIREMENTS_TXT)

        # add pyyaml to requirement as default
        with open(requirements_file_container, "a") as f:
            f.write("pyyaml")

        # Note that after venv is created in the container, it will be at
        # /runtime/venv. Therefore, the python path should be
        # /runtime/venv/bin/python.
        venv_python_path = join(CONTAINER_WORK_DIR, VENV, "bin", "python")

        # Mount the entire workdir into /runtime, and create the virtual
        # env inside /runtime. Note that as code has already been downloaded,
        # from container's perspective, the structure will be:
        # /runtime <= CWD
        #   /code
        #       requirements.txt
        # This way, virtual env folder will be put under /runtime/venv from
        # container's perspective and under self.workdir/venv from host's
        # perspective.

        venv_command = "{} --system-site-packages {}".format("virtualenv", VENV)
        mount_command = {self.workdir: {'bind': CONTAINER_WORK_DIR, 'mode': 'rw'}}
        self.worker_logger.log_info(
            "pre_run::req",
            "mount command: {}".format(mount_command))
        docker_client = docker.from_env()
        c = docker_client.containers.run(self._get_container_image(),
                                         entrypoint=venv_command,
                                         volumes=mount_command,
                                         read_only=True,
                                         user=os.getuid(),
                                         detach=True)

        c.wait()
        output = c.logs().decode().split('\n')
        for line in output:
            self.worker_logger.log_info("pre_run::req", line.rstrip('\n'))

        if exists(requirements_file_host) and getsize(requirements_file_host) != 0:
            command = "{} -m pip --disable-pip-version-check --no-cache-dir install -r {} ".format(
                venv_python_path,
                requirements_file_container)

            c = docker_client.containers.run(self._get_container_image(),
                                             entrypoint=command,
                                             volumes=mount_command,
                                             read_only=True,
                                             user=os.getuid(),
                                             detach=True)

            c.wait()
            output = c.logs().decode().split('\n')
            for line in output:
                self.worker_logger.log_info("pre_run::req", line.rstrip('\n'))

        return True

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                self.task_uuid: <str>
                self.task: <TrainingTask>
                code is placed at <WORKER_CWD>/workdir/CODE_DIR_NAME/
                dataset is downloaded at self.task.dataset_local_path
                virtualenv is placed at <WORKER_CWD>/VENV/
                output folder is created at /workdir/OUTPUT_DIR_NAME/
                log folder is created at /workdir/LOG_DIR_NAME/

                When running in container:
                    - <WORKER_CWD> = '/runtime'
                    - dataset will be mounted at '/data'
                    - The file layout looks like:
                        /data  <= self.task.dataset_local_path folder mounted as '/data' [Read-Only]
                            user_data.json
                        /runtime
                            /venv <= 'workdir/VENV' folder mounted as '/runtime/venv' [Read-Write]
                                /bin
                                    Python
                                /lib
                                    <user_packages>
                            /code <= 'workdir/code' folder mounted as '/runtime/code' [Read-Write] <= CWD
                                user_code.py
                                main.py
                            worker_run.py
                        /output <= 'workdir/output' folder mounted as '/output' [Read-Write]
                            user_output.txt

                When running on bare metal:
                    - <WORDER_CWD> = self.workdir
                    - dataset will be placed at self.task.dataset_local_path
                    - The file layout looks like:
                        /self.task.dataset_local_path
                            user_data.json
                        /workdir
                            /venv
                                /bin
                                    Python
                                /lib
                                    <user_packages>
                            /code <= CWD
                                user_code.py
                                main.py
                            /output
                                user_output.txt

            Produce:
                self.task_context: <TaskContext> will contain the task context.

        @returns
            None - After passing pre_run stage, always go to post_run stage.

    '''

    def run(self, in_container: bool = True, container_config: Dict[str, Any] = None):
        self.worker_logger.log_info(
            "run",
            "{} task: {}".format(self.task.task_role, self._get_current_task_uuid()))

        # Prepare environment variables.
        env = {
            WORKER_RUN_ENV_TASK_UUID: str(self._get_current_task_uuid()),
            WORKER_RUN_ENV_TASK_INDEX: str(self.task.task_index),
            WORKER_RUN_ENV_TASK_CLUSTER_SPEC: json.dumps(self.task.cluster_spec),
            WORKER_RUN_ENV_WORKER_TYPE: str(self.worker_type),
            WORKER_RUN_ENV_WORKER_RESOURCE_ID: str(self.resource_id),
            WORKER_RUN_ENV_TASK_ROLE: str(self.task.task_role)
        }

        if not in_container:
            if os_platform == WIN:
                python_path = join(self._get_venv_location(), "Scripts", "python")
            else:
                python_path = join(self._get_venv_location(), "bin", "python")

            # For direct run, dataset folder is just the path to the dataset
            # on the root.
            env[WORKER_RUN_ENV_DATASET_DIR] = str(self.task.dataset_local_path)
            # Code folder is self._get_code_dir_location
            env[WORKER_RUN_ENV_CODE_DIR] = str(self._get_code_dir_location())
            # Output folder is self._get_output_dir_location
            env[WORKER_RUN_ENV_OUTPUT_DIR] = str(self._get_output_dir_location())
            # Log folder is self._get_log_dir_location
            env[WORKER_RUN_ENV_LOG_DIR] = str(self._get_log_dir_location())
            exec_process = self._execute_direct(python_path, env)
            task_context = TaskContext(self.worker_logger,
                                       self._get_log_dir_location(),
                                       exec_process=exec_process)
        else:
            venv_python_path = join(CONTAINER_WORK_DIR, VENV, "bin", "python")
            # For container run, dataset folder is mounted to
            # self._get_container_dataset_path.
            env[WORKER_RUN_ENV_DATASET_DIR] = str(self._get_container_dataset_path())
            # Code folder is self._get_container_code_dir_location
            env[WORKER_RUN_ENV_CODE_DIR] = str(self._get_container_code_dir_location())
            # Output folder is self._get_container_output_dir_location
            env[WORKER_RUN_ENV_OUTPUT_DIR] = str(self._get_container_output_dir_location())
            # Log folder is self._get_container_log_dir_location
            env[WORKER_RUN_ENV_LOG_DIR] = str(self._get_container_log_dir_location())
            exec_container = self._execute_container(venv_python_path, env, container_config)
            task_context = TaskContext(self.worker_logger,
                                       self._get_log_dir_location(),
                                       exec_container=exec_container)

        self.task_context = task_context
        self._start_streaming_log()

        return

    def _start_streaming_log(self):
        self.task_context.user_log_stream = UserLogStream(self.task_context,
                                                          self._get_current_job_uuid(),
                                                          self._get_current_task_uuid(),
                                                          self.master_endpoint,
                                                          self.auth_token)

        log_file = self._get_user_log_file()
        log_process = Process(target=self.task_context.user_log_stream.stream_log,
                              args=("user", log_file))

        log_process.start()
        self.task_context.log_process = log_process

    def _execute_direct(self, python_path, env):
        # For direct execution, CWD is self.workdir.
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        worker_run_path = join(dirname(cur_dir_path), "worker_container", "worker_run.py")
        exec_process = subprocess.Popen([python_path, worker_run_path],
                                        cwd=self._get_code_dir_location(),
                                        env=env,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)

        return exec_process

    def _execute_container(self, venv_python_path, env, container_config):
        # worker_run.py is directly under /runtime.
        worker_run_path = "{}/{}".format(CONTAINER_WORK_DIR, "worker_run.py")

        # Build a mount mapping.
        mount_command = {
            self._get_code_dir_location(): {'bind': self._get_container_code_dir_location(), 'mode': 'rw'},
            self._get_output_dir_location(): {'bind': self._get_container_output_dir_location(), 'mode': 'rw'},
            self._get_log_dir_location(): {'bind': self._get_container_log_dir_location(), 'mode': 'rw'},
            self._get_venv_location(): {'bind': self._get_container_venv_location(), 'mode': 'rw'},
            self.task.dataset_local_path: {'bind': self._get_container_dataset_path(), 'mode': 'ro'},
        }

        # Build environments.
        env_command = []
        for env_name in env.keys():
            cmd = ["{}={}".format(env_name, env[env_name])]
            env_command += cmd

        # Build runtime command.
        runtime_command = "nvidia"

        # Build run command.
        command = "{} {}".format(venv_python_path, worker_run_path)

        # Also take in rest of the container configurations.
        container_config = copy.deepcopy(container_config)
        container_config["entrypoint"] = command
        container_config["volumes"] = mount_command
        container_config["detach"] = True
        container_config["user"] = os.getuid()
        container_config["network_disabled"] = True
        container_config["environment"] = env_command
        container_config["runtime"] = runtime_command
        container_config["working_dir"] = self._get_container_code_dir_location()
        docker_client = docker.from_env()
        exec_container = docker_client.containers.run(self._get_container_image(),
                                                      **container_config)

        return exec_container

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                self.task_context: <TaskContext>
                self.task: <TrainingTask>

            Produce:
                None

            This routine will keep running until the user's code finishes, or
            server askes us to stop.

        @returns
            None - After the run stage, always go to post_run stage.

    '''

    def signal(self, simulate_keep_alive_response: Dict[str, Any] = None, is_signal_finish: bool = False):
        already_terminated = False
        alive = False
        graceful = False
        request_body = {}
        while True:
            if not already_terminated:
                alive, graceful = self.task_context.monitor()

            if alive and graceful:
                self.worker_logger.log_info(
                    "signal",
                    "worker is still running on task {}".format(
                        self._get_current_task_uuid()))

                request_body = {'task_uuid': self._get_current_task_uuid(),
                                'action': 'progress'}

                success, \
                status_code, \
                response_body, \
                error_message = request_server(
                    self.master_endpoint + "/api/v1/worker/task/",
                    'post',
                    **{"data": request_body,
                       "auth": self.auth_token})

                # if there is simulate_keep_alive_response
                # update corresponding values in the actual response
                if simulate_keep_alive_response is not None:
                    request_body.update(simulate_keep_alive_response)
                    # Set the status to success in simulated signal.
                    success = True
                    status_code = 200

                if not success:
                    self.worker_logger.log_error("signal", error_message)
                    # If the server has returned an unexpected response, there
                    # is really nothing can be done at the worker side other
                    # than signal kill the task process. Server will take care
                    # of the clean up.
                    self.worker_logger.log_info("signal", "worker status: stop")
                    self.task_context.terminate()
                    return

                if status_code == 200:
                    status = response_body.get("result", None)
                    create_tensorboard = response_body.get("create_tensorboard", None)
                    if status == "continue":
                        self.worker_logger.log_info(
                            "signal",
                            "worker status: continue")

                        if create_tensorboard:
                            self._create_tensorboard()

                        sleep(int(self.task.keep_alive_interval))
                        continue
                    else:
                        # Note that the server tells the work to stop, the worker
                        # does not need to signal finish.
                        if status != "stop":
                            self.worker_logger.log_warning(
                                "signal",
                                "unexpected worker status from server: {}".format(
                                    status))
                        else:
                            # Master does ask us to stop. Mark the task as finished
                            # as well as we don't need to report to master.
                            self._set_current_task_finished()

                        self.worker_logger.log_info(
                            "signal",
                            "terminate task {}".format(self._get_current_task_uuid()))

                        self.task_context.terminate()

                        # If server asks us to stop, it will pass along a
                        # PreSigned URL for uploading the output. Capture that.
                        self._get_output_upload_urls(response_body)
                        return
                elif status_code < 500:
                    self.worker_logger.log_warning(
                        "signal",
                        "unexpected response status: {}, error: {}".format(
                            status_code,
                            response_body.get("error", None)))

                    self.worker_logger.log_info(
                        "signal",
                        "terminate task {}".format(self._get_current_task_uuid()))

                    self.task_context.terminate()
                    return
                else:
                    # If server side has a problem, there is nothing more can
                    # be done at the client side. Abort the current job.
                    self.worker_logger.log_warning(
                        "signal",
                        "unexpected server side error status: {}".format(
                            status_code))

                    if self.task_context.can_retry():
                        self.worker_logger.log_info(
                            "signal",
                            "server side unexpected error, retry... (chance left: {})"
                                .format(self.task_context.retry_count))

                        sleep(int(self.task.keep_alive_interval))
                        continue
                    else:
                        self.worker_logger.log_info(
                            "signal",
                            "terminate task {}".format(self._get_current_task_uuid()))

                        self.task_context.terminate()
                        return
            else:
                # If the exec process has terminated already, check the output
                # queue to see if there is an item indicates that the task is
                # finished.
                already_terminated = True
                request_body = {}
                task_state = None
                if graceful:
                    self.worker_logger.log_info(
                        "signal",
                        "task {} finished".format(self._get_current_task_uuid()))

                    # If the worker needs to signal finish, let the server know
                    # the task has gracefuly finished. Note that there is no
                    # need to check the return status after this call.
                    if self.task.signal_finish:
                        task_state = 'finished'

                else:
                    self.worker_logger.log_warning(
                        "signal",
                        "task {} unexpectedly stopped".format(
                            self._get_current_task_uuid()))

                    # Let the server know the task has failed as the exec
                    # process unexpectedly terminated. Note that there is no
                    # need to check the return status after this call.
                    task_state = 'failed'

                success = True
                status_code = 0
                if not graceful or self.task.signal_finish:
                    if is_signal_finish:
                        success = True
                        status_code = 200
                    else:
                        success, \
                        status_code = self._report_server_task_state(task_state)

                self.task_context.terminate()
                if success and status_code >= 500:
                    # If server side has an error, retry.
                    if self.task_context.can_retry():
                        self.worker_logger.log_info(
                            "signal",
                            "server side unexpected error, retry... (chance left: {})"
                                .format(self.task_context.retry_count))

                        sleep(int(self.task.keep_alive_interval))
                        continue
                    else:
                        self.worker_logger.log_error(
                            "signal",
                            "server side unexpected error for too many times when siganl finish!")

                elif success and status_code < 300:
                    self.worker_logger.log_info(
                        "signal",
                        "successfully reported task {} finish to server!"
                            .format(self._get_current_task_uuid()))

                    # Mark the task as finished ONLY WHEN we successfully report
                    # that the task is finished to server.
                    self._set_current_task_finished()

                return

    def _report_server_task_state(self, task_state):
        if self._get_current_task_uuid() is None:
            self.worker_logger.log_error(
                "report_task_state",
                "fatal error! task_uuid is None!")

            return False, 500

        request_body = {'task_uuid': self._get_current_task_uuid(),
                        'action': task_state}

        success, status_code, response_body, _ = request_server(
            self.master_endpoint + "/api/v1/worker/task/",
            'post',
            **{"data": request_body,
               "auth": self.auth_token})

        if success and \
           response_body is not None:

            # If we tell server that we stopped, server will pass back a
            # PreSigned URL for uploading the output. Capture that.
            self._get_output_upload_urls(response_body)

        return success, status_code

    def _create_tensorboard(self):
        # Find an empty port that worker can use to create tensorboard
        # but there is a bug in tensorboard that cannot log event using port
        # other than 6006
        port = 6006

        # Start tensorboard
        self.task.tensorboard_process = \
            subprocess.Popen(["tensorboard", "--logdir={}".format(
                join(self.workdir, OUTPUT_DIR_NAME))])

        # Report tensorboard api back to master server
        request_body = {'tensorboard_created': 1}
        success, _, response_body, error_message = request_server(
            self.master_endpoint + "/api/v1/worker/task/{}/".format(
                self._get_current_task_uuid()),
            'put',
            **{"data": request_body,
               "auth": self.auth_token})
        if success:
            self.worker_logger.log_info(
                "tensorboard",
                "successfully started tensorboard at {}".format(
                    response_body.get("tensorboard_url", None)))
        else:
            self.worker_logger.log_warning(
                "tensorboard",
                "failed to start tensorboard with error: {}".format(
                    error_message))

        return

    def _get_output_upload_urls(self, response_body):
        if self.task_context is None:
            self.worker_logger.log_warning(
                "output_upload",
                "missing 'task_context'.")

            return

        self.task_context.output_upload_urls = None
        task_data = response_body.get("task_data", None)
        if task_data is None:
            self.worker_logger.log_warning(
                "output_upload",
                "server malformed response: missing 'task_data'.")

            return

        upload_urls = task_data.get("upload_urls", None)
        if upload_urls is None:
            self.worker_logger.log_warning(
                "output_upload",
                "server malformed response: missing 'upload_urls' inside 'task_data'.")

            return

        output_upload_urls = upload_urls.get(JOB_CONTENT_TYPE_OUTPUT, None)
        if output_upload_urls is None:
            self.worker_logger.log_warning(
                "output_upload",
                "server malformed response: missing '{}' inside 'task_data[upload_urls]'.".format(
                    JOB_CONTENT_TYPE_OUTPUT))

            return

        expected_fileds = ['url', 'fields']
        for expected_filed in expected_fileds:
            if expected_filed not in output_upload_urls:
                self.worker_logger.log_warning(
                    "output_upload",
                    "server malformed response: missing '{}' inside 'task_data[upload_urls][{}]'.".format(
                        expected_filed,
                        JOB_CONTENT_TYPE_OUTPUT))

                return

        self.worker_logger.log_info(
            "output_upload",
            "server responsed upload urls: {}.".format(output_upload_urls))

        self.task_context.output_upload_urls = output_upload_urls
        return

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                self.task: <TrainingTask>
                user artifact inside /workdir/OUTPUT_DIR_NAME

            Produce:
                Upload the user artifact to S3.
                Upload the user logs to S3.
                Drop the refcount taken on the dataset and garbage collect
                if necessary.

        @returns
            None - post_run always go to cleanup.

    '''

    def post_run(self, simulate_need_upload_output: bool = False,
                 simulate_need_upload_log: bool = False,
                 local_output_folder: str = None):
        need_upload_output = simulate_need_upload_output \
            if simulate_need_upload_output is not None else False
        need_upload_log = simulate_need_upload_log \
            if simulate_need_upload_log is not None else False

        # Check if there is anything need to upload.
        for item in os.listdir(self._get_output_dir_location()):
            need_upload_output = True
            break

        if isfile(self._get_user_log_file()) and \
           getsize(self._get_user_log_file()) != 0:

            need_upload_log = True

        if need_upload_output or need_upload_log:
            self.worker_logger.log_info(
                "post_run",
                "task {} has artifacts need upload."
                    .format(self._get_current_task_uuid()))

            # First check if there is a local output folder. If not, ask server
            # for really uploading.
            if local_output_folder is not None:
                if need_upload_output:
                    shutil.copytree(self._get_output_dir_location(),
                                    join(local_output_folder, OUTPUT_DIR_NAME))

                if need_upload_log:
                    shutil.copyfile(self._get_user_log_file(),
                                    join(local_output_folder,
                                         self._get_user_log_file_name()))

            else:
                output_upload_urls = self.task_context.output_upload_urls
                if output_upload_urls is None:
                    self.worker_logger.log_error(
                        "post_run",
                        "do not have presigned url for uploading!")
                else:
                    if need_upload_output:
                        self._upload_to_presigned_url(
                                self._get_output_dir_location(),
                                self._get_upload_output_tar_location(),
                                self._get_upload_output_tar_file_name(),
                                output_upload_urls)

                    if need_upload_log:
                        self._upload_to_presigned_url(
                                self._get_log_dir_location(),
                                self._get_upload_log_tar_location(),
                                self._get_upload_log_tar_file_name(),
                                output_upload_urls)

        else:
            self.worker_logger.log_info(
                "post_run",
                "task {}: no training artifacts found".format(
                    self._get_current_task_uuid()))

        # try to clean up work dir after run
        if self.task.tensorboard_process is not None:
            try:
                self.tensorboard_process.kill()
            except Exception as e:
                self.worker_logger.log_error(
                    "post_run",
                    "failed to terminate tensorboard: {}".format(str(e)))

                traceback.print_exc()

        # Finally, drop the reference count on the dataset.
        self._unreference_dataset()
        return

    def _upload_to_presigned_url(self,
                                 upload_from,
                                 tar_location,
                                 upload_name,
                                 upload_urls):

        make_tarfile(tar_location, upload_from)
        # Sanity check that tar file exists.
        if not isfile(tar_location):
            self.worker_logger.log_warning(
                "upload",
                "failed to tar {} at {}".format(upload_from, tar_location))

            return False

        with open(tar_location,'rb') as fd:
            files = {'file': (upload_name, fd)}
            response = requests.post(upload_urls["url"],
                                     data=upload_urls["fields"],
                                     files=files)
            if not response.ok:
                self.worker_logger.log_warning(
                    "upload",
                    "failed to upload tar {} to {}".format(
                        tar_location,
                        upload_urls["url"]))

                return False

        return True

    # --------------------------------------------------------------------------

    '''

        @abstract

            Expect:
                None

            Produce:
                Anything under self.workdir is cleared.
                self.task set to None.
                self.task_uuid set to None.

        @returns
            success:
                - success <bool>: Whether successfully finished this stage.

    '''

    def task_cleanup(self):
        # First clean up the workdir.
        self._cleanup_workdir()

        # If there is a task uuid, this means the worker has polled a task.
        # If the task is *not* marked as finished, this means the worker
        # encountered some fatal error in the handling and **has not reported
        # to master that it cannot handle the task**.  In this case, we must
        # attempt to report failure to master.
        success = True
        if self._get_current_task_uuid() is not None and \
                not self._get_current_task_finished():

            self.worker_logger.log_warning(
                "cleanup",
                "task: {} is not marked as finished, attempt to report failure to master"
                    .format(self._get_current_task_uuid()))

            try:
                # The task must be reported as failed if we reach here and
                # have not marked the task has finished.
                success, status_code = self._report_server_task_state('failed')
                if not success or status_code >= 300:
                    self.worker_logger.log_error(
                        "cleanup",
                        "task: {} failed to report to master: success: {} status: {}"
                            .format(self._get_current_task_uuid(),
                                    success,
                                    status_code))

                    success = False
            except Exception as e:
                self.worker_logger.log_error(
                    "cleanup",
                    "task: {} exception when report to master: {}"
                        .format(self._get_current_task_uuid(),
                                str(e)))

                traceback.print_exc()
                success = False

        elif self._get_current_task_uuid() is None:
            self.worker_logger.log_warning(
                "cleanup",
                "no task is present for this worker...")

        else:
            self.worker_logger.log_info(
                "cleanup",
                "task: {} completed!".format(
                    self._get_current_task_uuid()))

        self.task = None
        self.task_uuid = None
        return success

    # --------------------------------------------------------------------------

    def _get_code_dir_location(self):
        return join(self.workdir, CODE_DIR_NAME)

    def _get_output_dir_location(self):
        return join(self.workdir, OUTPUT_DIR_NAME)

    def _get_log_dir_location(self):
        return join(self.workdir, LOG_DIR_NAME)

    def _get_dataset_local_path(self, dataset_name):
        return join(self.toplevel_datadir, dataset_name)

    def _get_upload_log_tar_file_name(self):
        return "log_{}{}".format(self.task_uuid[:6], EXTENSION_TAR_GZ)

    def _get_upload_log_tar_location(self):
        return join(self.workdir,
                    self._get_upload_log_tar_file_name())

    def _get_upload_output_tar_file_name(self):
        return "output_{}{}".format(self.task_uuid[:6], EXTENSION_TAR_GZ)

    def _get_upload_output_tar_location(self):
        return join(self.workdir,
                    self._get_upload_output_tar_file_name())

    def _get_venv_location(self):
        return join(self.workdir, VENV)

    def _get_container_code_dir_location(self):
        return CONTAINER_CODE_DIR_LOCATION

    def _get_container_output_dir_location(self):
        return CONTAINER_OUTPUT_DIR_LOCATION

    def _get_container_log_dir_location(self):
        return CONTAINER_LOG_DIR_LOCATION

    def _get_container_dataset_path(self):
        return CONTAINER_DATASET_DIR_LOCATION

    def _get_container_venv_location(self):
        return CONTAINER_VENV_LOCATION

    def _get_container_image(self):
        if self.task.job_type == JOB_TYPE_TENSORFLOW:
            return CONTAINER_TENSORFLOW
        else:
            return CONTAINER_PYTORCH

    def _get_user_log_file_name(self):
        return "{}.log".format(self._get_current_task_uuid())

    def _get_user_log_file(self):
        return join(self._get_log_dir_location(),
                    self._get_user_log_file_name())

    def _cleanup_workdir(self):
        delete_all_from_dir(self.workdir)
        return

    def _get_current_task_uuid(self):
        return self.task_uuid

    def _get_current_job_uuid(self):
        if self.task is None:
            return None
        return self.task.job_uuid

    def _get_current_task_finished(self):
        if self.task is None:
            return False

        return self.task.finished

    def _set_current_task_finished(self):
        if self.task:
            self.task.finished = True
        return
