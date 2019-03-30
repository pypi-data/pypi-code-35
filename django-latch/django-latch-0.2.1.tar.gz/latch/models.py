from django.db import models
from django.conf import settings

from latch.latch_sdk_python import Latch


class LatchSetup(models.Model):
    latch_appid = models.CharField(max_length=256, null=False, unique=True)
    latch_secret = models.CharField(max_length=128, null=False, unique=True)

    def __str__(self):
        return "Latch Setup"

    class Meta:
        verbose_name_plural = "Latch Setup"

    @classmethod
    def instance(cls):
        """
        Returns an instance of Latch API :class:`latch.latch_sdk_python.Latch` object for the current
        configuration
        """
        if not LatchSetup.objects.exists():
            return None

        setup = LatchSetup.objects.first()
        return Latch(setup.latch_appid, setup.latch_secret)

    @classmethod
    def appid(cls):
        """
        Returns the configured application identifier
        """
        if not LatchSetup.objects.exists():
            return None
        setup = LatchSetup.objects.first()
        return setup.latch_appid


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latch_accountId = models.CharField(
        max_length=128, default="", null=True, blank=True
    )

    def __str__(self):
        return "Latch UserProfile {}".format(self.user)

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    @classmethod
    def accountid(cls, user):
        try:
            acc_id = user.userprofile.latch_accountId
            return acc_id
        except Exception as e:
            return None

    @classmethod
    def get_or_create_profile(cls, user):
        profile = None
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        return profile

    @classmethod
    def save_user_accountid(cls, user, acc_id):
        profile = UserProfile.get_or_create_profile(user)
        profile.latch_accountId = acc_id
        profile.save()

    @classmethod
    def delete_user_account_id(cls, acc_id):
        try:
            UserProfile.objects.get(latch_accountId=acc_id).delete()
            return True
        except UserProfile.DoesNotExist:
            return None
