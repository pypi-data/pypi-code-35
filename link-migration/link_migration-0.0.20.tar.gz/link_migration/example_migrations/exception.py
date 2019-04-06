# -*- coding: utf-8 -*-
"""
    Raise an exception during migration.

    Consider multiple way to handle an exception, such as continuation,
    ending, and retrying.
"""

version = 40


def up():
    """
        Upgrading with an exception
    """

    # raise Exception('An Exception in migration upgrading occured')


def down():
    """
        Downgrading with an exception
    """

    # raise Exception('An Exception in migration downgrading occured')
