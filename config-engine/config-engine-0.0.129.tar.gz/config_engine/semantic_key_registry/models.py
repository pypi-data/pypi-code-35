from django.db import models
from simple_history.models import HistoricalRecords

from config_engine.base.models import (
    TimeStampedEntity,
)
from config_engine.payer_source_system.models import (
    PayerSourceSystem,
    CXProductFeature
)

STRING = 'string'
NUMERIC = 'numeric'
DATE = 'date'
DATETIME = 'datetime'
OBJECT = 'object'
LIST = 'list'
DECIMAL = 'decimal'
BOOLEAN = 'boolean'
KEY_VALUE_TYPE_CHOICES = ((STRING, "string"), (NUMERIC, "numeric"), (DATE, "date"),
                   (DATETIME, "datetime"), (OBJECT, "object"), (LIST, "list"),
                   (DECIMAL, "decimal"), (BOOLEAN, "boolean"), )


class CXSemanticEventKey(TimeStampedEntity):
    semantic_key = models.TextField(unique=True)
    display_name = models.TextField()
    description = models.TextField()
    why_captured = models.TextField()
    feature = models.ForeignKey(CXProductFeature, on_delete=models.DO_NOTHING, null=True)
    is_primary_feature_key = models.BooleanField()
    event_object = models.TextField()
    event_action = models.TextField()
    history = HistoricalRecords(table_name='simplehistory_cx_semantic_event_key')

    class Meta:
        db_table = 'cx_semantic_event_key'


class CXSemanticDataKey(TimeStampedEntity):
    semantic_key = models.TextField(unique=True)
    display_name = models.TextField()
    description = models.TextField()
    key_value_type = models.TextField(null=False, choices=KEY_VALUE_TYPE_CHOICES)
    history = HistoricalRecords(table_name='simplehistory_cx_semantic_data_key')

    class Meta:
        db_table = 'cx_semantic_data_key'


class PayerConsumerDataKey(TimeStampedEntity):
    semantic_data_key = models.ForeignKey(CXSemanticDataKey, on_delete=models.DO_NOTHING)
    key_value_type = models.TextField(null=False, choices=KEY_VALUE_TYPE_CHOICES)
    configuration = models.ForeignKey(PayerSourceSystem, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField
    history = HistoricalRecords(table_name='simplehistory_payer_consumer_data_key')

    class Meta:
        db_table = 'payer_consumer_data_key'
        unique_together = (('semantic_data_key', 'configuration'),)


class PayerConsumerEventKey(TimeStampedEntity):
    semantic_event_key = models.ForeignKey(CXSemanticEventKey, on_delete=models.DO_NOTHING)
    configuration = models.ForeignKey(PayerSourceSystem, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField
    history = HistoricalRecords(table_name='simplehistory_payer_consumer_event_key')

    class Meta:
        db_table = 'payer_consumer_event_key'
        unique_together = (('semantic_event_key', 'configuration'),)


class PayerConsumerEventDataKey(TimeStampedEntity):
    semantic_event_key = models.ForeignKey(CXSemanticEventKey, on_delete=models.DO_NOTHING)
    key_value_type = models.TextField(null=False, choices=KEY_VALUE_TYPE_CHOICES)
    configuration = models.ForeignKey(PayerSourceSystem, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField
    history = HistoricalRecords(table_name='simplehistory_payer_consumer_event_data_key')

    class Meta:
        db_table = 'payer_consumer_event_data_key'
        unique_together = (('semantic_event_key', 'configuration'),)
