from django.conf.urls import url

from .views.rating import RatingCreateView, SkipRatingCreateView


app_name = 'api'


urlpatterns = [
    url(r'^create/$', RatingCreateView.as_view(), name='create'),
    url(r'^skip/$', SkipRatingCreateView.as_view(), name='skip'),
]
