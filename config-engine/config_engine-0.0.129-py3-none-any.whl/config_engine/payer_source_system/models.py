from django.db import models

from config_engine.base.models import TimeStampedEntity

from simple_history.models import HistoricalRecords


class CXPayer(TimeStampedEntity):
    name = models.TextField(null=False, unique=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'cx_payer'

    def __str__(self):
        return self.name


class CXProduct(TimeStampedEntity):
    name = models.TextField(null=False, unique=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'cx_product'

    def __str__(self):
        return self.name


class CXProductFeature(TimeStampedEntity):
    product = models.ForeignKey(CXProduct, null=False, on_delete=models.DO_NOTHING)
    master_feature = models.TextField(null=False)
    feature = models.TextField(null=False)
    history = HistoricalRecords(table_name='simplehistory_cx_product_feature')

    class Meta:
        db_table = 'cx_product_feature'
        unique_together = (('master_feature', 'feature'),)

    def __str__(self):
        return str(self.product) + '.' + str(self.master_feature) + '.' + str(self.feature)


class PayerSourceSystem(TimeStampedEntity):
    SYSTEM = 'back_office'
    CONSUMER = 'consumer_facing'
    SOURCE_SYSTEM_TYPE_CHOICES = ((SYSTEM, "back_office"), (CONSUMER, "consumer_facing"))

    MEMBER = 'member'
    BROKER = 'broker'
    LEAD = 'lead'
    EMPLOYEE = 'employee'
    PROVIDER = 'provider'

    SOURCE_SYSTEM_CONSUMER_TYPE_CHOICES = ((MEMBER, "member"), (BROKER, "broker"),
                                           (LEAD, "lead"), (EMPLOYEE, "employee"),
                                           (PROVIDER, "provider"))

    description = models.TextField(null=True)
    source_system_name = models.TextField(null=True, unique=True)
    is_active = models.BooleanField(default=False)
    system_type = models.TextField(null=True, choices=SOURCE_SYSTEM_TYPE_CHOICES)
    consumer_type = models.TextField(null=True, choices=SOURCE_SYSTEM_CONSUMER_TYPE_CHOICES)
    referrer_url = models.TextField(null=True)
    payer = models.ForeignKey(CXPayer, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='payer')
    product = models.ForeignKey(CXProduct, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='product')
    history = HistoricalRecords(table_name='simplehistory_payer_source_system')

    class Meta:
        db_table = 'payer_source_system'

    def __str__(self):
        return self.source_system_name
