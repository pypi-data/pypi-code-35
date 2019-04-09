import json
import urllib.parse

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

import boto3
from botocore.exceptions import ClientError
from google.protobuf import text_format

from mbq.pubsub import exceptions, models, utils


def get_name_from_topic_arn(arn):
    if arn:
        return arn.split(":")[-1]


class SNSTopicListFilter(admin.SimpleListFilter):
    title = "topic"
    parameter_name = "topic_arn"

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request).order_by("topic_arn")
        topic_arns = qs.values_list("topic_arn", flat=True).distinct()
        for arn in topic_arns:
            yield (arn, get_name_from_topic_arn(arn))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(topic_arn=self.value())
        return queryset


def replay_messages(model_admin, request, queryset):
    sqs = boto3.client("sqs")
    queue_urls = {}

    for message in queryset:
        if message.queue not in queue_urls:
            url = sqs.get_queue_url(QueueName=utils.construct_full_queue_name(message.queue))
            queue_urls[message.queue] = url["QueueUrl"]

        try:
            sqs.send_message(QueueUrl=queue_urls[message.queue], MessageBody=message.payload)
            message.delete()
        except ClientError as e:
            model_admin.message_user(
                request, f"Message {message.id} failed to replay: {e.response}"
            )


replay_messages.short_description = "Replay messages"


class UndeliverableMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "message_timestamp", "message_type", "queue")

    list_filter = ("message_type", "queue")

    def has_delete_permission(self, *args):
        return True

    def has_add_permission(self, request):
        return False

    def admin_topic(self, message):
        return get_name_from_topic_arn(message.topic_arn)

    admin_topic.short_description = "topic"

    list_display = list_display + ("admin_topic",)
    list_filter = list_filter + (SNSTopicListFilter,)

    def admin_papertrail_link(self, message):
        papertrail_link = settings.PUBSUB.get("PAPERTRAIL_URL")
        if papertrail_link:
            try:
                message_id = json.loads(message.payload)["MessageId"]
                url = f"{papertrail_link}/events?q={message_id}"
                return format_html('<a href="{url}" target="_blank">{text}</a>', url=url, text=url)
            except Exception:
                return (
                    "Failed to generate Papertrail link. "
                    "This likely means this message wasn't published by mbq.pubsub."
                )
        else:
            return "To see a papertrail link, add the 'PAPERTRAIL_URL' setting to your ranch config"

    admin_papertrail_link.short_description = "papertrail"

    def admin_rollbar_query(self, message):
        try:
            message_id = json.loads(message.payload)["MessageId"]
            query = urllib.parse.quote(f"context:pubsub-message-id#{message_id}")
            service = settings.PUBSUB.get("SERVICE")
            url = f"https://rollbar.com/ManagedByQ/{service}/items/?query={query}"
            return format_html('<a href="{url}" target="_blank">{text}</a>', url=url, text=url)
        except Exception:
            return (
                "Failed to generate Rollbar URL. "
                "This likely means this message wasn't published by mbq.pubsub."
            )

    admin_rollbar_query.short_description = "rollbar"

    def admin_payload(self, message):
        try:
            envelope = utils.Envelope.from_undeliverable_message(message)

            if envelope.payload_type is utils.PayloadType.PROTO:
                proto_class = utils.get_proto_from_message_type(envelope.message_type)
                proto = proto_class()
                proto.ParseFromString(envelope.payload.encode())
                payload = text_format.MessageToString(proto, as_utf8=True, indent=4)
            elif envelope.payload_type is utils.PayloadType.JSON:
                payload = json.dumps(envelope.payload, indent=4)
            return format_html("<br/><pre>{}</pre>", payload)

        except exceptions.EnvelopeException:
            return (
                "Failed to parse payload from message envelope. "
                "This likely means this message wasn't published by mbq.pubsub."
            )

    admin_payload.short_description = "payload"

    def admin_message(self, message):
        try:
            payload = json.loads(message.payload)
            data = json.loads(payload["Message"])
            payload["Message"] = data
        except Exception:
            payload = message.payload
        return format_html("<br/><pre>{}</pre>", json.dumps(payload, indent=4))

    admin_message.short_description = "full message"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "created_at",
                    "message_timestamp",
                    "message_type",
                    "admin_payload",
                    "queue",
                    "topic_arn",
                    "admin_papertrail_link",
                    "admin_rollbar_query",
                ),
                "classes": ("wide",),
            },
        ),
        ("Advanced", {"fields": ("admin_message",), "classes": ("wide", "collapse")}),
    )

    readonly_fields = (
        "id",
        "created_at",
        "message_timestamp",
        "message_type",
        "admin_payload",
        "queue",
        "topic_arn",
        "admin_papertrail_link",
        "admin_rollbar_query",
        "admin_message",
    )

    actions = [replay_messages]


admin.site.register(models.UndeliverableMessage, UndeliverableMessageAdmin)
