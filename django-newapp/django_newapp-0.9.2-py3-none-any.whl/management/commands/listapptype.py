from newapp.utils import get_app_templates

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Example usage:
    python manage.py listapptemplate
    """
    help = __doc__
    args = '<function arg arg ...>'

    def handle(self, *args, **options):
        """
        Queues the function given with the first argument with the
        parameters given with the rest of the argument list.
        """
        print(get_app_templates())
        