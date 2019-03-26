from rest_framework import serializers
from services_shared import exceptions

from config_engine.payer_source_system import models


class CXPayerListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CXPayer
        fields = ('id', 'name', )


class CXProductListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CXProduct
        fields = ('id', 'name', )


class CXProductFeatureListCreateSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(read_only=True, allow_null=False, default=None, slug_field='name')

    class Meta:
        model = models.CXProductFeature
        fields = ('id', 'product', 'feature', 'master_feature')

    def create(self, validated_data):
        try:
            product_data = self.initial_data.pop('product')
        except KeyError:
            raise exceptions.BadRequest

        if product_data:
            product, created = models.CXProduct.objects.get_or_create(name=product_data)
            validated_data['product'] = product

        cx_product_feature, created = models.CXProductFeature.objects.get_or_create(**validated_data)

        return cx_product_feature


class PayerSourceSystemListCreateSerializer(serializers.ModelSerializer):
    payer = serializers.SlugRelatedField(read_only=True, allow_null=True, default=None, slug_field='name')
    product = serializers.SlugRelatedField(read_only=True, allow_null=True, default=None, slug_field='name')

    class Meta:
        model = models.PayerSourceSystem
        fields = ('id', 'description', 'source_system_name', 'is_active', 'system_type', 'consumer_type', 'referrer_url',
                  'payer', 'product', )

    def create(self, validated_data):
        payer_data = None
        product_data = None

        try:
            payer_data = self.initial_data.pop('payer')
        except KeyError:
            pass

        try:
            product_data = self.initial_data.pop('product')
        except KeyError:
            pass

        if payer_data:
            payer, created = models.CXPayer.objects.get_or_create(name=payer_data)
            validated_data['payer'] = payer

        if product_data:
            product, created = models.CXProduct.objects.get_or_create(name=product_data)
            validated_data['product'] = product

        payer_source_system, created = models.PayerSourceSystem.objects.get_or_create(**validated_data)

        return payer_source_system
