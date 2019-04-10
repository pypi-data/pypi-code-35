import logging
from locust import HttpLocust, task, seq_task

from benchgrape.core.statement import PreparedStatementsMixin
from benchgrape.core.wamp import WampTaskSet, PubSubMixin

logger = logging.getLogger(__name__)


DEFAULT_MIN_WAIT = 1000 * 60 * 5  # 5 min
DEFAULT_MAX_WAIT = 1000 * 60 * 15  # 15 min


class StabilityTaskSet(WampTaskSet, PreparedStatementsMixin):
    """
    stays connected and every 5-15 min sets a get_history call
    """
    tasks = {}

    @task()
    def idle(self):
        pass


class StabilityActivity(HttpLocust):
    task_set = StabilityTaskSet
