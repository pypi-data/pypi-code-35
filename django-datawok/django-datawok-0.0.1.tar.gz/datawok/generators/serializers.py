from rest_framework import serializers


def generate_serializer(model):
    """
    Dynamically generates a viewset for a given model.
    """
    name = "{}Serializer".format(model.__name__.title())

    meta = type("Meta", (), {"model": model, "fields": "__all__"})

    return type(name, (serializers.ModelSerializer,), {"Meta": meta})
