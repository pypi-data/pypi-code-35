import itertools

import logging
import yaml
from contextlib import contextmanager
from pathlib import Path
from typing import Union, List, Iterable

log = logging.getLogger(__name__)

# items with lower index take precedence
_loaded_dicts: List[dict] = []
_override_dicts: List[dict] = []

_NON_EXISTING = object()  # Sentinel
DELETED = object()  # Sentinel


class GConfError(Exception):
	pass


def load(*configs: Union[Path, str], required=True) -> List[Path]:
	paths = [Path(config) for config in configs]

	non_existing = [p for p in paths if not p.exists()]
	if required and non_existing:
		raise FileNotFoundError(f'One or more config files not found: {", ".join(map(str, non_existing))}')

	existing = [p for p in paths if p.exists()]
	global _loaded_dicts
	for p in existing:
		with open(p) as c:
			log.debug(f'Loading config from {p}')
			_loaded_dicts.insert(0, yaml.safe_load(c))

	return existing


def load_first(*configs: Union[Path, str], required=True) -> Path:
	paths = [Path(config) for config in configs]

	for p in paths:
		if p.exists():
			if not p.is_file():
				raise FileNotFoundError(f'{p} is not a file')

			loaded = load(p, required=False)
			if loaded:
				return loaded[0]

	if required:
		raise FileNotFoundError(f'No config file found in {", ".join(map(str, paths))}')


def add(dict_: dict):
	global _loaded_dicts
	_loaded_dicts.insert(0, dict_)


@contextmanager
def override_conf(dict_: dict):
	global _override_dicts
	_override_dicts.insert(0, dict_)
	try:
		yield
	finally:
		_override_dicts.pop(0)


def reset():
	global _loaded_dicts, _override_dicts
	_loaded_dicts = []
	_override_dicts = []


def get(*args: str, default=None):
	split_args = list(itertools.chain(*[a.split('.') for a in args]))
	for d in itertools.chain(_override_dicts, _loaded_dicts):
		result = _get_single(split_args, d)
		if result is DELETED:
			break
		if result is not _NON_EXISTING:
			return result
	if default:
		return default
	raise GConfError(f'Key not found: {".".join(split_args)}')


def _get_single(split_args: Iterable[str], dict_: dict):
	current_value: Union[list, dict] = dict_
	for search_term in split_args:

		if isinstance(current_value, list):
			try:
				i = int(search_term)
			except ValueError as e:
				raise GConfError(f'Found a list but {search_term} is not a list index') from e
			try:
				current_value = current_value[i]
			except IndexError:
				return _NON_EXISTING

		elif isinstance(current_value, dict):
			try:
				current_value = current_value[search_term]
			except KeyError:
				return _NON_EXISTING

		else:
			raise GConfError(f'Invalid type in config: {type(current_value)}')

	return current_value
