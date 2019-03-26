from django.conf.urls import include
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="Configuration Engine API",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path(r'admin/', admin.site.urls),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('source-system/', include('config_engine.payer_source_system.urls'), name='source-system'),
    #path('semantic-key-registry/', include('config_engine.semantic_key_registry.urls'), name='semantic-key-registry'),

]
