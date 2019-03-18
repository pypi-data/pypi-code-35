import datetime
import logging

from redis_log_handler import RedisKeyHandler

from skidward.app import app
from skidward import worker_detector
from skidward.models import db, Job, JobStatus, Message, Task
from skidward.backend import get_redis_backend, get_backend_configuration


MESSAGE_EXPIRATION_DURATION = 10


class TaskRunner:
    def __init__(self, task_id):
        with app.app_context():
            self.task = Task.query.get(task_id)
            self.context = self.task.context
            self.worker_name = self.task.worker.name
            self.redis_client = get_redis_backend()

            self.start()

    def _create_new_job(self):
        job = Job(
            state=JobStatus.RUNNING,
            ran_at=datetime.datetime.utcnow(),
            task_id=self.task.id,
        )
        db.session.add(job)
        db.session.commit()

        logging.info("Job id:{} created".format(job.id))

        return job

    def _set_logging_config(self):
        log_handler = RedisKeyHandler(
            self.context.get("LOGGING_KEY"), **get_backend_configuration()
        )
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)

        logging.info("Logging {}".format(self.worker_name))

    def _persist_logs(self, job):
        def _get_all_log_messages():
            return self.redis_client.lrange(self.context.get("LOGGING_KEY"), 0, -1)

        messages = [
            Message(job_id=job.id, content=msg) for msg in _get_all_log_messages()
        ]
        db.session.bulk_save_objects(messages)

    def _expire_logs(self):
        self.redis_client.expire(
            self.context.get("LOGGING_KEY"), MESSAGE_EXPIRATION_DURATION
        )

    def start(self):
        self._set_logging_config()

        job = self._create_new_job()
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
        self._persist_logs(job)
        db.session.commit()

        self._expire_logs()
