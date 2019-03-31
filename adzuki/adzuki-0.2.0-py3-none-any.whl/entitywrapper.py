from datetime import datetime
from . import utils
import copy

class EntityWrapper(object):
  @staticmethod
  def from_iterator(model, entities, projection=None):
    for entity in entities:
      yield EntityWrapper(model, entity, projection)

  def __init__(self, model, entity, projection=None):
    self._model = model
    self._entity = entity
    self._projection = projection

  def __getitem__(self, key):
    return self.get(key, None)

  def get(self, key, default=None):
    if self._projection is None or key in self._projection:
      return self._entity.get(key, default)
    else:
      return default

  def __setitem__(self, key, value):
    if self._projection is not None:
      raise ValueError('Updating a projected entitiy is not allowed.')
    else:
      self._entity[key] = value

  def __contains__(self, key):
    return key in self._entity

  def __delitem__(self, key):
    if self._projection is None or key in self._projection:
      del self._entity[key]

  def __eq__(self, other):
    if isinstance(other, EntityWrapper):
      if self.key.id_or_name != None:
        return self.key.id_or_name == other.key.id_or_name
    else:
      return self._entity == other

  def __hash__(self):
    if self.key.id_or_name != None:
      return self.key.id_or_name.__hash__()
    else:
      return NotImplemented

  @property
  def __dict__(self):
    dictionary = dict(self._entity)
    jsonifiable_dictionary = { 'id': self.key.id_or_name }
    for key, value in dictionary.items():
      if self._projection is None or key in self._projection:
        if isinstance(value, bytes):
          jsonifiable_dictionary[key] = value.decode('utf-8')
        else:
          jsonifiable_dictionary[key] = value
    return jsonifiable_dictionary

  @property
  def id(self):
    return self._entity.key.id_or_name

  @property
  def key(self):
    return self._entity.key

  @property
  def kind(self):
    return self._entity.kind

  def is_valid(self):
    return self._model._schema_validator.is_valid(utils.entity2dict(self._entity))

  def put(self):
    if self._projection is not None:
      raise ValueError('Updating a projected entitiy is not allowed.')
    else:
      self._model._schema_validator.validate(utils.entity2dict(self._entity))
      return self._model._client.put(self._entity)

  def delete(self):
    if self._projection is not None:
      raise ValueError('Updating a projected entitiy is not allowed.')
    else:
      self._entity['deleted_at'] = datetime.now()
      return self._model.put(self._entity)
