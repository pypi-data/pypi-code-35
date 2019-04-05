import json
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from datawok.conf import settings as app_settings
from datawok.utils.auth import secure


@secure
class Base(TemplateView):
    @staticmethod
    def prep_data_for_injection(queryset, serializer=None, many=False):
        if serializer:
            data = serializer(queryset, many=many).data
        else:
            data = queryset

        return json.dumps(json.dumps(data, cls=DjangoJSONEncoder))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["API_TOKEN"] = app_settings.SECRET_KEY
        context["AWS_PUBLIC_ROOT"] = app_settings.AWS_PUBLIC_ROOT
        context["APP_ROOT"] = app_settings.APP_ROOT
        context["API_ROOT"] = reverse_lazy("api-root")

        return context
