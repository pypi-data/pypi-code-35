from typing import Iterable, Union
from .structure import InputPort, OutputPort, PipeStage, WorkUnit

class EmitterStage(PipeStage):
    def __init__(self, name: str, emitter: callable = None):
        super().__init__(name)
        self.__emitter = emitter
        self.output = OutputPort("output", self)

    def ports(self):
        yield self.output

    def emit(self):
        return self.__emitter()

    def work(self):
        for work in self.emit():
            self.output.put(work)
            self.tick()

class MapperStage(PipeStage):
    def __init__(self, name: str, mapper: callable = None):
        super().__init__(name)
        self.input = InputPort("input", self)
        self.output = OutputPort("output", self)
        self.__mapper = mapper

    def ports(self):
        yield self.input
        yield self.output

    def map(self, unit: WorkUnit)->Iterable[WorkUnit]:
        mapped = self.__mapper(unit)
        
        if not mapped:
            return

        if isinstance(mapped, Iterable):
            for unit in mapped:
                yield unit

        yield mapped

    def work(self):
        while True:
            original = self.input.get()
            for unit in self.map(original):
                self.output.put(unit)
            self.input.task_done()
            self.tick()


class ForkStage(PipeStage):
    def __init__(self, name: str, output_count: int):
        super().__init__(name)
        self.input = InputPort("input", self)
        self.outputs = []
        
        for i in range(0, output_count):
            port = OutputPort(f"output_{i}", self)
            self.outputs.append(port)

    def ports(self):
        yield self.input
        for output in self.outputs:
            yield output

    def work(self):
        while True:
            work = self.input.get()
            for output in self.outputs:
                output.put(work)
            self.input.task_done()
            self.tick()


class ThrottleStage(PipeStage):
    def work(self):
        pass

class BatchingStage(PipeStage):
    def work(self):
        pass

class MuxerStage(PipeStage):
    def work(self):
        pass

class DemuxerStage(PipeStage):
    def work(self):
        pass

class SinkStage(PipeStage):
    def __init__(self, name: str, consumer: callable = None):
        super().__init__(name)
        self.__consumer = consumer
        self.input = InputPort("input", self)
    
    def ports(self):
        yield self.input

    def consume(self, unit: WorkUnit):
        self.__consumer(unit)

    def work(self):
        while True:
            work = self.input.get()
            self.consume(work)
            self.input.task_done()
            self.tick()

