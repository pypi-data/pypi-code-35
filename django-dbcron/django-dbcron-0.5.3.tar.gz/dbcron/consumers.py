import traceback

from django.dispatch import receiver

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic import websocket
from channels.exceptions import StopConsumer
from channels import layers

from dbcron import models
from dbcron import signals
from dbcron import settings


class JobConsumerMixin:
    model = models.Job
    queryset = model.objects.all()
    groups = [settings.JOB_GROUP]

    def base_run(self, event):
        self.job_id = event['id']
        self.job = self.queryset.get(pk=self.job_id)
        self.job.run()
        raise StopConsumer()

    def _format_status(self, event):
        status = event.copy()
        status.pop('type', None)
        return status


class JobSyncConsumer(JobConsumerMixin, websocket.JsonWebsocketConsumer):
    def run(self, event):
        self.base_run(event)

    def emit_job_status(self, event):
        status = self._format_status(event)
        self.send_json(status)


class JobAsyncConsumer(JobConsumerMixin, websocket.AsyncJsonWebsocketConsumer):
    async def run(self, event):
        await sync_to_async(self.base_run)(event)

    async def emit_job_status(self, event):
        status = self._format_status(event)
        await self.send_json(status)


def _emit_job_status(job, status, message=None):
    data = {
        'id': job.id,
        'type': 'emit.job.status',
        'status': status,
        'message': message,
    }
    if hasattr(job, 'get_absolute_url'):
        data['url'] = str(job.get_absolute_url())
    channel_layer = layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(settings.JOB_GROUP, data)


@receiver(signals.job_started, dispatch_uid="ws_job_start")
def send_job_start(sender, job, **kwargs):
    _emit_job_status(job, 'started')


@receiver(signals.job_done, dispatch_uid="ws_job_don")
def send_job_done(sender, job, **kwargs):
    _emit_job_status(job, 'done')


@receiver(signals.job_failed, dispatch_uid="ws_job_failed")
def send_job_failed(sender, job, error, **kwargs):
    message = traceback.format_exc().splitlines()[-1]
    _emit_job_status(job, 'failed', message)
