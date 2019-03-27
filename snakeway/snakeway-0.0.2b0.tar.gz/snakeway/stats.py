from collections import defaultdict, deque
from itertools import tee
from statistics import mean
from threading import Lock
from typing import Dict

from snakeway import Stage
from snakeway.dto import CheckpointInfo


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Stats:
    def __init__(self):
        self.data: Dict[str, dict] = {}
        self.open_checkpoints: Dict[int, str] = {}
        self.stats: Dict[str, dict] = {}
        self.lock = Lock()

    def put(self, data: CheckpointInfo):
        with self.lock:
            clabel = data.checkpoint_label
            if data.stage == Stage.START:
                assert data.cid not in self.open_checkpoints
                if clabel not in self.data:
                    self.data[clabel] = {
                        'threaded': defaultdict(deque)
                    }
                self.open_checkpoints[data.cid] = clabel
                self.data[clabel]['threaded'][data.cid].append(data)
            elif data.stage == Stage.IN:
                clabel = self.open_checkpoints[data.cid]
                assert not any(
                    x.label == data.label for x in
                    self.data[clabel]['threaded'][data.cid]), "Duplicated label"
                self.data[clabel]['threaded'][data.cid].append(data)
            elif data.stage == Stage.END:
                clabel = self.open_checkpoints[data.cid]
                del self.open_checkpoints[data.cid]
                part = self.data[clabel]['threaded'][data.cid]
                part.append(data)
                self.process_part(clabel, part)
                part.clear()

    def process_part(self, clabel: str, part: deque):
        if clabel not in self.stats:
            self.stats[clabel] = defaultdict(deque)
        for ca, cb in pairwise(part):
            self.stats[clabel][(ca.label, cb.label)].append(cb.ts - ca.ts)

    def get_stats(self):
        ret = {}
        with self.lock:
            for stat, data in self.stats.items():
                part_stats = {}
                ret[stat] = part_stats
                for labels, values in data.items():
                    part_stats[labels] = {
                        'max': max(values),
                        'min': min(values),
                        'avg': mean(values)
                    }
        return ret
