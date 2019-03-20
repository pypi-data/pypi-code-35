from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


def create_facebook_profile(sender, instance, created, **kwargs):
    if created:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        model = models.get_model(app_label, model_name)
        model.objects.create(
            user=instance,
            slug=instance.pk,
        )

post_save.connect(create_facebook_profile, sender=User)
