import abc
import collections
import logging
import os
from pathlib import Path
from typing import Union

CONFIG_PATH = Path(__file__).parent / 'resources' / 'config'

log = logging.getLogger(__name__)


def _load_env_var(key: str, val: str):
    if not key.startswith('KTDK_'):
        return None
    name = key[5:].lower()
    if val in ['True', 'true']:
        val = True
    if val in ['False', 'false']:
        val = False
    return {name: val}


def _load_env_vars() -> dict:
    params = {}
    for (key, val) in os.environ.items():
        parsed = _load_env_var(key, val)
        if parsed:
            params.update(parsed)
    return params


def _get_subdir(where: Path, sub_path, create=False):
    full_path = where / Path(sub_path)
    if create and not full_path.exists():
        full_path.mkdir(parents=True)
    return full_path


class ConfigPaths:
    """Context dirs wrapper for paths
    """

    def __init__(self, config: 'ConfigPropMixin'):
        """Creates instance of the paths dirs
        Args:
            config(ConfigPropMixin): Context instance
        """
        self._container = config

    @property
    def workspace(self) -> Path:
        """Gets workspace path
        Returns(Path): Workspace path
        """
        return Path(self._container['workspace'])

    @property
    def test_files(self) -> Path:
        """Test files path
        Returns(Path): Test file path
        """
        return Path(self._container['test_files'])

    @property
    def submission(self) -> Path:
        """Submission files path
        Returns:

        """
        return Path(self._container['submission'])

    def submission_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return _get_subdir(self.submission, sub_path, create)

    def test_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return _get_subdir(self.test_files, sub_path, create)

    def result_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return _get_subdir(self.results, sub_path, create)

    def workspace_path(self, sub_path: Union[str, Path], create=False) -> Path:
        return _get_subdir(self.workspace, sub_path, create)

    @property
    def results(self) -> Path:
        """Gets results path
        Returns(Path): Results path

        """
        results_dir = self._container['results']
        if not results_dir:
            results_dir = self.workspace / 'results'
        return Path(results_dir)

    def get_dir(self, name) -> Path:
        return getattr(self, name)

    def resolve(self, name) -> Path:
        return getattr(self, name, name)

    def save_result(self, sub_path: Union[str, Path], content) -> Path:
        path = self.results / Path(sub_path)
        base_dir: Path = path.parent
        if not base_dir.exists():
            base_dir.mkdir(parents=True)
        log.debug(f"[SAVE] Save content to the results file: {sub_path}")
        path.write_text(content, encoding='utf-8')
        return path


class ConfigPropMixin:
    @property
    def paths(self) -> ConfigPaths:
        if not hasattr(self, '__paths'):
            setattr(self, '__paths', ConfigPaths(self))
        return getattr(self, '__paths')

    @property
    def devel(self) -> bool:
        return self.__props__.get('devel', False)

    @property
    def kill(self) -> bool:
        return self.__props__.get('kill', False)

    @property
    def clean(self) -> bool:
        return self.__props__.get('clean', False)

    @property
    def submission_config(self) -> dict:
        return self.__props__['submission_config']

    @submission_config.setter
    def submission_config(self, value):
        self.__props__['submission_config'] = value

    @property
    @abc.abstractmethod
    def __props__(self) -> dict:
        return {}


class Config(collections.MutableMapping, ConfigPropMixin):
    def __len__(self) -> int:
        return len(self.container)

    def __iter__(self):
        return iter(self.container)

    def __delitem__(self, item):
        del self.container[item]

    def __init__(self, **params):
        self._container = params or {}

    def load(self):
        tmp_params = dict(self._container)
        self._load_default()
        self._load_provided()
        self.load_envs()
        self._container.update(tmp_params)

    @property
    def container(self) -> dict:
        return self._container

    def __getitem__(self, item):
        return self._container[item]

    def __setitem__(self, key, value):
        self._container[key] = value

    def _load_default(self):
        """Loads the default config from the CONFIG
        """
        self.load_yaml(CONFIG_PATH / 'defaults.yml')

    def _load_test_files(self, rel_path=None):
        """Will load the configuration from the config file located in the test_files
        Args:
            rel_path: Relative path in the test_files
        """
        rel_path = rel_path or 'config.yml'
        path = self.paths.test_files / rel_path
        if path.exists():
            self.load_yaml(path)

    def load_yaml(self, file_path):
        """Loads the YAML config from any location
        Args:
            file_path: Yaml location file path
        """
        from ktdk import utils
        self._container.update(utils.parse_yaml_config(file_path))

    def load_envs(self):
        """Loads the params from the env variables
        """
        envs = _load_env_vars()
        self._container.update(envs)

    def load_dict(self, params: dict):
        """Loads the dictionary
        Args:
            params:
        Returns:
        """
        self._container.update(params)

    def save_yaml(self, file_path):
        """Saves the configuration to the YAML file
        Args:
            file_path: YAML file path
        """
        from ktdk import utils
        utils.save_yaml(file_path, self)

    @property
    def __props__(self):
        return self.container

    def _load_provided(self):
        provided_path = self.paths.test_files / self.get('ktdk_config_path', '.ktdk_config.yml')
        if provided_path.exists():
            log.info(f"[CFG] Loading provided KTDK config for project: {provided_path}")
            self.load_yaml(provided_path)
