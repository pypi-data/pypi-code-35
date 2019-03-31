from datetime import datetime

class EntityWrapper(object):
  @staticmethod
  def from_iterator(model, entities, projection=None):
    for entity in entities:
      yield EntityWrapper(model, entity, projection)

  @staticmethod
  def type_match(given_type, value):
    if isinstance(given_type, list):
      if value in given_type:
        return value
      else:
        raise TypeError('%s is not a member of enumerate set %s' % (value, str(given_type)))
    elif isinstance(given_type, dict):
      def nested_type_match(key_and_type):
        key, new_given_type = key_and_type
        return EntityWrapper.type_match(new_given_type, value[key])
      if list(map(nested_type_match, given_type.items())):
        return value
    elif isinstance(given_type, type):
      if type(value) == given_type and isinstance(value, datetime):
        return value
      else:
        return given_type(value)
    else:
      raise ValueError('Unable to perform type matching for \'%s\'.' % str(given_type))

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
    attributes = self._model.attributes
    if self._projection is not None:
      raise ValueError('Updating a projected entitiy is not allowed.')
    elif key in self:
      given_type = attributes[key]
      self._entity[key] = EntityWrapper.type_match(given_type, value)
    else:
      raise AttributeError('Attribute[%s] is not existed in model.' % key)

  def __contains__(self, key):
    return key in self._model.attributes and (self._projection is None or key in self._projection)

  def __delitem__(self, key):
    if self._projection is None or key in self._projection:
      del self._entity[key]

  def __eq__(self, other):
    if isinstance(other, EntityWrapper):
      if self.key.name != None:
        return self.key.name == other.key.name
      elif self.key.id != None:
        return self.key.id == other.key.id
    else:
      return self._entity == other

  def __hash__(self):
    if self.key.name != None:
      return self.key.name.__hash__()
    elif self.key.id != None:
      return self.key.name.__hash__()
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

  def put(self):
    if self._projection is not None:
      raise ValueError('Updating a projected entitiy is not allowed.')
    else:
      return self._model.put(self._entity)

  def delete(self):
    if self._projection is not None:
      raise ValueError('Updating a projected entitiy is not allowed.')
    else:
      self._entity['deleted_at'] = datetime.now()
      return self._model.put(self._entity)
