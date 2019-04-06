import os
import sys

from setupy.core.model import Setup
from setupy.core.serialize import serialize
from setupy.loaders import FileDependencyLoader, YamlDependencyLoader
from setupy.errors import FeatureNotFoundError, SettingNotFoundError

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def setupy(
        imports=None,
        features=None,
        settings=None,
        literal_settings=None,
        dependency_loader=None,
        feature_path=None,
        settings_path=None,
        include_help=False):

    if dependency_loader is None:
        feature_path = (feature_path or
                        os.environ.get("SETUPY_FEATURES") or
                        os.path.join(DIR_PATH, "features"))
        settings_path = (settings_path or
                         os.environ.get("SETUPY_SETTINGS") or
                         os.path.join(DIR_PATH, "settings"))

        dependency_loader = FileDependencyLoader(feature_path, settings_path)

    setup = Setup(dependency_loader)

    if (not features):
        features = []

    if (not imports):
        imports = []

    if (not settings):
        settings = []

    for i in imports:
        setup.add_import(i)

    for f in features:
        try:
            setup.add_feature(f)
        except FeatureNotFoundError:
            print(f'WARNING: Feature {f} was not found', file=sys.stderr)

    for s in settings:
        try:
            setup.add_setting(s)
        except SettingNotFoundError:
            print(f'WARNING: Setting {s} was not found', file=sys.stderr)

    literal_loader = YamlDependencyLoader()

    for s in literal_settings or []:
        setup.add_setting_object(literal_loader.load_setting(s))

    return serialize(setup, include_help)
