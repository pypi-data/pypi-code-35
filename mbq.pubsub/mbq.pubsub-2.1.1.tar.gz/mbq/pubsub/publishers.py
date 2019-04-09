import json
from typing import Union

import arrow
import boto3
from google.protobuf import message

import mbq.atomiq
from mbq.pubsub import utils


def _publish(payload: dict, topic_arn: str, use_atomiq: bool):
    if use_atomiq:
        mbq.atomiq.sns_publish(topic_arn=topic_arn, payload=payload)
    else:
        sns = boto3.client("sns")
        sns.publish(
            TargetArn=topic_arn, MessageStructure="json", Message=json.dumps({"default": payload})
        )


def publish_proto(proto: message.Message, topic_arn: str, use_atomiq: bool = True):
    message_type = f"proto.{proto.__module__}.{proto.DESCRIPTOR.name}"
    payload = proto.SerializeToString().decode()
    envelope = utils.Envelope(message_type, payload, utils.PayloadType.PROTO, arrow.now())

    _publish(json.dumps(envelope.asdict()), topic_arn, use_atomiq)


def publish_json(
    message_type: str, data: Union[dict, list, tuple], topic_arn: str, use_atomiq: bool = True
):
    payload = json.dumps(data)
    envelope = utils.Envelope(message_type, payload, utils.PayloadType.JSON, arrow.now())

    _publish(json.dumps(envelope.asdict()), topic_arn, use_atomiq)
