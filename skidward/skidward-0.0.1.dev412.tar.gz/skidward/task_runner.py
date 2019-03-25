import datetime
import logging

from redis_log_handler import RedisKeyHandler

from skidward.app import app
from skidward import worker_detector
from skidward.models import db, Job, JobStatus, Message, Task
from skidward.backend import get_redis_backend, get_backend_configuration


MESSAGE_EXPIRATION_DURATION = 10


class TaskRunner:
    def __init__(self, task_id, context, worker_name):
        with app.app_context():
            self.task = Task.query.get(task_id)
            self.context = context
            self.worker_name = worker_name
            self.redis_client = get_redis_backend()

            self.start()

    @staticmethod
    def get_unique_message_key(job_id, task_id):
        return "J{}-T{}".format(job_id, task_id)

    def _create_new_job(self):
        job = Job(
            state=JobStatus.RUNNING,
            ran_at=datetime.datetime.utcnow(),
            task_id=self.task.id,
        )
        db.session.add(job)
        db.session.commit()

        return job

    def _get_logging_key(self, job):
        key = self.context.get("LOGGING_KEY")
        if key:
            return key

        return TaskRunner.get_unique_message_key(job.id, self.task.id)

    def _set_logging_config(self, logging_key):
        raw_logs = self.context.get("RAW_LOGS", False)
        log_handler = RedisKeyHandler(
            logging_key, raw_logging=raw_logs, **get_backend_configuration()
        )
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)

        logging.info("Logging {}".format(self.worker_name))

    def _persist_logs(self, job, logging_key):
        def _get_all_log_messages():
            return self.redis_client.lrange(logging_key, 0, -1)

        messages = [
            Message(job_id=job.id, content=msg) for msg in _get_all_log_messages()
        ]
        db.session.bulk_save_objects(messages)

    def _expire_logs(self, logging_key):
        self.redis_client.expire(logging_key, MESSAGE_EXPIRATION_DURATION)

    def start(self):
        # Need to create a job to fallback to a unique message key for Redis
        # happening before the first logging takes place.
        job = self._create_new_job()

        logging_key = self._get_logging_key(job)
        self._set_logging_config(logging_key)

        logging.info("Job id:{} created".format(job.id))

        worker_module = worker_detector.load_worker_on_namespace(self.worker_name)

        logging.info("{} is running".format(self.worker_name))

        try:
            worker_module.start(self.context)
            status = JobStatus.SUCCESS
        except Exception as e:
            status = JobStatus.FAIL
            logging.info(e)

        logging.info("Status : {}".format(status))

        job.state = status
        self._persist_logs(job, logging_key)
        db.session.commit()

        self._expire_logs(logging_key)
