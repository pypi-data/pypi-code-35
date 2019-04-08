import uuid

from django.core.management import BaseCommand

from mbq import env, pubsub
from mbq.protos.invoicing.events import invoice_updated_pb2


class Command(BaseCommand):
    def handle(self, *args, **options):
        invoice_event = invoice_updated_pb2.InvoiceUpdatedEvent()
        invoice_event.invoice.id = str(uuid.uuid4())

        pubsub.publish_proto(invoice_event, env.get("SNS_ARN"))

        print(f"Proto published: {str(invoice_event)}")
