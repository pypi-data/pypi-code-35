from .structures import PipeStage, PipeQueue, InputPort, OutputPort

class EmitterProcess(PipeStage):
    def __init__(self, name: str, emitter: callable):
        super().__init__(name)
        self.__emitter = emitter
        self.output = OutputPort("output", self)

    def ports(self):
        yield self.output

    def run(self):
        for work in self.__emitter():
            self.output.put(work)
            self.tick()

class MapperProcess(PipeStage):
    def __init__(self, name: str, mapper: callable):
        super().__init__(name)
        self.input = InputPort("input", self)
        self.output = OutputPort("output", self)
        self.__mapper = mapper

    def ports(self):
        yield self.input
        yield self.output

    def run(self):
        while True:
            work = self.input.get()
            work = self.__mapper(work)
            self.output.put(work)
            self.input.task_done()
            self.tick()


class MulticastStage(PipeStage):
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

    def run(self):
        while True:
            work = self.input.get()
            for output in self.outputs:
                output.put(work)
            self.input.task_done()
            self.tick()


class ThrottleProcess(PipeStage):
    def run(self):
        pass

class BatchingProcess(PipeStage):
    def run(self):
        pass

class MuxerProcess(PipeStage):
    def run(self):
        pass

class DemuxerProcess(PipeStage):
    def run(self):
        pass

class SinkProcess(PipeStage):
    def __init__(self, name: str, consumer: callable):
        super().__init__(name)
        self.__consumer = consumer
        self.input = InputPort("input", self)
    
    def ports(self):
        yield self.input

    def run(self):
        while True:
            work = self.input.get()
            self.__consumer(work)
            self.input.task_done()
            self.tick()

