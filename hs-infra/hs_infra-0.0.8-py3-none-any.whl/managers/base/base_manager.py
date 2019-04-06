from hs_infra.entities.base.base_entity import BaseModel


class BaseManager:
    model = BaseModel

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
