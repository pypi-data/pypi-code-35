from simpleflow import (
    activity,
    Workflow,
)


@activity.with_attributes(task_list='quickstart', version='example')
def task():
    return 1


class MyWorkflow(Workflow):
    name = 'basic'
    version = 'example'
    task_list = 'example'

    def __init__(self, x):
        self.items = []

    def run(self, x):
        self.items.append("foo")
        print self.items
        for i in [1, 2, 3, 4]:
            future = self.submit(task)
            future.wait()
