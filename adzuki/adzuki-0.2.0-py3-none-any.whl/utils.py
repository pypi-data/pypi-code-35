from google.cloud.datastore.entity import Entity

def entity2dict(subject):
  if isinstance(subject, Entity):
    dictioniarized = dict(subject)
    return { k: entity2dict(v) for k, v in dictioniarized.items() }
  elif isinstance(subject, list):
    return [ entity2dict(v) for v in subject ]
  else:
    return subject
