from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import autodiscover
from .views import ReceiverView, RequestListView


autodiscover()
urlpatterns = (
    path(
        '<slug:source_slug>/',
        csrf_exempt(ReceiverView.as_view()),
        name='webhook_receiver'
    ),
    path(
        '<slug:source_slug>/log/',
        RequestListView.as_view(),
        name='webhook_log'
    ),
)
