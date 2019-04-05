from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from datawok.utils.api_auth import TokenAPIAuthentication
from datawok.models import Query, Meta
from datawok.serializers import QuerySerializer


class QueryViewset(viewsets.ModelViewSet):
    authentication_classes = (TokenAPIAuthentication,)
    serializer_class = QuerySerializer
    permission_classes = []
    pagination_class = None
    queryset = Query.objects.all()

    def create(self, request):
        data = request.data.copy()

        try:
            data["datawok_model"] = Meta.objects.get(
                datawok_model__model=data["datawok_model"]
            ).datawok_model
        except Meta.DoesNotExist:
            return Response(
                "No Meta instance for model: {}.".format(
                    data["datawok_model"]
                ),
                404,
            )

        try:
            data["creator"] = User.objects.get(username=data["creator"])
        except Meta.DoesNotExist:
            return Response(
                "No user found named: {}.".format(data["creator"]), 404
            )

        q = Query(**data)
        q.save()

        return Response("OK", 200)
