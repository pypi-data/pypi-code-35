import argparse
import multiprocessing as mp
import os.path
import sys
from datetime import datetime
from multiprocessing.connection import wait

# Add the top-level directory to the PYTHONPATH
worker_main_dir_path = os.path.dirname(os.path.realpath(__file__))
worker_dir_path = os.path.abspath(os.path.join(worker_main_dir_path, os.pardir))
sys.path.insert(0, worker_dir_path)

from main.worker_entry import worker_entry
from main.utils import *

from worker.worker_runtime import *

###############################################################################

DDL_WORKDIR_NAME = "workdir"
DDL_METADIR_NAME = "meta"
DDL_DATADIR_NAME = "data"

###############################################################################

def start_workers_main(runtime, datadir):

    # First attempt to get the simulated registration. If that does not exist,
    # query the database for the real registration.
    registered_workers = runtime.get_fake_registration()
    if not registered_workers:
        registered_workers = get_registered_workers()

    if not registered_workers:
        print("[Error::FATAL] Malformed worker register file or no worker.")
        return

    handles = []
    worker_processes = {}
    for worker_uuid in registered_workers.keys():
        worker_config = registered_workers[worker_uuid]
        success, gpu_id = gpu_uuid_to_gpu_id(runtime, worker_config["gpu_uuid"])
        if not success:
            print("[Error::FATAL] Worker {} has an invalid GPU {}. Skip it.".format(
                  worker_uuid,
                  worker_config["gpu_uuid"]))

            continue

        worker_config["gpu_id"] = gpu_id
        p = mp.Process(target=worker_entry,
                       args=(runtime,
                             worker_config["workdir"],
                             datadir,
                             worker_config["port"],
                             worker_uuid,
                             worker_config["passcode"],
                             worker_config["gpu_id"]))

        worker_processes[worker_uuid] = {
            'process': p,
            'config': worker_config,
            'last_start': datetime.now(),
            'stop_count': 0
        }

        p.start()
        handles += [p.sentinel]

    if not worker_processes:
        print("[INFO] No worker found. Terminate main thread.")
        return

    # Monitor the health of all the processes.
    while True:
        # Wait until any process terminates.
        wait(handles)
        # Need to update handles as processes can come and go.
        handles = []
        # Monitor the health of each process.
        worker_uuids = list(worker_processes.keys())
        for worker_uuid in worker_uuids:
            worker_context = worker_processes[worker_uuid]
            process = worker_context['process']
            if process.is_alive():
                # A running process should just keep running. Keep track its
                # handle so that main process can wait for it.
                handles += [process.sentinel]
                continue

            process.join()
            worker_context["stop_count"] += 1
            print("[INFO] {} has terminated! Count: {}".format(
                    worker_uuid,
                    worker_context["stop_count"]))

            # This process has terminated. If only run once, do not attempt
            # to restart. Otherwise, restart the worker.
            if runtime.run_once():
                worker_processes.pop(worker_uuid, None)
            else:
                delta = datetime.now() - worker_context['last_start']
                if delta.total_seconds() < 30 and worker_context['stop_count'] >= 5:
                    print("[Error] Worker {} restarted for too many times too quickly.".format(
                            worker_uuid))

                    worker_processes.pop(worker_uuid, None)
                else:
                    print("[INFO] Restart {}!".format(worker_uuid))
                    # Restart the worker process. Also update the new handle in
                    # the handles list.
                    worker_config = worker_context['config']
                    p = mp.Process(target=worker_entry,
                                   args=(runtime,
                                         worker_config["workdir"],
                                         datadir,
                                         worker_config["port"],
                                         worker_uuid,
                                         worker_config["passcode"],
                                         worker_config["gpu_id"]))

                    worker_context['process'] = p
                    worker_context['last_start'] = datetime.now()
                    p.start()
                    handles += [p.sentinel]

        if len(handles) == 0:
            # If there is no living process, terminate.
            print("[INFO] No living process. Terminate main thread.")
            return

def main(debug_config=None):
    if debug_config is None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--appdir',
            type=str,
            required=True,
            help='app directory for the DDL worker, must be an absolute path')
        parser.add_argument(
            '--runtime',
            type=str,
            default=None,
            help='specify a path to config file')
        parser.add_argument(
            '--sharing',
            type=int,
            default=1,
            help='specify the number of workers to register for each GPU')
        parser.add_argument(
            '--secret',
            type=str,
            default=None,
            help='secret')
        FLAGS, _ = parser.parse_known_args()
        runtime = FLAGS.runtime
        appdir = FLAGS.appdir
        secret = FLAGS.secret
        sharing = FLAGS.sharing
    else:
        runtime = debug_config.get('test_runtime', None)
        secret = debug_config.get('secret', None)
        sharing = debug_config.get('sharing', 1)
        appdir = debug_config['appdir']

    if runtime is not None and not os.path.isfile(runtime):
        raise RuntimeError('--runtime does not point to a valid config file.')

    workdir = os.path.join(appdir, DDL_WORKDIR_NAME)
    metadir = os.path.join(appdir, DDL_METADIR_NAME)
    datadir = os.path.join(appdir, DDL_DATADIR_NAME)

    # If app folder does not exist, exit now.
    if not os.path.isdir(appdir):
        print("[Error::FATAL] Does not have a valid app folder.")
        return

    # If metadir does not exist, exit now.
    if not os.path.isdir(metadir):
        print("[Error::FATAL] Does not have a valid metadir.")
        return

    # If workdir does not exist, create one.
    if not os.path.isdir(workdir):
        os.mkdir(workdir)

    # If datadir does not exist, create one.
    if not os.path.isdir(datadir):
        os.mkdir(datadir)

    # If there exists a test config, load it.
    if runtime is not None:
        print('[INFO] Use runtime from file: {}'.format(runtime))
        runtime = WorkerRuntime(runtime)
    else:
        runtime = WorkerRuntime()

    # Cleanup the local datasets.
    success = cleanup_datasets(datadir)
    if not success:
        return

    # If force registration, remove any previous registrations.
    if runtime.force_registration():
        success = unregister(workdir)
        if success:
            os.mkdir(workdir)
        else:
            return

    # Check if worker has already been registered.
    success, worker_registered = registered()
    if not success:
        # If the db cannot be connected, it is fatal. Exit now.
        return

    if not worker_registered:
        success = register(runtime, metadir, workdir, sharing, secret)
        # Registration failure is fatal. Exit now.
        if not success:
            return

    # If only doing registration, exit now.
    if runtime.registration_only():
        return

    start_workers_main(runtime, datadir)
    return


if __name__ == '__main__':
    main()
