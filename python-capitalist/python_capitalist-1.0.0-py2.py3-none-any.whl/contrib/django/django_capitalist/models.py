from django.db import models
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
