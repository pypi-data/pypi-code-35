from __future__ import print_function
import time

from simpleflow import (
    activity,
    Workflow,
    futures,
)


def as_activity(func):
    func.get_task_id = lambda wf, *args, **kwargs: "INCREMENTING-{}".format(args[0])
    return activity.with_attributes(
        task_list="quickstart",
    )(func)

@as_activity
def increment(x):
    time.sleep(20)
    return x + 1


class BasicWorkflow(Workflow):
    name = 'basic'
    version = 'example'
    task_list = 'example'
    tag_list = ['a=1', 'b=foo']

    def run(self, x, t=30):
        y = self.submit(increment, x)
        futures.wait(y)
