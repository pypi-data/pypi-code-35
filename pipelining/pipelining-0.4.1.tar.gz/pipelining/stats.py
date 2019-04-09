from time import time
from .structure import Pipeline, PipeStage

def __yield_throughputs(pipeline: Pipeline, time_delta: float):
    output = {}
    for name, stage in pipeline.stages.items():
        tp = stage.ticks.get() / time_delta
        output[name]= tp
    return output

def compute_throughput(pipeline: Pipeline):
    if not pipeline.ticks_ts:
        raise Exception("Pipeline hasn't started")

    time_delta = time() - pipeline.ticks_ts
    return __yield_throughputs(pipeline, time_delta)

def __yield_pipe_sizes(pipeline: Pipeline):
    for name, queue in pipeline.queues.items():
        yield dict(name=name, size=queue.qsize())

def compute_pipe_sizes(pipeline: Pipeline):
    sizes = __yield_pipe_sizes(pipeline)
    return list(sizes)