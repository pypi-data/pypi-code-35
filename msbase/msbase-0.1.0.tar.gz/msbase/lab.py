import time
import glob

from abc import ABC, abstractmethod
from typing import List
from tabulate import tabulate

from msbase.subprocess_ import try_call_std
from msbase.utils import append_pretty_json, datetime_str
from msbase.utils import load_jsonl, write_pretty_json

def to_matrix_internal(config_pairs):
    if not len(config_pairs):
        return [{}]
    key, values = config_pairs[0]
    configs = []
    tail_configs = to_matrix_internal(config_pairs[1:])
    for v in values:
        if not tail_configs:
            configs.append([(key, v)])
        configs.extend([dict(config, key=v) for config in tail_configs])
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
    def digest_output(self, name: str, output, command):
        raise NotImplementedError

    @abstractmethod
    def digest_column_names(self):
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
                        "output": output, "command": step.command }
                stat = dict(config, **stat)
                self.log(stat)

    def analyze(self):
        table = [["Step", "Runtime (s)"] + self.digest_column_names()]

        for f in sorted(glob.glob("run-%s-*.log" % self.name)):
            print("importing %s" % f)
            for log in load_jsonl(f):
                row = []
                row.append(log['step_name'])
                row.append(log['seconds'])
                digest = self.digest_output(log['step_name'], log['output'], log["command"])
                for col in self.digest_column_names():
                    row.append(digest[col])
                table.append(row)
                print('STDOUT')
                print(log['output'][0])
                print('STDERR')
                print(log['output'][1])
                print('CODE')
                print(log['output'][2])

        print(tabulate(table, headers="firstrow", tablefmt="github"))

        tex_result = tabulate(table, headers="firstrow", tablefmt="latex_raw")
        open("results.tex", "w").write(tex_result)

        write_pretty_json(table, "results.json")
