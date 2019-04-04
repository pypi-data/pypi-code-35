import sys

from django.apps import AppConfig as DjangoAppConfig
from django.core.checks.registry import register
from django.core.management.color import color_style
from edc_utils import get_utcnow

from .address import Address
from .system_checks import edc_base_check


style = color_style()


class AppConfig(DjangoAppConfig):
    name = "edc_base"
    verbose_name = "Edc Base"
    institution = "Institution (see edc_base.AppConfig.institution)"
    project_name = "Project Title (see edc_base.AppConfig.project_name)"
    project_repo = ""
    physical_address = Address()
    postal_address = Address()
    disclaimer = "For research purposes only."
    default_url_name = "home_url"
    copyright = f"2010-{get_utcnow().year}"
    license = "GNU GENERAL PUBLIC LICENSE Version 3"

    def ready(self):
        register(edc_base_check)
        sys.stdout.write(f"Loading {self.verbose_name} ...\n")
        sys.stdout.write("  * For research purposes only.")
        sys.stdout.write(f" Done loading {self.verbose_name}.\n")
