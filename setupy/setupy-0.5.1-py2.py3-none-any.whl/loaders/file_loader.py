import os

from setupy.loaders import YamlDependencyLoader
from setupy.errors import SettingNotFoundError, FeatureNotFoundError


def _without_extension(iterable):
    for f in iterable:
        filename, _ = os.path.splitext(f)
        yield filename


def _files_only(directory):
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            yield f


class FileDependencyLoader:

    def __init__(self, feature_path, setting_path):
        self._feature_path = feature_path
        self._setting_path = setting_path
        self._yaml_loader = YamlDependencyLoader()

    def feature_names(self):
        return set(_without_extension(_files_only(self._feature_path)))

    def setting_names(self):
        return set(_without_extension(_files_only(self._setting_path)))

    def load_feature(self, feature_name):
        prefix = os.path.join(self._feature_path, feature_name)
        try:
            with open(prefix + ".yaml") as yaml:
                with open(prefix + ".py") as py:
                    return self._yaml_loader.load_feature(yaml.read(), py.read())
        except FileNotFoundError as e:
            raise FeatureNotFoundError(feature_name) from e

    def load_setting(self, setting_name):
        try:
            with open(os.path.join(self._setting_path, setting_name) + ".yaml") as yaml:
                return self._yaml_loader.load_setting(yaml.read())
        except FileNotFoundError as e:
            raise SettingNotFoundError(setting_name) from e
