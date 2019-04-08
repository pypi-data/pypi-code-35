import json
from typing import Union

import arrow
import boto3
from google.protobuf import message

from mbq.pubsub import utils


def _publish(message_type: str, payload: str, topic_arn: str):
    sns = boto3.client("sns")

    sns.publish(
        TargetArn=topic_arn, MessageStructure="json", Message=json.dumps({"default": payload})
    )


def publish_proto(proto: message.Message, topic_arn: str):
    message_type = f"proto.{proto.__module__}.{proto.DESCRIPTOR.name}"
    payload = proto.SerializeToString().decode()
    envelope = utils.Envelope(message_type, payload, utils.PayloadType("proto"), arrow.now())

    _publish(message_type, envelope.dumps(), topic_arn)


def publish_json(message_type: str, data: Union[dict, list, tuple], topic_arn: str):
    payload = json.dumps(data)
    envelope = utils.Envelope(message_type, payload, utils.PayloadType("json"), arrow.now())
    _publish(message_type, envelope.dumps(), topic_arn)
