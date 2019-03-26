import django_filters

from config_engine.payer_source_system import models


class PayerSourceSystemFilter(django_filters.FilterSet):
    payer = django_filters.rest_framework.filters.CharFilter(
        field_name="payer__name",
        label="payer",
        lookup_expr="iexact"
    )

    product = django_filters.rest_framework.filters.CharFilter(
        field_name="product__name",
        label="product",
        lookup_expr="iexact"
    )

    source_system_name = django_filters.rest_framework.filters.CharFilter(
        field_name="source_system_name",
        label="source_system_name",
        lookup_expr="iexact"
    )

    referrer_url = django_filters.rest_framework.filters.CharFilter(
        field_name="referrer_url",
        label="referrer_url",
        lookup_expr="iexact"
    )

    is_active = django_filters.rest_framework.filters.BooleanFilter(
        field_name="is_active",
        label="is_active"
    )

    consumer_type = django_filters.rest_framework.filters.CharFilter(
        field_name="consumer_type",
        label="consumer_type",
        lookup_expr="iexact"
    )

    system_type = django_filters.rest_framework.filters.CharFilter(
        field_name="system_type",
        label="system_type",
        lookup_expr="iexact"
    )

    class Meta:
        model = models.PayerSourceSystem
        fields = {}


class CXProductFeatureFilter(django_filters.FilterSet):
    product = django_filters.rest_framework.filters.CharFilter(
        field_name="product__name",
        label="product",
        lookup_expr="iexact"
    )

    master_feature = django_filters.rest_framework.filters.CharFilter(
        field_name="master_feature",
        label="master_feature",
        lookup_expr="iexact"
    )

    feature = django_filters.rest_framework.filters.CharFilter(
        field_name="feature",
        label="feature",
        lookup_expr="iexact"
    )

    class Meta:
        model = models.CXProductFeature
        fields = {}
