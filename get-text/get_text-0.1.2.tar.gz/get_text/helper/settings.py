import yaml


def load_setting_file(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileExistsError:
        return None
