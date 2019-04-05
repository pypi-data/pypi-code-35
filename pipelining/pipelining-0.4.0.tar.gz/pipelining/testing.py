from time import time, sleep
from multiprocessing import Event
from unittest import skip
from contextlib import contextmanager
from multiprocessing.managers import MakeProxyType, SyncManager
from .structure import PipeStage, Pipeline, PipeQueue, AnyPort
from .stages import SinkStage, WorkUnit

def wait_ticks(subject: PipeStage, count: int, timeout: int=None):
    while subject.ticks.get() < count:
        sleep(.2)

class StageTestBench():
    def __init__(self, subject: PipeStage, pipeline: Pipeline):
        self.__pipes: dict(PipeQueue) = {}
        self.__subject = subject
        self.__pipeline = pipeline
        self.__setup_pipes()

    def __setup_pipes(self):
        for port in self.__subject.ports():
            pipe = self.__pipeline.add_pipe(f"{port.name}_pipe")
            port.connect_to(pipe)
            self.__pipes[port.name] = pipe

    def put_unit(self, unit: WorkUnit, pipe_name: str = "input"):
        pipe = self.__pipes[pipe_name]
        pipe.put(unit)

    def get_unit(self, timeout:int=None, pipe_name: str = "output"):
        pipe = self.__pipes[pipe_name]
        pipe.get(timeout=timeout)

    def yield_units(self, timeout:int=None, max_units:int=None):
        count = 0
        while not max_units or count <= max_units:
            yield self.get_unit(timeout)
            count += 1


@contextmanager
def stage_test_bench(subject: PipeStage):
    pipeline = Pipeline()
    pipeline.add_stage(subject)
    testbench = StageTestBench(subject, pipeline)
    pipeline.start()
    yield testbench
    pipeline.stop()
    pipeline.join()


class PipeSafeMockObj:
    def __init__(self):
        self.call_parameters = []
        self._set_return_value(None)

    def __call__(self, *args, **kwargs):
        self.call_parameters.append({'args': args, 'kwargs': kwargs})
        return self.return_value

    def _get_call_parameters(self):
        return self.call_parameters

    def _set_return_value(self, value):
        self.return_value = value

    def call_count(self):
        return len(self.call_parameters)

    def called(self):
        return self.call_count() > 0


PipeSafeMockProxy = MakeProxyType("PipeSafeMockProxy", ['__call__',
                                                    '_get_call_parameters',
                                                    '_set_return_value',
                                                    '_set_return_value_empty_dict',
                                                    'assert_has_calls',
                                                    'call_count', 'called'])

SyncManager.register("PipeSafeMock", PipeSafeMockObj, PipeSafeMockProxy)
