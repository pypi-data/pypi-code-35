import re

__all__ = ('camelize', )


def camelize(s: str) -> str:
  return re.sub('_([a-z])', lambda m: m.group(1).upper(), s)
