"""Support to setup logging output format for paired-comparison analyses

*** Version History:
2018-01-08, first version
2018-07-30, only console output, if no log_file is defined
"""
import logging
from pathlib import Path


def setup(result_path='.', log_file=None):
    """Initialize file and console log output streams.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # *** create handlers explicitly, to specify encoding:

    if log_file is not None:
        result_path = Path(result_path)
        result_path.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(result_path / log_file, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter('{asctime} {name} {levelname}: {message}',
                                          style='{',
                                          datefmt='%Y-%m-%d %H:%M:%S'))
        root_logger.addHandler(fh)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('{asctime} {name}: {message}',
                                           style='{',
                                           datefmt='%H:%M:%S'))
    root_logger.addHandler(console)
