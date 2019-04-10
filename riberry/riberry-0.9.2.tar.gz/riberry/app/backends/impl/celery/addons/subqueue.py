from celery import current_task

from .base import AddonStartStopStep
import riberry

KEY = 'rib_subqueue'


def send_task_propagate_subqueue(self, *args, **kwargs):
    kwargs['headers'] = kwargs.get('headers', {})
    if current_task and getattr(current_task.request, KEY, object) != object:
        kwargs['headers'][KEY] = current_task.request.get(KEY)
    else:
        kwargs['headers'][KEY] = kwargs['headers'].get(KEY)


class SubQueue(riberry.app.addons.Addon):

    RECEIVER_QUEUE = 'rib.external'

    def __init__(self, amount, queues):
        self.amount = amount
        self.queues = queues

    def register(self, riberry_app: 'riberry.app.base.RiberryApplication'):
        class ConcreteSubQueueStep(SubQueueStep):
            rib = riberry_app
            amount = self.amount
            queues = self.queues

        riberry_app.backend.steps['worker'].add(ConcreteSubQueueStep)
        riberry.app.backends.impl.celery.patch.patch_send_task(
            instance=riberry_app.backend.instance,
            func=send_task_propagate_subqueue,
        )


class SubQueueStep(AddonStartStopStep):

    queues: list
    amount: int

    def __init__(self, worker, **_):
        super().__init__(worker=worker, interval=1)
        self.executed = False

    def should_run(self) -> bool:
        return True

    def run(self):
        if not self.executed and self.consumer:
            for queue in self.queues:
                for num in range(self.amount):
                    self.consumer.add_task_queue(f'{queue}.{num}')
            self.executed = True
