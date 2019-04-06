from hs_infra.entities.base.base_entity import BaseModel
from hs_infra.meta_classes.singleton_meta_class import Singleton


class BaseDal(metaclass=Singleton):
    """this would be useful for object oriented programing patterns..."""
    # over ride model for gain its functionality
    model = BaseModel

    def create_new(self, **kwargs):
        new_instance = self.model.objects.create(**kwargs)
        return new_instance

    def get_by_id(self, obj_id):
        qs = self.model.objects.get(id=obj_id)
        return qs

    def find_by_id(self, obj_id):
        qs = self.model.objects.filter(id=obj_id)
        if qs.exists():
            return qs[0]
        else:
            return None

    def find_by_kwargs(self, **kwargs):
        qs = self.model.objects.filter(kwargs)
        return qs
