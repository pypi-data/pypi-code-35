from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from datawok.utils.api_auth import TokenAPIAuthentication
from datawok.utils.process_input_data import process_input_data
from rest_framework.response import Response

from .serializers import generate_serializer


class Pagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "size"


class DatawokModelViewset(ModelViewSet):
    pagination_class = Pagination

    @action(detail=False, methods=["post"])
    def bulk_create(self, request, pk=None):
        data = request.data

        try:
            model = self.model
            data = process_input_data(model, data)
            model.objects.bulk_create([model(**datum) for datum in data])
        except Exception as e:
            print(e)
            return Response(
                {"msg": "Error reading or decoding CSV.", "error": str(e)},
                status=500,
            )

        return Response({"msg": "success"}, status=200)


def generate_model_viewset(model, serializer=None):
    """
    Dynamically generates a viewset for a given model.
    """
    name = "{}ViewSet".format(model.__name__.title())

    if serializer is None:
        serializer = generate_serializer(model)

    return type(
        name,
        (DatawokModelViewset,),
        {
            "model": model,
            "authentication_classes": (TokenAPIAuthentication,),
            "permission_classes": [],
            "serializer_class": serializer,
            "queryset": model.objects.get_queryset().order_by("pk"),
        },
    )
