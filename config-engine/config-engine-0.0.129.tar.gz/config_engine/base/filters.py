import django_filters

class CharInFilter(django_filters.BaseInFilter,
                   django_filters.rest_framework.CharFilter):
    """ allows using the 'in' lookup_expr with related fields"""
    pass
