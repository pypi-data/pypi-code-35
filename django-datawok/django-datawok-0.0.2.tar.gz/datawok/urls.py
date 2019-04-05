from django.urls import include, path
from rest_framework import routers

from datawok.models import datawok_models
from datawok.views import (
    SQL,
    List,
    upload_csv_file_views,
    publish_views,
    detail_views,
)
from datawok.viewsets import datawok_viewsets, MetaViewset, QueryViewset

router = routers.DefaultRouter()

urlpatterns = [
    path("", List.as_view(), name="datawok-list"),
    path("api/sql/", SQL.as_view(), name="datawok-sql"),
]

router.register(r"meta", MetaViewset)
router.register(r"query", QueryViewset)

for i, model in enumerate(datawok_models):
    name = model.__name__.lower()
    # Model viewsets
    router.register(
        r"{}".format(name),
        datawok_viewsets[i],
        base_name="datawok-{}".format(name),
    )

    # CSV file upload views
    urlpatterns += [
        path(
            r"api/{}/upload/csv/file/".format(name),
            upload_csv_file_views[i].as_view(),
            name="datawok-upload-csv-file-{}".format(name),
        )
    ]

    # Publish views
    urlpatterns += [
        path(
            r"api/{}/publish/".format(name),
            publish_views[i].as_view(),
            name="datawok-publish-{}".format(name),
        )
    ]

    # Detail views
    urlpatterns += [
        path(
            r"{}/".format(name),
            detail_views[i].as_view(),
            name="datawok-detail-{}".format(name),
        )
    ]

urlpatterns += [path("api/", include(router.urls))]
