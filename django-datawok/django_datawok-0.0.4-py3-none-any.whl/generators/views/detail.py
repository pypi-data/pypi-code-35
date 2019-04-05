from django.db.models import Q
from django.shortcuts import get_object_or_404
from datawok.views.base import Base
from datawok.generators.serializers import generate_serializer
from datawok.utils.get_field_type import get_field_type
from datawok.models import Query
from datawok.serializers import QuerySerializer
from datawok.models import Meta
from datawok.conf import settings


class Detail(Base):
    template_name = "datawok/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        fields = {}
        for field in self.model._meta.get_fields():
            field_type = get_field_type(field)
            fields[str(field.name)] = field_type
        context["fields"] = Base.prep_data_for_injection(fields)

        context["queries"] = Base.prep_data_for_injection(
            Query.objects.filter(
                Q(datawok_model__model=self.model.__name__.lower())
            ),
            QuerySerializer,
            many=True,
        )

        context["model"] = self.model.__name__.lower()

        meta = get_object_or_404(Meta, datawok_model__model=context["model"])
        context["meta_pk"] = meta.pk

        context["query_limit"] = settings.QUERY_LIMIT

        return context


def generate_detail_view(model, serializer=None):
    """
    Dynamically generates a detail view for a given model.
    """
    name = "{}DetailView".format(model.__name__.title())

    if serializer is None:
        serializer = generate_serializer(model)

    return type(name, (Detail,), {"model": model, "serializer": serializer})
