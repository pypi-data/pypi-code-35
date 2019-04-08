import enum
import functools
import importlib
import json
import re
import time

from django.db import connections
from django.db.migrations.executor import MigrationExecutor

import arrow

from .exceptions import EnvelopeException
from .settings import project_settings


_DB_READY = {}
PROTO_MESSAGE_PREFIX = r"^proto\."
PROTO_CLASS_PATTERN = r"\.([^.]*)$"


class PayloadType(enum.Enum):
    PROTO = "proto"
    JSON = "json"


class Envelope:
    def __init__(
        self,
        message_type: str,
        payload: str,
        payload_type: PayloadType,
        envelope_created_at: arrow.Arrow,
    ):
        self.message_type = message_type
        self.payload = payload
        self.payload_type = payload_type
        self.envelope_created_at = envelope_created_at

    def __eq__(self, other):
        return (
            self.message_type == other.message_type
            and self.payload == other.payload
            and self.payload_type is other.payload_type
            and self.envelope_created_at == other.envelope_created_at
        )

    def dumps(self):
        obj = {
            "message_type": self.message_type,
            "payload": self.payload,
            "payload_type": self.payload_type.value,
            "envelope_created_at": self.envelope_created_at.format(),
        }

        return json.dumps(obj)

    @classmethod
    def from_sqs_message(cls, message):
        try:
            body = json.loads(message.body)
            obj = json.loads(body["Message"])

            envelope_created_at_str = obj.get("envelope_created_at")
            if envelope_created_at_str:
                envelope_created_at = arrow.get(envelope_created_at_str)
            else:
                envelope_created_at = arrow.now()

            return cls(
                # `message_type` and `payload` are the two required attributes of the envelope;
                # if they are not present in the message body, raise
                obj["message_type"],
                obj["payload"],
                # All properties following this comment are optional in the message body to
                # maintain backwards compatibility
                PayloadType(obj.get("payload_type", "json")),
                envelope_created_at,
            )
        except Exception as e:
            raise EnvelopeException from e


def construct_full_queue_name(queue_name):
    return f"mbq-{project_settings.SERVICE}-{queue_name}-{project_settings.ENV.short_name}"


def debounce(seconds=None, minutes=None, hours=None):
    def wrapper(func):
        func.seconds_between_runs = 0
        func.last_run = time.time()

        if seconds:
            func.seconds_between_runs += seconds
        if minutes:
            func.seconds_between_runs += minutes * 60
        if hours:
            func.seconds_between_runs += hours * 60 * 60

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if func.last_run + func.seconds_between_runs < time.time():
                func(*args, **kwargs)
                func.last_run = time.time()

        return wrapped_func

    return wrapper


def is_db_ready(database="default"):
    """Determine whether the migrations for pubsub are up to date. Can
    be used to defer hitting the database until everything is ready.

    Implementation is inspired by the `./manage.py migrate --plan` command:

       https://github.com/django/django/blob/master/django/core/management/commands/migrate.py#L140-L150
    """
    global _DB_READY

    if not _DB_READY.get(database, False):
        executor = MigrationExecutor(connections[database])
        # find the pubsub migrations
        pubsub_migrations = [
            node for node in executor.loader.graph.leaf_nodes() if node[0] == "pubsub"
        ]
        # build a plan to run all the migrations
        plan = executor.migration_plan(pubsub_migrations)
        # if there's no plan then we're fully up to date
        _DB_READY[database] = not bool(plan)

    return _DB_READY[database]


def get_proto_from_message_type(message_type: str):
    try:
        full_path = re.sub(PROTO_MESSAGE_PREFIX, "", message_type)
        proto_class = re.search(PROTO_CLASS_PATTERN, full_path).groups()[0]
        proto_path = re.sub(PROTO_CLASS_PATTERN, "", full_path)
        module = importlib.import_module(proto_path)
        return getattr(module, proto_class)
    except ModuleNotFoundError:
        return None
