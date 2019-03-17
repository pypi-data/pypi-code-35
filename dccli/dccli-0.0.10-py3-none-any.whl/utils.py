import argparse
import json
import os
import tarfile
import traceback
from datetime import datetime
from os import listdir
from os.path import splitext, basename, join, isfile, isdir, getsize

import requests
import yaml
from clint import resources
from clint.textui import puts, indent, colored, progress, prompt

from dccli.constants import *


def console_out_log(message, level="log", tab=0, quote=''):
    def _puts(level, message):
        if level == "success":
            puts(colored.green(message))
        elif level == "error":
            puts(colored.red(message))
        elif level == "info":
            puts(colored.cyan(message))
        elif level == "warn":
            puts(colored.yellow(message))
        else:
            puts(colored.clean(message))

    # Cannot have quote but no tab.
    if quote != "" and tab == 0:
        tab = 4

    if tab > 0:
        with indent(indent=tab, quote=quote):
            _puts(level, message)
    else:
        _puts(level, message)


def console_out_success(message, tab=0, quote=''):
    console_out_log(message, level="success", tab=tab, quote=quote)


def console_out_error(message, tab=0, quote=''):
    console_out_log(message, level="error", tab=tab, quote=quote)


def console_out_info(message, tab=0, quote=''):
    console_out_log(message, level="info", tab=tab, quote=quote)


def console_out_warn(message, tab=0, quote=''):
    console_out_log(message, level="warn", tab=tab, quote=quote)


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Token ' + self.token
        return r


class BaseCase:
    master_endpoint = None
    parser = argparse.ArgumentParser()
    welcome = None
    splitter = "==========================================="

    def __init__(self, master_endpoint="http://dtf-masterserver-dev.us-west-1.elasticbeanstalk.com"):
        self.master_endpoint = master_endpoint

    def add_arguments(self):
        # add case specific arguments
        pass

    def execute(self, FLAGS):
        # add your specific logic functions
        raise Exception("must be overridden")

    def welcome_message(self):
        if self.welcome is not None:
            front = (len(self.splitter) - len(self.welcome)) // 2
            back = (len(self.splitter) - len(self.welcome)) - front
            console_out_log(self.splitter)
            console_out_log("{}{}{}".format(" "*front, self.welcome, " "*back))
            console_out_log(self.splitter)

    def parse_and_execute(self):
        self.add_arguments()
        FLAGS, _ = self.parser.parse_known_args()
        self.welcome_message()
        self.execute(FLAGS)

    def get_job_folder(self, job_uuid):
        return join(resources.user.path, job_uuid)

    def get_job_config_file_name(self, job_uuid):
        return "{}.ini".format(job_uuid)

    def get_job_config(self, job_uuid):
        config = resources.user.read(
            self.get_job_config_file_name(job_uuid))

        if config is None:
            return None

        try:
            config_parsed = json.loads(config)
        except:
            console_out_warn("Failed to load job config for job {}".format(job_uuid))
            if DEBUG:
                traceback.print_exc()

            return None
        return config_parsed

    def update_job_config(self, job_uuid, **kwargs):
        # Attempt to load the config first
        existing_config = self.get_job_config(job_uuid)
        timenow = datetime.now().strftime(JOB_TIME_FMT)
        if existing_config is None:
            existing_config = {
                "create_at": timenow,
                "last_state_at": timenow,
                "job_active": True,
                "output_downloaded": False
            }

        # Load/update configuration.
        for key in kwargs.keys():
            # These keys are auto updated.
            ignore_keys = ["last_state_at", "terminate_at", "create_at", "update_at"]
            if key in ignore_keys:
                continue

            # Note that the entire job state histroy is kept.
            if key == "job_state":
                # Append the new state at the end of the state history.
                if key in existing_config:
                    state_history = existing_config[key]
                else:
                    state_history = []

                state_history += [(kwargs[key], timenow)]
                existing_config[key] = state_history
                existing_config["last_state_at"] = timenow
            else:
                # Record the time that job is terminated.
                if key == "job_active":
                    still_active = existing_config.get("job_active", True)
                    if not kwargs[key] and still_active:
                        existing_config["terminate_at"] = timenow
                existing_config[key] = kwargs[key]

        existing_config["update_at"] = timenow
        resources.user.write(
            self.get_job_config_file_name(job_uuid),
            json.dumps(existing_config))

        return existing_config

    def get_all_job_configs(self):
        job_configs = {}
        user_folder = resources.user.path
        if isdir(user_folder):
            for item in listdir(user_folder):
                item_path = join(user_folder, item)
                if isfile(item_path):
                    filename, extension = splitext(item)
                    if extension == ".ini":
                        job_config = self.get_job_config(filename)
                        if job_config is not None:
                            job_configs[filename] = job_config
        return job_configs

    def select_a_job(self, include_conditions={"job_active": True}, auto_select_only_one=True):
        all_jobs = self.get_all_job_configs()
        options = []
        index = 1
        for job_uuid in all_jobs.keys():
            skip = False
            # If the job does not match condition, exclude it.
            for condition_key in include_conditions.keys():
                if condition_key not in all_jobs[job_uuid]:
                    continue
                if all_jobs[job_uuid][condition_key] != include_conditions[condition_key]:
                    skip = True
                    break
            if skip:
                continue

            options += [{
                'selector': str(index),
                'prompt': "({}) {}: {}".format(
                    all_jobs[job_uuid]["create_at"],
                    all_jobs[job_uuid].get("job_type", "<data lost>"),
                    job_uuid),
                'return': job_uuid
            }]

            index += 1

        if len(options) == 0:
            return None

        if len(options) == 1 and auto_select_only_one:
            return options[0]['return']

        selected = prompt.options(
            "Please select a job (1-{}):".format(len(options)), options)
        return selected

    def display_job_info(self, job_uuid, job_config):
        job_type = job_config.get("job_type", "<data lost>")
        console_out_log("job type:  {}".format(job_type), quote=" >")

        # Job current state from server.
        server_state = job_config.get("server_state", None)
        tensorboard = job_config.get("tensorboard_location", None)
        if server_state is not None:
            console_out_log("job state: {}".format(server_state), quote=" >")

        # Some additional information...
        create_time = datetime.strptime(job_config["create_at"], JOB_TIME_FMT)
        if job_config["job_active"]:
            timenow = datetime.now()
        else:
            timenow = datetime.strptime(
                job_config["terminate_at"], JOB_TIME_FMT)

        duration = (timenow - create_time).total_seconds()
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = '{:02}:{:02}:{:02}'.format(
            int(hours), int(minutes), int(seconds))
        duration_str = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        console_out_log("duration:  {}".format(duration_str), quote=" >")
        if tensorboard is not None:
            console_out_log("tensorboard: {}".format(
                tensorboard), quote=" >")
        job_state = job_config.get("job_state", None)
        if job_state:
            console_out_log("job local history:", quote=" >")
            for (job_state, time) in job_config["job_state"]:
                console_out_log("[{}] {}".format(time, job_state), tab=8)


def load_yaml(task_path):
    with open(task_path) as f:
        config = None
        filename, file_extension = splitext(basename(task_path))
        if file_extension == ".json":
            config = json.load(f)
        elif file_extension == ".yaml":
            config = yaml.load(f)
        else:
            raise ValueError("{} is not a valid config".format(str(f)))
    return config


def get_size(path):
    total_size = 0
    for item in listdir(path):
        sub_path = join(path, item)
        if isfile(sub_path):
            total_size += getsize(sub_path)
        else:
            total_size += get_size(sub_path)
    return total_size


def make_tarfile(output_filename, source_dir):
    tar_info = {
        "total_size": get_size(source_dir),
        "tar_size": 0
    }

    def _progress_filter(tarinfo):
        total_size = tar_info["total_size"]
        tar_size = tar_info["tar_size"]
        file_size = tarinfo.size
        tar_size += file_size
        current_progress = (tar_size * 100) // total_size
        tar_info["tar_size"] = tar_size
        bar.show(current_progress)
        return tarinfo

    if source_dir is not None:
        if not source_dir.endswith(os.path.sep):
            source_dir = source_dir + os.path.sep
        with progress.Bar(label="zip dataset ", expected_size=100) as bar:
            bar.show(0)
            with tarfile.open(output_filename, "w:gz") as tar:
                tar.add(source_dir, arcname=basename(source_dir), filter=_progress_filter)


def unzip_tarfile(source_tar, target_dir):
    tar = tarfile.open(source_tar, "r:gz")
    tar.extractall(path=target_dir)
    tar.close()


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def request_server(url, verb, **kwargs):
    response = None
    # Allow a 30s timeout for the request.
    try:
        if verb == 'post':
            response = requests.post(url, timeout=30, **kwargs)
        elif verb == 'put':
            response = requests.put(url, timeout=30, **kwargs)
        elif verb == 'get':
            response = requests.get(url, timeout=30, **kwargs)
        else:
            console_out_error("Unknown api '{}'".format(verb))
            return False, None, None, None
    except Exception as e:
        console_out_error("Server is temporarily unavailable...")
        if DEBUG:
            traceback.print_exc()
        return False, None, None, None

    if response is None:
        console_out_error("Server is temporarily unavailable...")
        return False, None, None, None

    response_data = None
    try:
        if response.text is not None:
            response_data = json.loads(response.text)
    except Exception as e:
        console_out_error("Server returned malformed data...")
        if DEBUG:
            traceback.print_exc()
        return False, None, None, None

    error = None
    if not response.ok:
        error = "Unknown error..."
        if response_data is not None:
            error = response_data.get("error", "Unknown error...")
            if type(error) is dict:
                error_string = ""
                for k in error.keys():
                    if error[k] is None:
                        continue
                    error_entry = error[k]
                    if type(error[k]) is list:
                        error_entry = error[k][0]
                    if error_string == "":
                        error_string = error_entry
                    else:
                        error_string += (", " + error_entry)
                error = error_string

    return response.ok, response, response_data, error
