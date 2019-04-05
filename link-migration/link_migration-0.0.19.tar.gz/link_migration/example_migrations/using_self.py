# -*- coding: utf-8 -*-
"""
    Using the self object.

    This shows how to access the config file, along with other migration
    metadata and functionality.
"""

version = 20


def up(self):
    """
    Migration upgrade with self object.

    :param self: Contains the config object which allows conf.py access.
    """
    print(f'Version: {version} --- Root Dir: {self.config.ROOT_DIR}')


def down(self):
    """
    Migration downgrade with self object.

    :param self: Contains the config object which allows conf.py access.
    """
    print(f'Version: {version} --- Root Dir: {self.config.ROOT_DIR}')
