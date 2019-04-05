from datawok.conf import settings
from datawok.generators.viewsets import generate_model_viewset
from datawok.models import datawok_models
from datawok.serializers import datawok_serializers
from datawok.utils.importers import import_class
from datawok.constants import VIEWSET

viewsets = []

for i, model in enumerate(datawok_models):
    module_paths = settings.MODELS[i]

    viewset = (
        import_class(module_paths[VIEWSET])
        if isinstance(module_paths, dict) and VIEWSET in module_paths
        else generate_model_viewset(model, datawok_serializers[i])
    )

    viewsets.append(viewset)
