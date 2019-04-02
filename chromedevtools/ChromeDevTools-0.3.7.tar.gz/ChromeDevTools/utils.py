import re
from typing import Any, Mapping

__all__ = ('camelize', 'underscore', 'normalize_dict')


def camelize(s: str) -> str:
  return re.sub('_([a-z])', lambda m: m.group(1).upper(), s)


def underscore(s: str) -> str:
  """ Converts CamelCase and kebab-case to under_score """
  return re.sub('([a-z])([A-Z])', r'\1_\2', s).replace('-', '_').lower()


def normalize_dict(d: Mapping[str, Any]) -> Mapping[str, Any]:
  return {
    underscore(k): normalize_dict(v) if isinstance(v, dict) else v
    for k, v in d.items()
  }
