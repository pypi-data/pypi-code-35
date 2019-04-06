from isort import SortImports
from setupy.help import HELP_SECTION


def serialize(setup, include_help=False):
    imports = serialize_imports(setup)
    features = serialize_features(setup)
    settings, setting_names = serialize_settings(setup)

    setup_line = f"setup(**merge({setting_names}))"
    help_section = HELP_SECTION if include_help else ""

    return f"{imports}\n\n{features}\n\n{settings}\n\n{help_section}\n\n{setup_line}"


def serialize_imports(setup):
    return SortImports(file_contents="\n".join(setup.imports)).output


def serialize_features(setup):
    return "\n\n".join(f.code for f in setup.features)


def serialize_settings(setup):
    settings = setup.settings

    settings_as_dictionaries = (to_dictionary(s) for s in settings)

    serialized_settings = "\n\n".join(settings_as_dictionaries)
    setting_names = ", ".join(s.name for s in settings)

    return (f"{serialized_settings}", setting_names)


def to_dictionary(setting):
    name = setting.name
    dictionary = pretty(setting.properties)
    return f"{name} = {{\n{dictionary}\n}}"


def pretty(d, indent=1):
    result = []
    for key, value in d.items():
        tabs = " " * indent * 4
        formatted_value = value
        if isinstance(formatted_value, dict):
            prettified = pretty(value, indent + 1)
            formatted_value = f'{{\n{prettified}\n{tabs}}}'
        if isinstance(formatted_value, list):
            values = ", ".join(formatted_value)
            formatted_value = f'[{values}]'

        line = f'{tabs}"{key}": {formatted_value}'
        result.append(line)
    return ",\n".join(result)
