from worker.worker_fsm import WorkerStateMachine
from worker.worker_start import *


def worker_entry(runtime: WorkerRuntime,
                 workdir: str,
                 toplevel_datadir: str,
                 port: int,
                 worker_uuid: str,
                 passcode: str,
                 gpu_id: str):

    worker = Worker(runtime.master_server(),
                    port,
                    workdir,
                    toplevel_datadir,
                    worker_uuid=worker_uuid,
                    gpu_id=gpu_id,
                    passcode=passcode)

    worker_stm = WorkerStateMachine(worker, runtime)
    worker_stm.start()
