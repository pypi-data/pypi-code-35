# import logging
#
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter
# from rest_framework.generics import ListCreateAPIView
#
# # from config_engine.semantic_key_registry.filters import (
# #     SemanticKeyFilter,
# #     ConsumerDataAttributeFilter,
# # )
# from config_engine.semantic_key_registry import models
# # from config_engine.semantic_key_registry.serializers import (
# #     SemanticKeySerializer,
# #     ConsumerDataAttributeSerializer,
# # )
#
# logger = logging.getLogger(__name__)
#
#
# class CXSemanticEventKeyList(ListCreateAPIView):
#     """
#     Endpoint for getting, creating a list of SemanticKeys
#     """
#     model = models.CXSemanticEventKey
#     queryset = models.CXSemanticEventKey.objects.all()
#     serializer_class = CXSemanticEventKeySerializer
#     filter_backends = (DjangoFilterBackend,
#                        SearchFilter,
#                        )
#     filter_class = CXSemanticEventKeyFilter
#     search_fields = ('semantic_key', 'display_name', 'description', 'why_captured')
#
#
# class CXSemanticDataKeyList(ListCreateAPIView):
#     """
#     Endpoint for getting, creating a list of SemanticKeys
#     """
#     model = models.CXSemanticDataKey
#     queryset = models.CXSemanticDataKey.objects.all()
#     serializer_class = CXSemanticDataKeySerializer
#     filter_backends = (DjangoFilterBackend,
#                        SearchFilter,
#                        )
#     filter_class = CXSemanticDataKeyFilter
#     search_fields = ('semantic_key', 'display_name', 'description')
#
#
# class SemanticKeyDetail(GenericDetailView):
#     """
#     Detail endpoint to retrieve, update or delete a SemanticKey instance.
#     """
#     queryset = CXSemanticKey.objects.all()
#     serializer_class = SemanticKeySerializer
#
#
# class ConsumerDataAttributeList(GenericListView):
#     """
#     List endpoint for getting, creating a list of ConsumerDataAttributes
#     """
#     queryset = PayerConsumerDataAttribute.objects.all()
#     serializer_class = ConsumerDataAttributeSerializer
#     filter_class = ConsumerDataAttributeFilter
#
#     def get_queryset(self):
#         payer = self.request.META.get("X-ZPR-TENANT-NAME", self.request.tenant_name).lower()
#         logger.debug("payer is : {}".format(payer))
#         queryset = super().get_queryset()
#         if payer != 'internal':
#             queryset = queryset.filter(configuration__payer__internal_name__icontains=payer)
#         return queryset
#
#
# class ConsumerDataAttributeDetail(GenericDetailView):
#     """
#     Detail endpoint to retrieve, update or delete a ConsumerDataAttribute
#     instance.
#     """
#     queryset = PayerConsumerDataAttribute.objects.all()
#     serializer_class = ConsumerDataAttributeSerializer
#
#     def get_queryset(self):
#         payer = self.request.META.get("X-ZPR-TENANT-NAME", self.request.tenant_name).lower()
#         logger.debug("payer is : {}".format(payer))
#         queryset = super().get_queryset()
#         if payer != 'internal':
#             queryset = queryset.filter(configuration__payer__internal_name__icontains=payer)
#         return queryset
