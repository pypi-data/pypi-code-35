import copy
import os
import time
from itertools import chain
from datetime import datetime as dt
from ast import literal_eval
import multiprocessing as mp

from cronex import CronExpression

from skidward.backend import get_redis_backend
from skidward.models import Task
from skidward.task_runner import TaskRunner


REDIS_ELECTION_TTL = 60
REDIS_MANUAL_CHANNEL = "MANUAL_RUN"
REDIS_CONFIGURED_RUN_CHANNEL = "CONFIGURED_RUN"
WAKEUP_TIMER = int(os.getenv("WAKEUP_TIMER"))

mp_context = mp.get_context("spawn")
process_id = os.getpid()


class Elector:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def get_tasks(self):
        for task in chain(
            self.get_scheduled_tasks(),
            self.get_manual_tasks(),
            self.get_configured_tasks(),
        ):
            yield task

    def get_scheduled_tasks(self):
        for task in self.get_elected_tasks(Task.query.filter(Task.enabled).all()):
            yield task

    def get_manual_tasks(self):
        task_id = self.redis_client.rpop(REDIS_MANUAL_CHANNEL)
        while task_id:
            yield Task.query.get(task_id)
            task_id = self.redis_client.rpop(REDIS_MANUAL_CHANNEL)

    def get_configured_tasks(self):
        task_id, context = self.redis_client.hmget(
            REDIS_CONFIGURED_RUN_CHANNEL, keys=["task_id", "overwrite_context"]
        )
        while task_id:
            self.redis_client.hdel(
                REDIS_CONFIGURED_RUN_CHANNEL, "task_id", "overwrite_context"
            )
            task = Task.query.get(task_id)
            temp_task = copy.copy(task)
            temp_task.context = literal_eval(context)
            yield temp_task
            task_id, context = self.redis_client.hmget(
                REDIS_CONFIGURED_RUN_CHANNEL, keys=["task_id", "overwrite_context"]
            )

    def get_elected_tasks(self, tasks):
        return [task for task in tasks if self.is_runner_elected_for_task(task)]

    def is_runner_elected_for_task(self, task):
        date_tuple = dt.utcnow().timetuple()[:5]
        date_mask = "-".join(map(str, date_tuple))
        unique_key = f"{task.id}-{date_mask}"

        cron_expression = CronExpression(task.cron_string)
        if cron_expression.check_trigger(date_tuple):
            if not self.redis_client.exists(unique_key):
                self.redis_client.set(
                    unique_key, process_id, ex=REDIS_ELECTION_TTL, nx=True
                )
                return self.redis_client.get(unique_key) == str(process_id)

        return False


class SchedulerRunner:
    def __init__(self):
        self.elector = Elector(get_redis_backend())

    def run(self):
        while True:
            for task in self.elector.get_tasks():
                p = mp_context.Process(
                    target=TaskRunner, args=(task.id, task.context, task.worker.name)
                )
                p.start()

            time.sleep(WAKEUP_TIMER)


def start():
    SchedulerRunner().run()
