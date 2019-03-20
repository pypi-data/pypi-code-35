import os
import copy
import importlib

import jsonschema

from unv.utils.collections import update_dict_recur


def create_component_settings(
        key: str, default_settings: dict, schema: dict) -> dict:
    """Create and validate application component settings."""
    module_path = os.environ.get('SETTINGS', 'app.settings.development')
    module = importlib.import_module(module_path)
    app_settings = module.SETTINGS
    settings = copy.deepcopy(default_settings)

    if key in app_settings:
        settings = update_dict_recur(settings, app_settings[key])

    validator = jsonschema.Draft4Validator(schema)
    validator.validate(settings)

    return settings


def create_settings(settings: dict = None) -> dict:
    """Create app settings from provided base settings, overrided by env."""
    settings = settings or {}
    for key, value in os.environ.items():
        if 'OVERRIDE_SETTINGS_' not in key:
            continue
        current_settings = settings
        parts = [
            part.lower()
            for part in key.replace('OVERRIDE_SETTINGS_', '').split('_')
        ]
        last_index = len(parts) - 1
        for index, part in enumerate(parts):
            if index == last_index:
                if value == 'False':
                    value = False
                elif value == 'True':
                    value = True
                elif value.isdigit():
                    value = int(value)
                current_settings[part] = value
            else:
                current_settings = current_settings.setdefault(part, {})

    return settings
