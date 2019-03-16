import logging
from typing import TYPE_CHECKING

from ktdk.runtime.context import Context

if TYPE_CHECKING:
    from ktdk.core.tasks import Task

log = logging.getLogger(__name__)


class ContextMixin:
    @property
    def context(self) -> Context:
        return getattr(self, '_context', None)

    def inject_context(self, context):
        setattr(self, '_context', context)


class CheckersMixin:
    def check_that(self, task: 'Task', points_multiplier: float = 0, after_tasks: bool = False):
        """Adds the check task
        Args:
            after_tasks:
            points_multiplier: If this task fails, how much from the test points should be discarded
            task(Task): Task instance
        """
        from .tasks import TaskType
        setattr(task, '_type', TaskType.CHECKED)
        setattr(task, '_points_multiplier', points_multiplier)
        if after_tasks:
            self.add_after(task)
        else:
            self.add_task(task)
        return self

    def require_that(self, task: 'Task', points_multiplier: float = 0, after_tasks: bool = False):
        """Requires a subtask to pass
        Args:
            after_tasks: It should be executed after the tasks execution
            points_multiplier: If this task fails, how much from the test points should be discarded
            task(Task):
        """
        from .tasks import TaskType
        self.check_that(task, points_multiplier=points_multiplier, after_tasks=after_tasks)
        task.type = TaskType.REQUIRED
        return self

    def abort(self, message: str, points_multiplier: float = 0):
        from ktdk.asserts.checks.general import AbortTask
        log.warning(f"[ABORT] Aborted {self.name}: {message}")
        self.require_that(AbortTask(message=message), points_multiplier=points_multiplier)
