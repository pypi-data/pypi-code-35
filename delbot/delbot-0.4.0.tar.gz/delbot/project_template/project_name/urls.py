from django.contrib import admin
from django.urls import path, include
from delbot.blog import urls as blog_urls
from delbot.webhooks import urls as webhook_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(blog_urls)),
    path('wh/', include(webhook_urls)),
]
