from django_auth_ldap.backend import populate_user
from django.conf import settings
from django.contrib.auth.models import Group


def populate_user_signal_handler(user, ldap_user, **kwargs):
    # Converts the user to an LDAP user
    user.set_unusable_password()

    # If the user can login via LDAP, they can have editor permissions
    if 'wagtail.core' in settings.INSTALLED_APPS\
        or 'wagtailcore' in settings.INSTALLED_APPS:
        user.save()
        editors = Group.objects.get(name="Editors")
        moderators = Group.objects.get(name="Moderators") 
        user.groups.add(editors)
        user.groups.add(moderators)

def register_signal_handlers():
    populate_user.connect(populate_user_signal_handler)
