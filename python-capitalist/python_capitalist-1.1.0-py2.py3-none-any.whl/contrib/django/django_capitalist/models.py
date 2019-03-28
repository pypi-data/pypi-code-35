from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    code = models.CharField(_('ISO code'), max_length=3, unique=True)

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __str__(self):
        return self.code


# TODO
# class Rate(models.Model):
#     source = models.ForeignKey(Currency, models.CASCADE, verbose_name=_('source currency'), related_name='source_rates')
#     target = models.ForeignKey(Currency, models.CASCADE, verbose_name=_('target currency'), related_name='target_rates')


class Account(models.Model):
    number = models.CharField(_('unique number'), max_length=15, unique=True)
    name = models.CharField(_('name'), max_length=255)
    balance = models.DecimalField(_('balance'), max_digits=15, decimal_places=2)
    blocked_amount = models.DecimalField(_('blocked amount'), max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, models.CASCADE, verbose_name=_('currency'))

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return '{} ({})'.format(self.name, self.number)


class Batch(models.Model):
    batch_id = models.CharField(_('batch ID'), max_length=50, unique=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Not required. Just for your convenience.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('batch')
        verbose_name_plural = _('batches')

    def __str__(self):
        return 'Batch {}'.format(self.batch_id)


class BatchRecord(models.Model):
    NEW = 'NEW'
    READY = 'READY'
    INPROCESS = 'INPROCESS'
    DECLINED = 'DECLINED'
    PROCESSED = 'PROCESSED'

    STATE_CHOICES = (
        (NEW, _('New')),
        (READY, _('Ready')),
        (INPROCESS, _('In process')),
        (DECLINED, _('Declined')),
        (PROCESSED, _('Processed')),
    )

    batch = models.ForeignKey(Batch, models.CASCADE, verbose_name=_('batch'))
    state = models.CharField(_('status'), max_length=20, choices=STATE_CHOICES, default=NEW)
    data = models.TextField(_('record data (CSV)'))
    internal_id = models.CharField(_('internal ID'), max_length=255)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Not required. Just for your convenience.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('batch record')
        verbose_name_plural = _('batch records')
        unique_together = [
            ['batch', 'internal_id'],
        ]
