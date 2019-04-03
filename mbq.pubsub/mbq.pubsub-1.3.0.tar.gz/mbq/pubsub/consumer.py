import json
import logging
import typing

from django.db.utils import InterfaceError

import arrow
import boto3
import rollbar

from . import _collector as collector
from . import constants, exceptions, models, utils


logger = logging.getLogger(__name__)

NOT_PROVIDED = object()


class Consumer:
    def __init__(
        self,
        queue_name: str,
        handlers: dict,
        default_handler: typing.Optional[typing.Callable[[str], None]] = None,
    ):
        self._queue_name = queue_name
        self._queue_full_name = utils.construct_full_queue_name(queue_name)
        self._handlers = handlers
        self._default_handler = default_handler

    @property
    def queue(self):
        if not hasattr(self, "_queue"):
            sqs = boto3.resource("sqs")
            self._queue = sqs.get_queue_by_name(QueueName=self._queue_full_name)
        return self._queue

    @property
    def dead_letter_queue(self):
        """
        Find the dead letter queue from the primary queue's redrive policy.

        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
        """

        if not hasattr(self, "_dead_letter_queue"):
            try:
                redrive_policy = json.loads(self.queue.attributes["RedrivePolicy"])
                dlq_name = redrive_policy["deadLetterTargetArn"].split(":")[-1]
            except Exception as e:
                raise exceptions.ConsumerException(
                    f"No dead letter queue configured for {self.queue}"
                ) from e

            sqs = boto3.resource("sqs")
            self._dead_letter_queue = sqs.get_queue_by_name(QueueName=dlq_name)
        return self._dead_letter_queue

    def process_queue(self):
        collector.increment("consumer.attempt_read", tags={"queue": self._queue_name})
        messages = self.queue.receive_messages(WaitTimeSeconds=5, MaxNumberOfMessages=10)
        if len(messages) > 0:
            logger.info(f"Received {len(messages)} messages")

        for message in messages:
            handler = None

            try:
                body = json.loads(message.body)
                data = json.loads(body["Message"])
                message_type = data["message_type"]
            except (json.decoder.JSONDecodeError, KeyError):
                # These exceptions indicate that this message doesn't conform to our envelope
                # structure; we should attempt to use the default message handler, if the user
                # has set it
                message_type = constants.DEFAULT_MESSAGE_TYPE
                if self._default_handler:
                    handler = self._default_handler
                    payload = message.body

            if not handler and utils.is_proto_message_type(message_type):
                proto = utils.get_proto_from_message_type(message_type)
                handler = self._handlers.get(proto)
                if handler:
                    payload = proto()
                    payload.ParseFromString(data["payload"].encode())
            elif not handler:
                handler = self._handlers.get(message_type)
                payload = data["payload"]

            try:
                if handler:
                    logger.info(f"Processing {message_type} message")
                    handler(payload)
                    result = "succeeded"
                else:
                    result = "skipped"
                    logger.info(f"Received unregistered message_type: {message_type}")
            except InterfaceError:
                # This exception will raise if the db connetion is unexpectedly closed. We want to
                # raise it to the top of the stack so that the process exits
                raise
            except Exception:
                result = "failed"
                messageId = body["MessageId"]
                uuid = rollbar.report_exc_info(
                    payload_data={"context": f"pubsub-message-id#{messageId}"}
                )  # is None on local container test
                url = f"https://rollbar.com/item/uuid/?uuid={uuid}"
                logger.exception(
                    f"An error occurred while processing the "
                    f"message. MessageId: {messageId} Rollbar URL: {url}"
                )
            else:
                message.delete()

            collector.increment(
                "consumer.processed",
                tags={"result": result, "message_type": message_type, "queue": self._queue_name},
            )

    def process_dead_letter_queue(self):
        messages = self.dead_letter_queue.receive_messages(
            WaitTimeSeconds=0, MaxNumberOfMessages=10
        )
        if len(messages) > 0:
            logger.info(f"Received {len(messages)} messages on the dead letter queue")

        for message in messages:
            try:
                body = json.loads(message.body)
                data = json.loads(body["Message"])
                message_type = data["message_type"]
            except Exception as e:
                if self._default_handler:
                    message_type = constants.DEFAULT_MESSAGE_TYPE
                else:
                    raise e

            models.UndeliverableMessage.objects.create(
                message_type=message_type,
                message_timestamp=arrow.get(body.get("Timestamp")).datetime,
                payload=message.body,
                queue=self._queue_name,
                topic_arn=body.get("TopicArn"),
            )
            message.delete()

    def replay_dead_letter_queue(self, max_messages: int):
        if max_messages < 1:
            raise exceptions.ConsumerException("max_messages must be greater than 0")

        logger.info(
            f"Replaying at most {max_messages} messages "
            f"from {self.dead_letter_queue} to {self.queue}"
        )

        messages_processed = 0
        while True:
            messages = self.dead_letter_queue.receive_messages(
                WaitTimeSeconds=20, MaxNumberOfMessages=10
            )

            for message in messages:
                self.queue.send_message(MessageBody=message.body)
                message.delete()
                messages_processed += 1

                if messages_processed >= max_messages:
                    return
