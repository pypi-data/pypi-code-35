from time import time, sleep
from multiprocessing import Event
from unittest import skip
from contextlib import contextmanager
from .structure import PipeStage, Pipeline
from .stages import SinkStage, WorkUnit

class AssertionSink(SinkStage):
    def __init__(self, unit_asserter: callable, max_ticks: int = None, max_ticks_event: Event = None):
        super().__init__(name="assertion")
        self.__unit_asserter = unit_asserter

    def consume(self, unit: WorkUnit):
        self.__unit_asserter(unit)

    def wait_ticks(self, count: int, timeout: int=None):
        while self.ticks.get() < count:
            sleep(.2)

@contextmanager
def stage_workbench(subject: PipeStage, expected_ticks: int, output_asserter: callable=None):
    pipeline = Pipeline()
    inbound = pipeline.add_pipe("inbound")
    outbound = pipeline.add_pipe("outbound")
    
    subject.input.connect_to(inbound)
    subject.output.connect_to(outbound)
    pipeline.add_stage(subject)
    
    assertion = AssertionSink(unit_asserter=output_asserter)
    assertion.input.connect_to(outbound)
    pipeline.add_stage(assertion)
    pipeline.start()

    yield inbound
    
    assertion.wait_ticks(expected_ticks)
    pipeline.terminate()