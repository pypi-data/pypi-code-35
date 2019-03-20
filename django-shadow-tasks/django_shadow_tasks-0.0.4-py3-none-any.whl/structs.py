import json
import importlib

from typing import NamedTuple, Sequence, Mapping

from .routing import TasksRouter

__all__ = ('DelayedTask',)


class DelayedTask(NamedTuple):
    """
    Wrapper on the task.
    """
    path: str
    args: Sequence = None
    kwargs: Mapping = None
    ack_late: bool = True

    def to_bytes(self):
        return json.dumps(self._asdict(), ensure_ascii=False)

    @classmethod
    def from_bytes(cls, b_data):
        data = json.loads(b_data.decode())
        return cls(**data)

    @property
    def routing_key(self):
        return TasksRouter.get_routing_key_for_task(self.path)

    def __call__(self):
        """Call task from `self.path`."""
        f_path = self.path
        f_module_path, f_name = f_path.rsplit('.', 1)
        f_module = importlib.import_module(f_module_path)

        func = getattr(f_module, f_name)

        return func(*(self.args or tuple()), **(self.kwargs or dict()))
