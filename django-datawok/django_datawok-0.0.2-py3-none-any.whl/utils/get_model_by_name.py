from datawok.models import datawok_models


def get_model_by_name(name):
    for model in datawok_models:
        if model.__name__.lower() == name.lower():
            return model

    return None
