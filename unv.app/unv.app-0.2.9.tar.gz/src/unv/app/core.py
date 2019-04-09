import os
import copy
import importlib

import cerberus

from unv.utils.collections import update_dict_recur


def create_component_settings(
        key: str, default_settings: dict, schema: dict) -> dict:
    """Create and validate application component settings."""
    module_path = os.environ.get('SETTINGS', 'app.settings.development')
    module = importlib.import_module(module_path)

    app_settings = module.SETTINGS
    app_schema = getattr(module, 'SCHEMA', {})

    component_settings = copy.deepcopy(default_settings)
    component_settings = update_dict_recur(
        component_settings, app_settings.get(key, {}))
    component_schema = app_schema.get(key, schema)

    validator = cerberus.Validator(component_schema)
    if not validator.validate(component_settings):
        raise ValueError(f"Error validation settings {validator.errors}")

    return component_settings


def create_settings(settings: dict = None, base_settings: dict = None) -> dict:
    """Create app settings from provided base settings, overrided by env."""
    settings = settings or {}
    if base_settings:
        settings = update_dict_recur(settings, base_settings)
    for key, value in os.environ.items():
        if 'SETTINGS_' not in key:
            continue
        current_settings = settings
        parts = [
            part.lower()
            for part in key.replace('SETTINGS_', '').split('_')
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
