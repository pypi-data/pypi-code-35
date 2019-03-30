# pylint: disable=invalid-name
from django.urls import path
from latch import views

urlpatterns = [
    path("pair/", views.pair, name="latch_pair"),
    path("unpair/", views.unpair, name="latch_unpair"),
    path("status/", views.status, name="latch_status"),
]
