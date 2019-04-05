from rest_framework.response import Response
from rest_framework.views import APIView

from datawok.models import Meta
from datawok.celery import publish_to_aws
from datawok.utils.api_auth import TokenAPIAuthentication


class Publish(APIView):
    """
    View to handle publishing to AWS
    """

    def post(self, request, format=None):
        """
        Publish a model's data.
        """
        model_name = self.model.__name__.lower()

        try:
            meta = Meta.objects.get(datawok_model__model=model_name)
        except Meta.DoesNotExist:
            return Response(
                "No Meta instance for model: {}.".format(model_name), 404
            )

        publish_to_aws.delay(model_name, meta.get_publish_path())

        return Response("OK", 200)


def generate_publish_view(model):
    """
    Dynamically generates a publish view for a given model.
    """
    name = "{}PublishView".format(model.__name__.title())

    return type(
        name,
        (Publish,),
        {"model": model, "authentication_classes": (TokenAPIAuthentication,)},
    )
