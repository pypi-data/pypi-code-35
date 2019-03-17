import shutil
from time import sleep

from clint.textui import validators

from dccli.error_codes import *
from dccli.git_helper import *
from dccli.user import get_login_token
from dccli.utils import *


class Download(BaseCase):
    welcome = "Download Job Output"

    def add_arguments(self):
        self.parser.add_argument(
            '--dest',
            type=str,
            default=None,
            help="Destination folder to save the outputs")

        self.parser.add_argument(
            '--job_uuid',
            type=str,
            default=None,
            help="Your job uuid shown when you submit a training job")

    def execute(self, FLAGS):
        auth = get_login_token()
        if auth is None:
            console_out_error("Error: You need to login first")
            return USER_NEED_LOGIN

        job_uuid = FLAGS.job_uuid
        if job_uuid is None:
            job_uuid = self.select_a_job(
                include_conditions={"output_downloaded": False})

        if job_uuid is None:
            console_out_warn("No job specified")
            return USER_INPUT_ERROR

        download_to = FLAGS.dest
        if download_to is not None and isfile(download_to):
            console_out_error("Destination is a file")
            return USER_INPUT_ERROR

        if download_to is None or not exists(download_to):
            download_to = prompt.query(
                "Please specify location for download:",
                default=os.getcwd(),
                validators=[validators.PathValidator()])

        return self.download(auth, job_uuid, download_to)

    def download(self, auth, job_uuid, download_to):
        console_out_info("Download For Job {}".format(job_uuid))
        # Only download if the job is finished.
        progress_case = CheckProgress(self.master_endpoint)
        progress_case.check_progress(auth, job_uuid, quiet=True)

        job_config = self.get_job_config(job_uuid)
        if job_config is not None and job_config.get("job_active", False):
            console_out_warn("Download is available only when job finishes")
            return SUCCESS

        server_url = "{}/api/v1/user/download/{}/".format(
            self.master_endpoint, job_uuid)

        result, response, response_data, error = request_server(
            server_url, "get", auth=auth)

        # Validate server response.
        if not result:
            if response is not None and response.status_code == 401:
                console_out_error("Error: You need to login first")
                return USER_NEED_LOGIN

            console_out_error("Error: {}".format(error))
            return MASTER_FAILURE

        if response_data is None:
            console_out_error(
                "Error: Malformed response from server, no data reponsed")
            return MASTER_FAILURE

        download_urls = response_data.get("download_urls", None)
        if download_urls is None:
            console_out_warn("No downloadable content found")
            return MASTER_FAILURE

        output = download_urls.get(JOB_CONTENT_TYPE_OUTPUT, None)
        if output is None:
            console_out_warn("No downloadable content found")
            return MASTER_FAILURE

        # Start downloading.
        downloadables = []
        total_size = 0
        for (hint, url) in output:
            response = requests.get(url, allow_redirects=True)
            if not response.ok:
                continue
            size = int(response.headers.get('content-length', 0))
            if size != 0:
                total_size += size
            else:
                total_size += 1000
            downloadables += [(response, hint, size)]

        if len(downloadables) == 0:
            self.update_job_config(
                job_uuid,
                job_state=JOB_STATE_NO_OUTPUT,
                output_downloaded=True)

            console_out_warn("No downloadable content found")
            return INTERNAL_ERROR

        with progress.Bar(label="download output ", expected_size=100) as bar:
            download_size = 0
            bar.show(0)
            for (downloadable, hint, size) in downloadables:
                file_loc = join(download_to, hint)
                with open(file_loc, 'wb') as fd:
                    for chunk in downloadable.iter_content(chunk_size=128):
                        if size != 0:
                            download_size += 128
                            current_progress = (download_size * 100) // total_size
                            bar.show(current_progress)
                        fd.write(chunk)

                    if size == 0:
                        download_size += 1000
                        current_progress = (download_size * 100) // total_size
                        bar.show(current_progress)

        self.update_job_config(
            job_uuid,
            job_state=JOB_STATE_OUTPUT_DOWNLOADED,
            output_downloaded=True,
            output_folder=download_to)

        console_out_success("Output downloaded to: {}".format(download_to))
        return SUCCESS


class CheckProgress(BaseCase):
    welcome = "Check Job Progress"

    def add_arguments(self):
        self.parser.add_argument(
            '--job_uuid',
            type=str,
            default=None,
            help="Your job uuid shown when you submit the job")

    def execute(self, FLAGS):
        auth = get_login_token()
        if auth is None:
            console_out_error("Error: You need to login first")
            return USER_NEED_LOGIN

        job_uuid = FLAGS.job_uuid
        if job_uuid is None:
            job_uuid = self.select_a_job()

        if job_uuid is None:
            console_out_warn("No job specified")
            return USER_INPUT_ERROR

        return self.check_progress(auth, job_uuid)

    def check_progress(self, auth, job_uuid, quiet=False):
        job_config = self.get_job_config(job_uuid)
        if job_config is not None and not job_config.get("job_active", True):
            # The job is already terminated. Short cut.
            if not quiet:
                console_out_info("Job {}".format(job_uuid))
                self.display_job_info(job_uuid, job_config)
            return SUCCESS

        server_url = "{}/api/v1/user/progress/{}/".format(
            self.master_endpoint, job_uuid)

        result, response, response_data, error = request_server(
            server_url, "get", auth=auth)

        # Validate server response.
        if not result:
            if response is not None and response.status_code == 401:
                if not quiet:
                    console_out_error("Error: You need to login first")
                return USER_NEED_LOGIN

            console_out_error("Error: {}".format(error))
            return MASTER_FAILURE

        if response_data is None:
            if not quiet:
                console_out_error(
                    "Error: Malformed response from server, no data reponsed")
            return MASTER_FAILURE

        # Extract data from server response.
        job_uuid = response_data.get("job_uuid", None)
        if job_uuid is None:
            if not quiet:
                console_out_error(
                    "Error: Malformed response from server, missing 'job_uuid'")
            return MASTER_FAILURE

        job_state = response_data.get("job_state", None)
        if job_state is None:
            if not quiet:
                console_out_error(
                    "Error: Malformed response from server, missing 'job_state'")
            return MASTER_FAILURE

        job_active = response_data.get("job_active", None)
        if job_state is None:
            if not quiet:
                console_out_error(
                    "Error: Malformed response from server, missing 'job_active'")
            return MASTER_FAILURE

        tensorboard_location = response_data.get("tensorboard_location", None)

        # Everything looks right, keep track the updated information.
        job_config_state_update = {
            "server_state": job_state,
            "job_active": job_active
        }

        if not job_active:
            job_config_state_update["job_state"] = JOB_STATE_SERVER_SIGNALED_STOPPED

        if tensorboard_location is not None:
            job_config_state_update["tensorboard_location"] = tensorboard_location

        job_config = self.update_job_config(job_uuid, **job_config_state_update)
        if not quiet:
            console_out_info("Job {}".format(job_uuid))
            self.display_job_info(job_uuid, job_config)

        return SUCCESS


class StreamLog(BaseCase):
    welcome = "Stream Job Logs"

    def add_arguments(self):
        self.parser.add_argument(
            '--job_uuid',
            type=str,
            default=None,
            help="Your job uuid shown when you submit the job")

    def execute(self, FLAGS):
        auth = get_login_token()
        if auth is None:
            console_out_error("Error: You need to login first")
            return USER_NEED_LOGIN

        job_uuid = FLAGS.job_uuid
        if job_uuid is None:
            job_uuid = self.select_a_job()

        if job_uuid is None:
            console_out_warn("No job specified")
            return USER_INPUT_ERROR

        return self.stream_log(auth, job_uuid)

    def stream_log(self, auth, job_uuid):
        has_all_log = False
        last_timestamp = None
        while not has_all_log:
            time_stamp_argument = ""
            if last_timestamp is not None:
                time_stamp_argument = "&timestamp={}".format(last_timestamp)

            server_url = "{}/api/v1/user/stream/?job_uuid={}{}".format(
                self.master_endpoint,
                job_uuid,
                time_stamp_argument)

            result, response, response_data, error = request_server(
                server_url, "get", auth=auth)

            # Validate server response.
            if not result:
                if response is not None and response.status_code == 401:
                    console_out_error("Error: You need to login first")
                    return USER_NEED_LOGIN

                console_out_error("Error: {}".format(error))
                return MASTER_FAILURE

            if response_data is None:
                console_out_error(
                    "Error: Malformed response from server, no data reponsed")
                return MASTER_FAILURE

            # 200 means that is the last batch of log,
            # 202 means there is more
            status_code = response.status_code
            if status_code == 200:
                has_all_log = True

            logs = json.loads(response_data.get('log', None))
            last_timestamp = response_data.get('last_timestamp', None)
            if logs is not None and len(logs) > 0:
                for log in logs:
                    console_out_log(log.rstrip('\n'))
            sleep(3)

        return SUCCESS


class Submit(BaseCase):
    use_current_directory = False
    welcome = "Submit Job"
    job_uuid = None

    def add_arguments(self):
        self.parser.add_argument(
            '-c',
            action='store_true',
            default=False,
            help="Submit the current directory only (instead of the entire repo)")

    def execute(self, FLAGS):
        self.use_current_directory = FLAGS.c
        auth = get_login_token()
        if auth is None:
            console_out_error("Error: You need to login first")
            return USER_NEED_LOGIN

        config_path = self.get_config_file_path()
        if config_path is None or not exists(config_path):
            console_out_warn(
                "No job config found (Expected: '{}')".format(config_path))
            job_data = self.get_job_data_interactive()
            if job_data is None:
                return USER_INPUT_ERROR
        else:
            try:
                job_data = load_yaml(config_path)
            except:
                console_out_error(
                    "Error: cannot load job config at '{}'".format(config_path))
                return USER_INPUT_ERROR

        return self.submit_job(job_data, auth)

    def get_job_toplevel_dir(self):
        if self.use_current_directory:
            toplevel = os.getcwd()
        else:
            toplevel = get_repo_toplevel_dir()
        return toplevel

    def get_config_file_path(self):
        toplevel = self.get_job_toplevel_dir()
        if toplevel is None:
            return None

        return join(toplevel, CONFIG_FILE_NAME)

    def get_job_data_interactive(self):
        job_type = prompt.query(
            "Please specify job type {}:".format(SUPPORTED_JOB_TYPES))

        if job_type.lower() not in SUPPORTED_JOB_TYPES:
            console_out_error(
                "Error: Unsupported job type '{}'".format(job_type))
            return None

        job_data = {
            "job_type": job_type.lower(),
            "worker_required": 1
        }

        yes = prompt.yn("Use local dataset")
        if yes:
            dataset_path = prompt.query(
                "Please specify local dataset location:", validators=[validators.PathValidator()])
            job_data["dataset_path"] = dataset_path
        else:
            dataset_name = prompt.query(
                "Please specify dataset name:", default="cifar10")
            job_data["dataset_name"] = dataset_name

        return job_data

    def validate_job_param(self, job_data):
        job_type = job_data.get("job_type", None)
        if job_type is None:
            raise ValueError(
                "Error: Malformed job configration, missing 'job_type'")

        dataset_name = job_data.get("dataset_name", None)
        dataset_path = job_data.get("dataset_path", None)
        if dataset_path is not None:
            if not isdir(dataset_path) and not isfile(dataset_path):
                raise ValueError(
                    "Error: Malformed job configration, cannot find dataset path '{}'".format(
                        dataset_path))

        return job_type, dataset_name, dataset_path

    def submit_job(self, job_data, auth):
        try:
            job_type, dataset_name, dataset_path = self.validate_job_param(
                job_data)
        except Exception as e:
            console_out_error(str(e))
            return USER_INPUT_ERROR

        request_body = {
            'parameters': json.dumps(job_data)
        }

        # If the dataset name is supplied, assume this is a known dataset and pass that to server.
        if dataset_name is not None:
            request_body['dataset_name'] = dataset_name

        # Submit the job to server to get PreSigned URLs for uploading the code and datasets.
        server_url = "{}/api/v1/user/{}/job/".format(
            self.master_endpoint,
            JOB_TYPE_TO_API[job_type])

        result, response, response_data, error = request_server(
            server_url, "post", data=request_body, auth=auth)

        # Validate server response.
        if not result:
            if response is not None and response.status_code == 401:
                console_out_error("Error: You need to login first")
                return USER_NEED_LOGIN

            console_out_error("Error: {}".format(error))
            return MASTER_FAILURE

        if response_data is None:
            console_out_error(
                "Error: Malformed response from server, no data reponsed")
            return MASTER_FAILURE

        job_uuid = response_data.get("job_uuid", None)
        if job_uuid is None:
            console_out_error(
                "Error: Malformed response from server, missing 'job_uuid'")
            return MASTER_FAILURE

        # Create a config file for the job locally now that we have a job_uuid.
        self.update_job_config(
            job_uuid,
            job_type=job_type,
            source=self.get_job_toplevel_dir(),
            dataset=dataset_name if dataset_name is not None else dataset_path,
            job_state=JOB_STATE_PENDING_UPLOAD)

        # Stop the job if error occurs.
        stop_case = Stop(self.master_endpoint)
        dataset_known = response_data.get("dataset_known", False)
        upload_urls = response_data.get("upload_urls", None)
        if upload_urls is None:
            console_out_error(
                "Error: Malformed response from server, missing 'upload_urls'")

            stop_case.terminate_job(
                job_uuid, auth, JOB_STATE_SERVER_RESPONSE_UNEXPECTED, quiet=True)
            return MASTER_FAILURE

        # Code must be in the upload url.
        upload_code_url = upload_urls.get(JOB_CONTENT_TYPE_CODE, None)
        if upload_code_url is None:
            console_out_error("Error: Malformed response from server, missing '{}'".format(
                JOB_CONTENT_TYPE_CODE))

            stop_case.terminate_job(
                job_uuid, auth, JOB_STATE_SERVER_RESPONSE_UNEXPECTED, quiet=True)
            return MASTER_FAILURE

        # If dataset is not known, dataset must be in the upload url.
        upload_dataset_url = upload_urls.get(
            JOB_CONTENT_TYPE_DATASET, None)

        # Sanity check, we must have a dataset_path if there is upload_dataset_url.
        if dataset_path is not None and upload_dataset_url is None:
            console_out_error("Error: Server does not allow uploading dataset for current config")
            stop_case.terminate_job(
                job_uuid, auth, JOB_STATE_SERVER_RESPONSE_UNEXPECTED, quiet=True)
            return INTERNAL_ERROR

        # Everything is as expected now. Upload the code (and dataset if needed) to the upload url.
        success = self.upload_job_data(
            job_uuid, upload_code_url, upload_dataset_url, dataset_path)

        if not success:
            stop_case.terminate_job(
                job_uuid, auth, JOB_STATE_CANNOT_UPLOAD, quiet=True)
            return INTERNAL_ERROR

        # Job data uploaded.
        self.update_job_config(
            job_uuid,
            job_state=JOB_STATE_UPLOADED)

        # Signal the server that the job is ready.
        signal_server_url = "{}{}/".format(server_url, job_uuid)
        result, response, _, error = request_server(
            signal_server_url, "put", auth=auth)
        if not result:
            console_out_error(
                "Error: Failed to signal job ready, {}".format(error))

            stop_case.terminate_job(
                job_uuid, auth, JOB_STATE_CANNOT_SIGNAL_JOB_READY, quiet=True)
            return MASTER_FAILURE

        console_out_success("Submit job successfully")
        console_out_log("job type: {}".format(job_type), quote=" >")
        console_out_log("job uuid: {}".format(job_uuid), quote=" >")
        # Update the job state to submitted.
        self.update_job_config(
            job_uuid,
            job_state=JOB_STATE_READY)

        # save job_uuid in Submit case so that test can remove the s3 folder
        self.job_uuid = job_uuid
        return SUCCESS

    def pack_dataset(self, out_folder, dataset_path):
        dataset_tar_location = join(out_folder, DATASET_TAR_GZ)
        make_tarfile(dataset_tar_location, dataset_path)
        return dataset_tar_location

    def upload_job_data(self, job_uuid, upload_code_url, upload_dataset_url, dataset_path):
        code_tar_location = None
        dataset_tar_location = None
        job_tmp_folder = self.get_job_folder(job_uuid)

        try:
            # Make a job folder to ensure there is no collision.
            os.mkdir(job_tmp_folder)
            if not isdir(job_tmp_folder):
                console_out_error("Error: Cannot make a job folder")
                return False

            # Pack the code using git.
            success, out = pack_code_using_git(
                job_tmp_folder, self.get_job_toplevel_dir())
            if not success:
                console_out_error("Error: {}".format(out))
                return False

            # out is the path to the code tar ball.
            code_tar_location = out
            console_out_log("Upload code...")
            with open(code_tar_location, 'rb') as fd:
                files = {'file': (CODE_TAR_GZ, fd)}
                response = requests.post(
                    upload_code_url["url"],
                    data=upload_code_url["fields"],
                    files=files)

                if not response.ok:
                    print("Error: Failed to upload code to {}".format(
                        upload_code_url["url"]))
                    return False

            # If we also need to upload dataset, pack the dataset.
            if upload_dataset_url is not None:
                dataset_tar_location = self.pack_dataset(
                    job_tmp_folder, dataset_path)

                console_out_log("Upload dataset...")
                with open(dataset_tar_location, 'rb') as fd:
                    files = {'file': (DATASET_TAR_GZ, fd)}
                    response = requests.post(
                        upload_dataset_url["url"],
                        data=upload_dataset_url["fields"],
                        files=files)

                    if not response.ok:
                        console_out_error("Error: Failed to upload dataset to {}".format(
                            upload_dataset_url["url"]))
                        return False

            return True
        except:
            console_out_error("Error: Failed to upload job data")
            if DEBUG:
                traceback.print_exc()

            return False

        finally:
            if isdir(job_tmp_folder):
                shutil.rmtree(job_tmp_folder, ignore_errors=True)


class Stop(BaseCase):
    welcome = "Stop Job"

    def add_arguments(self):
        self.parser.add_argument(
            '--job_uuid',
            type=str,
            default=None,
            help="Your job uuid shown when you submit the job")

    def execute(self, FLAGS):
        auth = get_login_token()
        if auth is None:
            console_out_error("Error: You need to login first")
            return USER_NEED_LOGIN

        job_uuid = FLAGS.job_uuid
        if job_uuid is None:
            job_uuid = self.select_a_job()

        if job_uuid is None:
            console_out_warn("No job specified")
            return USER_INPUT_ERROR

        # If the job is already stopped, do not make redundant call.
        job_config = self.get_job_config(job_uuid)
        if job_config is not None and not job_config["job_active"]:
            console_out_success("Job {} already stopped".format(job_uuid))
            self.display_job_info(job_uuid, job_config)
            return SUCCESS

        return self.terminate_job(job_uuid, auth, JOB_STATE_TERMINATED)

    def terminate_job(self, job_uuid, auth, final_local_state, quiet=False):
        server_url = "{}/api/v1/user/progress/".format(self.master_endpoint)
        request_body = {
            'job_uuid': job_uuid,
            'job_update_state': "terminate"
        }

        # Tell the server to stop the job.
        result, response, _, error = request_server(
            server_url, "post", data=request_body, auth=auth)

        if not result:
            if response is not None and response.status_code == 401:
                if not quiet:
                    console_out_error("Error: You need to login first")
                return USER_NEED_LOGIN

            if not quiet:
                console_out_error("Error: {}".format(error))
            return MASTER_FAILURE

        # Mark the job as stopped locally.
        job_config = self.update_job_config(
            job_uuid, job_state=final_local_state, job_active=False)
        if not quiet:
            console_out_success("Job {} stopped".format(job_uuid))
            # Some additional information...
            self.display_job_info(job_uuid, job_config)

        return SUCCESS
