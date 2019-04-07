from django.core.management.base import BaseCommand

import os
from importlib import import_module
from django.conf import settings
from django.core.management import call_command
from newapp.utils import get_app_template_path, get_app_templates

APP_TEMPLATES = [ x.get('name') for x in get_app_templates() ]

class Command(BaseCommand):
    """
    Example usage:
    python manage.py newapp mambu --template=lite --appsdir=apps
    """
    help = __doc__
    args = '<function arg arg ...>'

    def check_name_conflick(self, name):
        apps_list = next(os.walk(os.path.join(settings.BASE_DIR, "apps")))[1]
        apps_list = apps_list +['admin', 'admindocs', 'auth' ,'contenttypes' ,'flatpages','gis','humanize',
                            'messages','postgres','redirects','sessions','sitemaps','sites','staticfiles'
                            'syndication']
        if name in apps_list:
            return True
        else:
            try:
                import_module(name)
            except ImportError:
                return False
            else:
                return True

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('--apptype', '-t', dest='apptype', default='lite',
                            help='Application type')
        parser.add_argument('--appdir', '-d', type=str, dest='appdir',  default='/',
                            help='Target directory')

    def handle(self, *args, **options):
        
        name = options['name']
        if self.check_name_conflick(name):
            self.stdout.write(self.style.ERROR("Sorry, but you can't use %s as name because this name already taken" % name))
            exit()

        apps_type = options['apptype']
        if apps_type not in APP_TEMPLATES:
            self.stdout.write(self.style.ERROR("no template with name %s" % apps_type))
            exit()

        if options['appdir'] == "/":
            app_dir = settings.BASE_DIR
            app_path = os.path.join(settings.BASE_DIR, name)
        else:
            app_dir = options['appdir'].strip("/")
            app_path = os.path.join(settings.BASE_DIR, "%s/%s" % (app_dir, name))
        
        if os.path.isdir(app_dir):
            os.mkdir(app_path)
        else:
            self.stdout.write(self.style.ERROR("Appdir %s not found" % app_dir))
            exit()

        template_path = get_app_template_path(apps_type)
        call_command("startapp", name, app_path, template=template_path)
        os.unlink(os.path.join(app_path, "desc.txt"))
        self.stdout.write(self.style.SUCCESS("Congratulation apps %s successfuly created" % name))