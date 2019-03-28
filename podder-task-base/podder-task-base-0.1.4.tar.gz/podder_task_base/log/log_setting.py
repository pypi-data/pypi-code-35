import logging
import os

import yaml


class LogSetting:
    LOG_YML_PATH = 'log.yml'
    _log_setting = None

    def load(self):
        if LogSetting._log_setting is None:
            LogSetting._log_setting = self._load_log_yml()
        return(LogSetting._log_setting)

    def _load_log_yml(self):
        file_path = self.LOG_YML_PATH
        if os.path.exists(file_path):
            with open(file_path, 'r') as stream:
                ret = yaml.load(stream)
        else:
            # if "log.yml" not found, load defalut values
            ret = {
                "task_name": "task-name-sample",
                "task_log_format": "[%(asctime)s] %(levelname)s - %(message)s",
                "task_log_level": logging.DEBUG,
                "sql_log_format": "[%(asctime)s] %(levelname)s - %(message)s",
                "sql_log_level": logging.WARN,
            }
        return ret
