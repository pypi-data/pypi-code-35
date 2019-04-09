import uuid

from django.core.management import BaseCommand

from mbq import env, pubsub
from mbq.protos.test import test_pb2


class Command(BaseCommand):
    def handle(self, *args, **options):
        test = test_pb2.Test()
        test.id = str(uuid.uuid4())

        pubsub.publish_proto(test, env.get("SNS_ARN"), use_atomiq=False)

        print(f"Proto published: {str(test)}")
