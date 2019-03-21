from django.apps import apps
from django.conf import settings

from votebase.core.utils.common import generate_slug_for_user


def create_user_profile(user, **attrs):
    # get swappable profile model
    profile_app_label, profile_model_name = settings.AUTH_PROFILE_MODULE.split(".")
    profile_model = apps.get_model(profile_app_label, profile_model_name)

    # create empty profile
    slug = generate_slug_for_user()
    profile = profile_model.objects.create(user=user, slug=slug, **attrs)

    # generate token
    # profile.token = generate_token(user)
    # profile.save(update_fields=['token'])

    # return new profile
    return profile


def get_user_profile(user):
    # get swappable profile model
    profile_app_label, profile_model_name = settings.AUTH_PROFILE_MODULE.split(".")
    profile_model = apps.get_model(profile_app_label, profile_model_name)

    # try to profile
    return profile_model.objects.get(user=user)
