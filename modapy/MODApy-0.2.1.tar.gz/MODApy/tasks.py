import multiprocessing as mp
import os
import time
from os import path

# non persistant task list
running = {}
executed = {}
errors = {}


class Task(object):
    def __init__(self, taskfile):
        self.name = taskfile
        with open(taskfile) as t:
            msg, delay = t.read().split(";")

        self.msg = msg
        self.delay = int(delay)

    def run(self):
        print(self.msg)
        time.sleep(self.delay)


def check_for_tasks():
    """
    find files with .task ending in current directory.
    This a file based no-priority queue which only find the files
    """
    tasks = filter(lambda x: x.endswith('.task'),
                   filter(path.isfile, os.listdir('.')))
    # this should also check for jobs that are not already running ...
    return tasks


def start_task(task):
    """
    open the file, read it's conent, then start a process with the file
    running is a global directory holding the running jobs
    """
    if task not in running:
        ti = Task(task)

        p = mp.Process(target=ti.run, name=ti.name)
        p.start()
        running[ti.name] = (p, p.pid, p.is_alive())


def clean_finished_tasks():
    """
    Check the running dictionary for items, each task that is done,
    is moved to the correct place (errors, or completed),
    errors and executed are global dictionaries.
    """
    for k, v in running.items():
        print(k, v[0].is_alive())
        if not v[0].is_alive():
            if v[0].exitcode:
                errors[k] = v[0].exitcode
            else:
                executed[k] = 'success!'
                running.pop(k)
                os.rename(k, k + '.done')


def run():
    """
    The main loop of tasku where everything happens.
    """

    while True:
        for task in check_for_tasks():
            start_task(task)
