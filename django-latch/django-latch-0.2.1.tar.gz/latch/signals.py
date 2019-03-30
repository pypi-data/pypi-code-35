# pylint: disable=unused-argument
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from latch.models import UserProfile, LatchSetup

@receiver(pre_delete, sender=UserProfile, dispatch_uid="unpair_before_delete")
def unpair_before_delete(sender, **kwargs):
    latch = LatchSetup.instance()
    latch.unpair(kwargs.get('instance').latch_accountId)
