from __future__ import absolute_import

from django.conf.urls import url

from tests.contrib.django.fixtures.testapp.views import exception, index


urlpatterns = (
    url(r"^index$", index, name="index"),
    url(r"^exception$", exception, name="exception"),
)
