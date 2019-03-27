from django.conf.urls import url

from .views import custom_data

app_name = 'dseo'

urlpatterns = [
    url(r'(?P<slug>[\w\.-]+)', custom_data, name='custom_data'),
]
