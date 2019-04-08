from datawok.conf import settings
from datawok.generators.views import (
    generate_upload_csv_file_view,
    generate_publish_view,
    generate_detail_view,
)
from datawok.models import datawok_models
from datawok.serializers import datawok_serializers
from datawok.utils.importers import import_class
from datawok.constants import DETAIL_VIEW, UPLOAD_CSV_FILE_VIEW, PUBLISH_VIEW

upload_csv_file_views = []
publish_views = []
detail_views = []

for i, model in enumerate(datawok_models):
    module_paths = settings.MODELS[i]

    # CSV Upload File Views
    upload_csv_file_view = (
        import_class(module_paths[UPLOAD_CSV_FILE_VIEW])
        if isinstance(module_paths, dict)
        and UPLOAD_CSV_FILE_VIEW in module_paths
        else generate_upload_csv_file_view(model)
    )
    upload_csv_file_views.append(upload_csv_file_view)

    # Publish Views
    publish_view = (
        import_class(module_paths[PUBLISH_VIEW])
        if isinstance(module_paths, dict) and PUBLISH_VIEW in module_paths
        else generate_publish_view(model)
    )
    publish_views.append(publish_view)

    # Detail Views
    detail_view = (
        import_class(module_paths[DETAIL_VIEW])
        if isinstance(module_paths, dict) and DETAIL_VIEW in module_paths
        else generate_detail_view(model, datawok_serializers[i])
    )
    detail_views.append(detail_view)
