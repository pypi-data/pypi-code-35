"""djangoldp_conversation URL Configuration"""
from django.conf.urls import url
from .models import Message, Thread
from djangoldp.views import LDPViewSet


urlpatterns = [
    url(r'^threads/', LDPViewSet.urls(model=Thread, nested_fields=["message_set", "author_user"])),
    url(r'^messages/', LDPViewSet.urls(model=Message, nested_fields=["author_user"])),
]
