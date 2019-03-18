# this task is chief if task_index = 0
from common.global_variable import (SUPPORTED_JOB_TYPES,
                                    JOB_CONTENT_TYPE_DATASET,
                                    JOB_CONTENT_TYPE_CODE)


class TrainingTask(object):
    def __init__(self,
                 job_uuid=None,
                 task_uuid=None,
                 keep_alive_interval=None,
                 signal_finish=None,
                 ask_finish=None,
                 task_role=None,
                 job_type=None,
                 cluster_spec=None,
                 task_index=None,
                 download_urls=None,
                 dataset_name=None,
                 is_dataset_persisted=None):

        # Validate task_uuid
        if job_uuid is None:
            raise ValueError("job_uuid is None")

        self.job_uuid = job_uuid

        # Validate task_uuid
        if task_uuid is None:
            raise ValueError("task_uuid is None")

        self.task_uuid = task_uuid

        # Validate job_uuid
        if job_uuid is None:
            raise ValueError("job_uuid is None")

        self.job_uuid = job_uuid

        # Validate keep_alive_interval
        if keep_alive_interval is None:
            raise ValueError("keep_alive_interval is None")

        try:
            self.keep_alive_interval = int(keep_alive_interval)
        except:
            raise ValueError("keep_alive_interval is not integer")

        if self.keep_alive_interval <= 0:
            raise ValueError("keep_alive_interval is not greater than 0")

        # Validate signal_finish
        if signal_finish is None:
            raise ValueError("signal_finish is None")

        try:
            self.signal_finish = bool(signal_finish)
        except:
            raise ValueError("signal_finish is not boolean")

        # Validate ask_finish
        if ask_finish is None:
            raise ValueError("ask_finish is None")

        try:
            self.ask_finish = bool(ask_finish)
        except:
            raise ValueError("ask_finish is not boolean")

        # Validate task cannot be both ask and signal finish
        if self.signal_finish and self.ask_finish:
            raise ValueError("unexpected task both signal and ask finish")

        # Validate task_role
        if task_role is None:
            raise ValueError("task_role is None")

        if task_role != "worker" and task_role != "ps":
            raise ValueError("task_role {} is not valid".format(task_role))

        self.task_role = task_role

        # Validate job_type
        if job_type is None:
            raise ValueError("job_type is None")

        if job_type not in SUPPORTED_JOB_TYPES:
            raise ValueError("job_type is not supported")

        self.job_type = job_type

        # Validate download_urls
        if download_urls is None:
            raise ValueError("download_urls is None")

        # Code must be in the download_urls
        if JOB_CONTENT_TYPE_CODE not in download_urls:
            raise ValueError("missing {} in download_urls".format(
                                JOB_CONTENT_TYPE_CODE))

        if download_urls[JOB_CONTENT_TYPE_CODE] is None or \
           len(download_urls[JOB_CONTENT_TYPE_CODE]) == 0:
           raise ValueError("invalid {} in download_urls".format(
                                JOB_CONTENT_TYPE_CODE))

        self.download_urls = download_urls

        # Task state is set to False by default. It is only set to true when
        # the worker reported to master that the task has terminated successfully.
        self.finished = False
        self.cluster_spec = cluster_spec
        self.task_index = task_index
        self.tensorboard_process = None
        self.dataset_name = dataset_name
        self.is_dataset_persisted = is_dataset_persisted
        self.dataset_local_path = None
        self.output_upload_urls = None
        # Validate for worker task
        if task_role == "worker":
            if self.dataset_name is None:
                raise ValueError("worker task requires dataset_name")

            if self.is_dataset_persisted is None:
                raise ValueError("worker task requires is_dataset_persisted")

            # Dataet must be in the download_urls for worker role
            if JOB_CONTENT_TYPE_DATASET not in download_urls:
                raise ValueError("worker task requires {} in download_urls".format(
                                    JOB_CONTENT_TYPE_DATASET))

            if download_urls[JOB_CONTENT_TYPE_DATASET] is None or \
               len(download_urls[JOB_CONTENT_TYPE_DATASET]) == 0:
               raise ValueError("invalid {} in download_urls".format(
                                    JOB_CONTENT_TYPE_DATASET))
