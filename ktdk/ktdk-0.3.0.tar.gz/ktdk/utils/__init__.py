import io
import logging
from pathlib import Path
from typing import Dict, Optional, Union

import yaml

from .flatters import flatten_all_tasks, flatten_tasks, flatten_tests
from .naming import normalize_name, unique_name

log = logging.getLogger(__name__)


def parse_yaml_config(file_path: Path) -> Optional[Dict]:
    """Loads the YAML file from the defined path
    Args:
        file_path: File path from which the YAML file should be loaded

    Returns(Dictionary): loaded yaml

    """
    file_path = Path(file_path)
    if not file_path.exists():
        log.warning(f"[YAML] Cannot load file - not exists: {file_path}")
        return {}
    with file_path.open('r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            # TODO Throw an exception
            log.error(f"[PARSE] Error for {file_path}: {exc}")
    return {}


def save_yaml(file_path, config):
    """Saves the config to the config file
    Args:
        file_path: YAML file path
        config: Configuration holder

    """
    file_path = Path(file_path)
    with file_path.open('w') as stream:
        try:
            yaml.safe_dump(config, stream, default_flow_style=False)
        except yaml.YAMLError as exc:
            # TODO Throw an exception
            log.error(f"[SAVE] Error: {exc}")


def universal_reader(input: Union['Path', 'io.TextIOBase', 'str']) -> str:
    content = input
    if isinstance(input, Path):
        content = Path(input).read_text(encoding='utf-8')
    if isinstance(input, io.TextIOBase):
        content = input.read()
    return content


def dig_class(obj, *selector):
    current = obj
    for sel in selector:
        current = getattr(current, sel)
        if not current:
            return None
    return current
