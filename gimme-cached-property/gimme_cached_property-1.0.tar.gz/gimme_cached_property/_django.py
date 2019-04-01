try:
    from django.utils.functional import cached_property as cached_property_django
except ImportError:
    cached_property_django = None
