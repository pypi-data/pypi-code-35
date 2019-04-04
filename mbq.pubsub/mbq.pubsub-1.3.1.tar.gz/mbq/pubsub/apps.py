from django.apps import AppConfig

from mbq import metrics
from mbq.pubsub.settings import project_settings


class PubSubConfig(AppConfig):
    name = "mbq.pubsub"
    verbose_name = "PubSub"

    def ready(self):
        from . import publishers

        self.module._collector = metrics.Collector(
            namespace="mbq.pubsub",
            tags={"env": project_settings.ENV.long_name, "service": project_settings.SERVICE},
        )

        self.module.publish_proto = publishers.publish_proto
        self.module.publish_json = publishers.publish_json
