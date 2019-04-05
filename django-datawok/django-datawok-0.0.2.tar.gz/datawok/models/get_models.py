from datawok.conf import settings
from datawok.utils.importers import import_class
from datawok.constants import MODEL

models = []

for module_paths in settings.MODELS:
    model = (
        import_class(module_paths[MODEL])
        if isinstance(module_paths, dict) and MODEL in module_paths
        else import_class(module_paths)
    )

    models.append(model)
