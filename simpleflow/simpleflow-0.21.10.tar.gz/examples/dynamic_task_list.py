from __future__ import print_function

from simpleflow import activity, Workflow


@activity.with_attributes(task_list="static", version="example")
def increment(x):
    return x + 1


# @activity.with_attributes(task_list='quickstart', version='example')
# => we don't decorate activity directly, we'll decorate it dynamically
# in the workflow so the task list for "double" is dynamic
def double(x):
    return x * 2


class BasicWorkflow(Workflow):
    name = "basic"
    version = "example"
    task_list = "example"
    tag_list = ["a=1", "b=foo"]

    def run(self, x, t=30):
        execution = self.get_run_context()
        y = self.submit(increment, x)
        print("self.get_run_context() => {}".format(execution))
        task_list = "dynamic"
        z = self.submit(
            activity.with_attributes(task_list=task_list, version="example")(double), y
        )

        print("{x} + 1 = {result}".format(x=x, result=xr.result))
        return z.result
