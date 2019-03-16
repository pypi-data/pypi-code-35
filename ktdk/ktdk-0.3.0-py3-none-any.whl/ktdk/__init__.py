"""
Main KTDK module
"""
__version__ = '0.3.0'

from ktdk import log_config, utils

log_config.load_config()

import json
import logging
from pathlib import Path
from typing import Callable, List, Optional

import requests

from ktdk.config import Config
from ktdk.core import Result, Task, Test
from ktdk.runtime import Context
from ktdk.runtime.stat import stat_test

log = logging.getLogger(__name__)


def dump_to_file(context: Context, file_name: str, what):
    """Dumps content to the file
    Args:
        context(Context): Context instance
        file_name(str): File name
        what: What should be written to the file
    """
    file_name = utils.unique_name(file_name, context=context) + ".json"
    context.paths.save_result(file_name, json.dumps(what))


class KTDK:
    """
    Main class of the KTDK, it holds configuration, the suite (root of the )
    """
    instance = None

    @staticmethod
    def get_instance(**cfg) -> 'KTDK':
        """Gets an instance of the KTDK
        Args:
            **cfg: KTDK config

        Returns(KTDK): KTDK instance

        """
        if KTDK.instance is None:
            log.debug(f"[KTDK] Instance config: {cfg}")
            KTDK.instance = KTDK(**cfg)
        return KTDK.instance

    def __init__(self, **cfg):
        """Creates instance of the KTDK suite
        Args:
            **cfg:
        """
        self.suite = Test(name='suite', tags=['suite'])
        self._post_actions: List[Callable] = []
        self.config = Config(**cfg)
        self.config.load()
        self.config['submission_config'] = self._parse_submission_config()
        log_config.load_config(**self.config, results_dir=self.config.paths.results)
        self.config.log_config()
        log.info(f"[KTDK] Version {__version__}")

    def register_tags(self, *tags):
        """Register avail. tags for the suite run
        Args:
            *tags: List of tags
        """
        if 'registered_tags' not in self.config:
            self.config['registered_tags'] = []
        self.config['registered_tags'].extend(tags)

    @property
    def post_actions(self) -> List[Callable]:
        """Gets all the post actions
        Returns(List[Callable]): List of all post actions
        """
        return self._post_actions

    def add_post_action(self, post_action: Callable):
        """Adds post action - action that will be executed after suite has been executed
        Args:
            post_action(Callable): Function that takes KTDK instance as the 1st arg and
                                    the Context as the 2nd arg

        """
        self._post_actions.append(post_action)

    def post_action(self):
        """Decorator that defines the post action
        Returns(Callable): Decorated Callable
        """

        def __post_action(func):
            self.add_post_action(func)

        return __post_action

    def create_context(self) -> Context:
        """Creates context from the configuration
        Returns(Context): The context instance
        """
        context = Context(suite_config=self.config, test_config={})

        return context

    def invoke(self) -> Result:
        """Invokes the KTDK suite
        Returns(Result): Overall result of the suite
        """
        return self.run()

    def run(self) -> Result:
        """Runs whole KTDK suite adn saves result

        Returns(Result): Overall result of the suite
        """
        context = self.create_context()
        log.info(f"[CTX] Created: {context}")
        suite_runner = self.suite.runner.get_instance(context=context)
        suite_result = suite_runner.invoke()
        self.__dump_required_files(context)
        self.__invoke_post_actions(context)
        return suite_result

    @property
    def stats(self) -> dict:
        return stat_test(self.suite)

    def __invoke_post_actions(self, context: Context):
        for post_action in self.post_actions:
            post_action(self, context)

        self.__send_notification(context=context)

    def __dump_required_files(self, context):
        if context.config['dump_result']:
            dump_to_file(context, 'suite-result', self.suite.to_dict())
        dump_to_file(context, 'suite-stats', self.stats)
        dump_to_file(context, 'suite-files', context.config['work_files'])

    def __send_notification(self, context: Context):
        webhook_url = context.config['webhook_url']
        if webhook_url:
            params = dict(url=webhook_url, data=json.dumps(self.stats))
            if context.config['webhook_token']:
                params['headers'] = {'Authorization': 'Bearer ' + context.config['webhook_token']}
            requests.post(**params)

    def _parse_submission_config(self) -> Optional[dict]:
        full_path = self._get_submission_config_path()
        if not full_path.exists():
            log.debug(f"[CONFIG] Submission config files has not been provided - {full_path}")
            return None
        sub_config = utils.parse_yaml_config(full_path)
        log.info(f"[LOAD] Loaded submission config {full_path}: {sub_config}")
        return sub_config

    def _get_submission_config_path(self) -> Optional[Path]:
        submission_config_file = self.config.get('submission_config_file')
        if submission_config_file is None:
            return None
        submission_path = self.config.get('submission')
        if submission_path is None:
            return None
        return Path(submission_path) / submission_config_file
