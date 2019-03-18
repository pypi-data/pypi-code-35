import time
from abc import ABC, abstractmethod
from typing import List
from msbase.subprocess_ import try_call_std
from msbase.utils import append_pretty_json, datetime_str

def to_matrix_internal(config_pairs):
    if not len(config_pairs):
        return []
    key, values = config_pairs[0]
    configs = []
    tail_configs = to_matrix_internal(config_pairs[1:])
    for v in values:
        if not tail_configs:
            configs.append([(key, v)])
        configs.extend([dict([(key, v)] + config) for config in tail_configs])
    return configs

def to_matrix(configs):
    return to_matrix_internal(list(configs.items()))

class Step(object):
    def __init__(self, name: str, command: List[str], cwd:str=None, env={}, configurations={}):
        self.name = name
        self.command = command
        self.config_matrix = to_matrix(configurations)
        self.cwd = cwd
        self.env = env

class AbstractLab(ABC):
    def __init__(self, name: str, steps: List[Step]):
        self.name  = name
        self.steps = steps

    @abstractmethod
    def digest_output(self, name: str, output):
        raise NotImplementedError

    def log(self, content):
        append_pretty_json(content, path=self.session_id + ".log")

    def run(self):
        self.session_id = "run-%s-%s" % (self.name, datetime_str())
        for step in self.steps:
            for config in step.config_matrix:
                start_seconds = time.time()
                output = try_call_std(step.command, cwd=step.cwd,
                                      env=dict(step.env, **config))
                seconds_spent = time.time() - start_seconds
                stat = {"step_name": step.name, "seconds": seconds_spent,
                        "output": output}
                stat = dict(self.digest_output(step.name, output), **stat)
                stat = dict(config, **stat)
                self.log(stat)
