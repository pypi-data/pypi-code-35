import yaml
import json

from os import path
from .common import CachedObj


class File(CachedObj):
    def isexists(self, obj_id):
        if path.exists(obj_id) is False:
            raise FileNotFoundError(f'{obj_id} not found')
        return obj_id


class Yaml(File):
    def default_handler(self, obj_id, **kwargs):
        with open(self.isexists(obj_id), 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)


class Json(File):
    def default_handler(self, obj_id, **kwargs):
        with open(self.isexists(obj_id), 'r') as file:
            return json.load(file)
