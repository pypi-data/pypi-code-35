from time import sleep
from .structure import Pipeline
from .stats import compute_pipe_sizes, compute_throughput

def run_forever(pipeline: Pipeline, report_freq=10):
    pipeline.start()
    while True:
        sleep(report_freq)
        throughputs = compute_throughput(pipeline)
        pipe_sizes = compute_pipe_sizes(pipeline)
        print(throughputs)
        print(pipe_sizes)
            
