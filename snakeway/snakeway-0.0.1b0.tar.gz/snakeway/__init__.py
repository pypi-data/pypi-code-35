import threading
import time
from queue import Queue

from snakeway.dto import CheckpointInfo, Stage
from snakeway.recorder import Recorder
from snakeway.stats import Stats
from snakeway.webserver import Server

recorder: Recorder = None


def run() -> None:
    global recorder
    q = Queue()
    st = Stats()
    Server(st).start()
    recorder = Recorder(q, st)
    recorder.start()


def check(label) -> None:
    tid = threading.get_ident()  # FIXME: Not safe
    data = CheckpointInfo(
        cid=tid,
        ts=time.time_ns(),
        label=label,
        stage=Stage.IN
    )
    recorder.q.put(data)


def begin(checkpoint_label) -> None:
    tid = threading.get_ident()  # FIXME: Not safe
    data = CheckpointInfo(
        cid=tid,
        ts=time.time_ns(),
        label='begin',
        stage=Stage.START,
        checkpoint_label=checkpoint_label
    )
    recorder.q.put(data)


def finish(label='finish') -> None:
    tid = threading.get_ident()  # FIXME: Not safe
    data = CheckpointInfo(
        cid=tid,
        ts=time.time_ns(),
        label=label,
        stage=Stage.END
    )
    recorder.q.put(data)
