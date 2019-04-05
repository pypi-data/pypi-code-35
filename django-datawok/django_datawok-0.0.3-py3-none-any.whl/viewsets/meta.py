from rest_framework import viewsets
from datawok.models import Meta
from datawok.serializers import MetaSerializer
from datawok.utils.api_auth import TokenAPIAuthentication


class MetaViewset(viewsets.ModelViewSet):
    model = Meta
    authentication_classes = (TokenAPIAuthentication,)
    permission_classes = []
    pagination_class = None
    serializer_class = MetaSerializer
    queryset = Meta.objects.all()
