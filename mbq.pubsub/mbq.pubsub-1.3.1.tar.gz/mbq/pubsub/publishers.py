import json

import boto3


sns = boto3.client("sns")


def _publish(message_type, payload, topic_arn):
    sns.publish(
        TargetArn=topic_arn,
        MessageStructure="json",
        Message=json.dumps(
            {"default": json.dumps({"message_type": message_type, "payload": payload})}
        ),
    )


def publish_proto(proto, topic_arn):
    message_type = f"proto.{proto.__module__}.{proto.DESCRIPTOR.name}"
    payload = proto.SerializeToString().decode()

    _publish(message_type, payload, topic_arn)


def publish_json(message_type, payload, topic_arn):
    _publish(message_type, payload, topic_arn)
