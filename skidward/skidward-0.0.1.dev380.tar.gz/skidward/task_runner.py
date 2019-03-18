import datetime
import logging

from redis_log_handler.RedisLogHandler import RedisLogHandler

from skidward.app import app
from skidward import worker_detector
from skidward.models import db, Job, JobStatus, Task


class TaskRunner:
    def __init__(self, task_id):
        with app.app_context():
            self.task = Task.query.get(task_id)
            self.context = self.task.context
            self.worker_name = self.task.worker.name

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
        log_handler = RedisLogHandler(self.context.get("LOGGING_CHANNEL"))
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)

        logging.info("Logging {}".format(self.worker_name))

    def start(self):
        self._set_logging_config()

        job = self._create_new_job()
        worker_module = worker_detector.load_worker_on_namespace(self.worker_name)

        logging.info("{} is running".format(self.worker_name))

        try:
            worker_module.start(self.context)
            status = JobStatus.SUCCESS
        except:
            status = JobStatus.FAIL

        logging.info("Status : {}".format(status))

        job.state = status
        db.session.commit()
