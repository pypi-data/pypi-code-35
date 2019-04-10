import logging
import os
import six
import uuid
from locust import TaskSet

from benchgrape.core.statement import login

logger = logging.getLogger(__name__)


class LongPollingTaskSet(TaskSet):
    def on_start(self):
        self.org = int(os.getenv('ORG_ID', 1))
        logger.info('configured organization: %i', self.org)
        self.auth_token = login(self.client)
        self.user_id = six.text_type(uuid.uuid4())

        if not self.parent.host:
            raise AssertionError(
                '--host must be appended to determine the websocket location.'
            )
