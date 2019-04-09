import uuid

from django.core.management.base import BaseCommand

from mbq import env, pubsub
from mbq.protos.test import test_exception_pb2


class Command(BaseCommand):
    def handle(self, *args, **options):
        test = test_exception_pb2.TestException()
        test.id = str(uuid.uuid4())

        pubsub.publish_proto(test, env.get("SNS_ARN"), use_atomiq=False)

        print(f"Proto published: {str(test)}")
