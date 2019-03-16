import importlib
import importlib.machinery
import importlib.util
import logging
import shutil
import sys
from pathlib import Path

from ktdk import Config, KTDK

log = logging.getLogger(__name__)


class CliManager:
    def __init__(self, config = None, **kwargs):
        self._params = dict(**kwargs)
        self._ktdk = None
        self._config_file = config

    @property
    def ktdk(self) -> KTDK:
        if self._ktdk is None:
            self._ktdk = self.get_ktdk()
        return self._ktdk

    @property
    def config(self) -> Config:
        return self.ktdk.config

    @property
    def workspace_dir(self) -> Path:
        return Path(self.ktdk.config['workspace']).absolute()

    @property
    def test_files_dir(self) -> Path:
        return Path(self.ktdk.config['test_files']).absolute()

    @property
    def submission_dir(self) -> Path:
        return Path(self.ktdk.config['submission']).absolute()

    @property
    def results_dir(self) -> Path:
        return Path(self.ktdk.config['results']).absolute()

    def load_project_files(self):
        """Loads the project files, adds the kontr_tests directly to the
        python modules, so the relative imports are working
        """
        module_path = self.test_files_dir / self.config.get('kontr_tests')
        sys.path.insert(0, str(module_path))
        path = module_path / self.config.get('entry_point')
        return _import_module_files('test_files', path)

    def get_ktdk(self, **kwargs) -> KTDK:
        """Gets new instance of the KTDK
        Args:
            **kwargs: Parameters

        Returns(KTDK): Instance of the KTDK
        """
        config = {**self._params, **kwargs}
        log.debug(f"[CFG] Config: {config}")
        ktdk = KTDK.get_instance(**config)
        return ktdk

    def load_suite(self) -> KTDK:
        """Loads the suite -- it loads the scenario in the test files
        Returns(KTDK):

        """
        self.load_project_files()
        if self._config_file:
            self.ktdk.config.load_yaml(self._config_file)
        return self.ktdk

    def run_the_suite(self) -> KTDK:
        """Run the whole suite, call the invoke method on the KTDK instance
        Returns(KTDK): Instance of the KTDK
        """
        ktdk = self.load_suite()
        if self.ktdk.config.devel and self.ktdk.config.clean:
            workspace = self.ktdk.config.paths.workspace
            log.info(f"[CLEAN] Cleaning workspace: {workspace}")
            shutil.rmtree(workspace)
            workspace.mkdir(parents=True)

        ktdk.invoke()
        return ktdk


def _import_module_files(module_name: str, path: Path):
    """Imports and loads the scenario `instructions.py`F module in the kontr_tests dir
    Args:
        module_name(str): Name of the module,
        path:(Path): Location of the module
    Returns: Scenario definition module instance

    """
    full_path = str(path)
    loader = importlib.machinery.SourceFileLoader(module_name, full_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    log.info(f"[CLI] Loading module: {mod}")
    return mod
