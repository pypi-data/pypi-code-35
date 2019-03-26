
from django.conf.urls import url, include


app_name = 'ratings'


urlpatterns = [
    url(r'^api/', include('ratings.api.urls', namespace='api')),
]
