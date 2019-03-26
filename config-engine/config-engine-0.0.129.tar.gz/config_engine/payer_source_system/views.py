from rest_framework.generics import ListCreateAPIView

from config_engine.payer_source_system import models
from config_engine.payer_source_system import serializers
from config_engine.payer_source_system import filters


class PayerList(ListCreateAPIView):
    queryset = models.CXPayer.objects.all()
    serializer_class = serializers.CXPayerListCreateSerializer


class ProductList(ListCreateAPIView):
    queryset = models.CXProduct.objects.all()
    serializer_class = serializers.CXProductListCreateSerializer


class CXProductFeatureList(ListCreateAPIView):
    queryset = models.CXProductFeature.objects.all()
    serializer_class = serializers.CXProductFeatureListCreateSerializer
    filter_class = filters.CXProductFeatureFilter

    def get_queryset(self):
        return super().get_queryset()


class PayerSourceSystemList(ListCreateAPIView):
    queryset = models.PayerSourceSystem.objects.all()
    serializer_class = serializers.PayerSourceSystemListCreateSerializer
    filter_class = filters.PayerSourceSystemFilter

    def get_queryset(self):
        return super().get_queryset()
