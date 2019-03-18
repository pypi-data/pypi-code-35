import random
import subprocess

import yaml

from common.global_variable import DEFAULT_MASTER_SERVER

###############################################################################

# General config
RUNTIME_MASTER_SERVER = "MASTER_SERVER"
RUNTIME_GPU_UUID_TO_ID = "GPU_UUID_TO_ID"
RUNTIME_CPU_MODE = "CPU_MODE"
RUNTIME_RUN_ONCE = "RUN_ONCE"
RUNTIME_WORKER_RUN_IN_CONTAINER = "WORKER_RUN_IN_CONTAINER"
RUNTIME_CONTAINER_CONFIG = "CONTAINER_CONFIG"

# Stage specific config
WORKER_REGISTER = "REGISTER"
REGISTER_FORCE_REGISTRATION = "FORCE_REGISTRATION"
REGISTER_REGISTRATION_ONLY = "REGISTRATION_ONLY"
REGISTER_FAKE_WORKER_REGISTRATION = "FAKE_WORKER_REGISTRATION"

WORKER_ENROLL = "ENROLL"
ENROLL_FAKE_ENROLL = "FAKE_ENROLL"


WORKER_POLL = "POLL"
POLL_SIMULATE_JOB = "SIMULATE_JOB"
POLL_POLL_SUCCESS_POSSIBILITY = "POLL_SUCCESS_POSSIBILITY"

WORKER_POLL_WAIT = "POLL_WAIT"

WORKER_FETCH = "FETCH"
FETCH_DOWNLOAD_CODE = "DOWNLOAD_CODE"
FETCH_DOWNLOAD_DATASET = "DOWNLOAD_DATASET"

WORKER_PRE_RUN = "PRE_RUN"

WORKER_RUN = "RUN"

WORKER_SIGNAL = "SIGNAL"
SIGNAL_FAKE_SIGNAL = "FAKE_SIGNAL"

WORKER_POST_RUN = "POST_RUN"
POST_RUN_UPLOAD_OUTPUT = "UPLOAD_OUTPUT"
POST_RUN_UPLOAD_LOG = "UPLOAD_LOG"

POST_RUN_COPY_OUTPUT_LOCAL = "COPY_OUTPUT_LOCAL"

WORKER_TASK_CLEANUP = "TASK_CLEANUP"


# Default runtime configuration
DEFAULT_CONTAINER_CONFIG = {
    # Per Nvidia docker, shared memory is default to 1GB.
    "shm_size": "1G"
}

DEFAULT_RUNTIME = {
    RUNTIME_MASTER_SERVER: DEFAULT_MASTER_SERVER,
    RUNTIME_CONTAINER_CONFIG: DEFAULT_CONTAINER_CONFIG
}

###############################################################################

def get_nvidia_gpu_mappings():
    command = ["nvidia-smi", "--query-gpu=index,gpu_uuid", "--format=csv,noheader"]
    try:
        exec_process = subprocess.Popen(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)

        stdout, stderr = exec_process.communicate()
    except Exception as e:
        print("[Error::FATAL] Cannot get nvidia GPU uuid to id mapping: {}".format(str(e)))
        return {}

    if stderr is not None:
        print("[Error::FATAL] Cannot get nvidia-smi output: {}".format(stderr))
        return {}

    if stdout is None:
        print("[Error::FATAL] Cannot get nvidia GPU uuid to id mapping")
        return {}

    mappings = stdout.decode("utf-8").split('\n')
    uuid_to_id = {}
    for mapping in mappings:
        values = mapping.split(',')
        if len(values) != 2:
            continue
        uuid_to_id[values[1].strip()] = values[0].strip()

    return uuid_to_id

class WorkerRuntime:
    keep_alive_count = -1

    def __init__(self, runtime_file=None):
        self.runtime = DEFAULT_RUNTIME
        # Load default runtime if there is no runtime file.
        if runtime_file is not None:
            try:
                with open(runtime_file, "r") as f:
                    self.runtime = yaml.load(f)


                for default in DEFAULT_RUNTIME.keys():
                    if default not in self.runtime:
                        self.runtime[default] = DEFAULT_RUNTIME[default]
            except Exception as e:
                print("[Error::FATAL] Cannot parse runtime file: {}".format(str(e)))
                raise

        # Load the current GPU UUID to ID mapping.
        self.runtime[RUNTIME_GPU_UUID_TO_ID] = get_nvidia_gpu_mappings()
        self._validate_runtime()
        print("[INFO] Runtime configuration:")
        print(self.runtime)

    def _validate_runtime(self):
        # Verify required keys exist.
        expected_keys = [RUNTIME_MASTER_SERVER,
                         RUNTIME_GPU_UUID_TO_ID,
                         RUNTIME_CONTAINER_CONFIG]

        for expected_key in expected_keys:
            if expected_key not in self.runtime:
                raise RuntimeError("[WorkerRuntime] No {} found!".format(expected_key))

        # Verify exclusive keys do not co-exist.
        exclusive_keys_in_stage = {
            WORKER_REGISTER:
                [
                    # Cannot have registration only and fake registration together.
                    [
                        REGISTER_REGISTRATION_ONLY,
                        REGISTER_FAKE_WORKER_REGISTRATION
                    ],

                    # Cannot have force registration and fake registration together.
                    [
                        REGISTER_FORCE_REGISTRATION,
                        REGISTER_FAKE_WORKER_REGISTRATION
                    ]
                ]
        }

        for stage in exclusive_keys_in_stage.keys():
            if stage not in self.runtime:
                continue
            for exclusive_keys in exclusive_keys_in_stage[stage]:
                for exclusive_key in exclusive_keys:
                    for i in range(0, len(exclusive_key)):
                        for j in range(i+1, len(exclusive_key)):
                            key_i = exclusive_key[i]
                            key_j = exclusive_key[j]
                            if key_i in self.runtime[stage] and key_j in self.runtime[stage]:
                                raise RuntimeError(
                                        "[WorkerRuntime] Cannot have both {} and {} in stage {}!".format(
                                            key_i,
                                            key_j,
                                            stage))

        # Verify dependent keys do co-exist.
        dependent_keys_in_stage = {

        }

        for stage in dependent_keys_in_stage.keys():
            if stage not in self.runtime:
                continue
            for dependent_keys in dependent_keys_in_stage[stage]:
                for dependent_key in dependent_keys:
                    for i in range(0, len(dependent_key)):
                        for j in range(i+1, len(dependent_key)):
                            key_i = dependent_key[i]
                            key_j = dependent_key[j]
                            if key_i in self.runtime[stage] and key_j not in self.runtime[stage]:
                                raise RuntimeError(
                                        "[WorkerRuntime] {} requires {} in stage {}!".format(
                                            key_i,
                                            key_j,
                                            stage))
                            elif key_j in self.runtime[stage] and key_i not in self.runtime[stage]:
                                raise RuntimeError(
                                        "[WorkerRuntime] {} requires {} in stage {}!".format(
                                            key_j,
                                            key_i,
                                            stage))

        # Verify inter-stage dependencies do co-exist.
        # Note: Make sure the former entry in the list depends on the latter
        # entry. The first entry in the list is the start of the dependency.
        interstage_dependencies = [
            # If the registration is faked, then enrolled must be faked as well.
            # If the enrollment is faked, then poll also must be faked.
            # If the poll is faked, then signal check must also be faked.
            # At last, post_run must copy output to local disk.
            {
                WORKER_REGISTER: REGISTER_FAKE_WORKER_REGISTRATION,
                WORKER_ENROLL: ENROLL_FAKE_ENROLL,
                WORKER_POST_RUN: POST_RUN_COPY_OUTPUT_LOCAL
            }
        ]

        for interstage_dependency in interstage_dependencies:
            stages = list(interstage_dependency.keys())
            for i in range(0, len(stages)):
                # Stage n is dependent on stage n+1
                stage_i = stages[i]
                config_stage_i = interstage_dependency[stage_i]

                # Skip non-existing configuration
                if stage_i not in self.runtime or \
                   config_stage_i not in self.runtime[stage_i]:

                    continue

                # Find the first existing configuration in the dependency chain.
                # Now make sure the rest of the configurations all exist.
                for j in range(i+1, len(stages)):
                    stage_j = stages[j]
                    config_stage_j = interstage_dependency[stage_j]
                    if stage_j not in self.runtime or \
                       config_stage_j not in self.runtime[stage_j]:

                        raise RuntimeError(
                                "[WorkerRuntime] {}::{} requires {}::{}".format(
                                    stage_i,
                                    config_stage_i,
                                    stage_j,
                                    config_stage_j))

                # Break the loop now. Further checks are duplicates.
                break


    def cpu_mode(self):
        return self.runtime.get(RUNTIME_CPU_MODE, False)

    def master_server(self):
        return self.runtime[RUNTIME_MASTER_SERVER]

    def run_once(self):
        return self.runtime.get(RUNTIME_RUN_ONCE, False)

    def worker_run_in_container(self):
        return self.runtime.get(RUNTIME_WORKER_RUN_IN_CONTAINER, True)

    def container_configuration(self):
        return self.runtime[RUNTIME_CONTAINER_CONFIG]

    def get_fake_registration(self):
        return self.get_stage_configuration(
                            WORKER_REGISTER,
                            REGISTER_FAKE_WORKER_REGISTRATION)

    def force_registration(self):
        return self.get_stage_configuration(
                    WORKER_REGISTER,
                    REGISTER_FORCE_REGISTRATION)

    def registration_only(self):
        return self.get_stage_configuration(
                    WORKER_REGISTER,
                    REGISTER_REGISTRATION_ONLY)

    def get_stage_configuration(self, stage, configuration):
        if stage not in self.runtime:
            return None

        return self.runtime[stage].get(configuration, None)

    def simulate_enroll(self):
        return self.get_stage_configuration(
                    WORKER_ENROLL,
                    ENROLL_FAKE_ENROLL)

    def simulate_signal_keep_alive_response(self):
        if WORKER_SIGNAL not in self.runtime:
            return None

        if SIGNAL_FAKE_SIGNAL not in self.runtime[WORKER_SIGNAL]:
            return None

        sim_signal = self.get_stage_configuration(WORKER_SIGNAL, SIGNAL_FAKE_SIGNAL)
        if "keep_alive" not in sim_signal:
            return None

        if "max_success" not in sim_signal["keep_alive"]:
            return sim_signal["keep_alive"]

        if sim_signal["keep_alive"]["max_success"] == 0:
            return sim_signal["keep_alive"]

        if self.keep_alive_count == -1:
            self.keep_alive_count = \
                sim_signal["keep_alive"]["max_success"]

        if self.keep_alive_count == 0:
            return {"result": "stop"}
        else:
            self.keep_alive_count -= 1
            return sim_signal["keep_alive"]

    def is_simulate_signal_finish(self):
        if WORKER_SIGNAL not in self.runtime:
            return False

        if SIGNAL_FAKE_SIGNAL not in self.runtime[WORKER_SIGNAL]:
            return False

        # If we do not simulate keep_alive, we do not simulate finish.
        sim_signal = self.get_stage_configuration(WORKER_SIGNAL, SIGNAL_FAKE_SIGNAL)
        if "keep_alive" not in sim_signal:
            return False

        self.keep_alive_count = -1

        return True

    def get_local_output_folder(self):
        return self.get_stage_configuration(
                    WORKER_POST_RUN,
                    POST_RUN_COPY_OUTPUT_LOCAL)

    def get_simulated_job(self):
        return self.get_stage_configuration(
                    WORKER_POLL,
                    POLL_SIMULATE_JOB)

    def is_simulate_poll_no_task(self):
        poll_success_possibility = self.get_stage_configuration(
                                        WORKER_POLL,
                                        POLL_POLL_SUCCESS_POSSIBILITY)

        if poll_success_possibility is None:
            return False

        if poll_success_possibility and poll_success_possibility < 100:
            # Get a random integer betwenn 1 to 100. If it is greater
            # than the possibility, treat the poll as no task ready.
            r = random.randint(1, 101)
            if r > poll_success_possibility:
                return True

        return False

    def get_upload_output(self):
        return self.get_stage_configuration(WORKER_POST_RUN, POST_RUN_UPLOAD_OUTPUT)

    def get_upload_log(self):
        return self.get_stage_configuration(WORKER_POST_RUN, POST_RUN_UPLOAD_LOG)

    def get_download_code(self):
        return self.get_stage_configuration(WORKER_FETCH, FETCH_DOWNLOAD_CODE)

    def get_download_dataset(self):
        return self.get_stage_configuration(WORKER_FETCH, FETCH_DOWNLOAD_DATASET)

