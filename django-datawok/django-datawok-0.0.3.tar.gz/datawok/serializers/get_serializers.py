from datawok.conf import settings
from datawok.generators.serializers import generate_serializer
from datawok.models import datawok_models
from datawok.utils.importers import import_class
from datawok.constants import SERIALIZER, PUBLISH_SERIALIZER

serializers = []
publish_serializers = []

for i, model in enumerate(datawok_models):
    module_paths = settings.MODELS[i]

    serializer = (
        import_class(module_paths[SERIALIZER])
        if isinstance(module_paths, dict) and SERIALIZER in module_paths
        else generate_serializer(model)
    )

    serializers.append(serializer)

    publish_serializer = (
        import_class(module_paths[PUBLISH_SERIALIZER])
        if isinstance(module_paths, dict)
        and PUBLISH_SERIALIZER in module_paths
        else generate_serializer(model)
    )
    publish_serializers.append(publish_serializer)
