from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import iHelaProvider

# https://raphaelyancey.fr/en/2018/05/28/setting-up-django-oauth2-server-client.html

urlpatterns = default_urlpatterns(iHelaProvider)
