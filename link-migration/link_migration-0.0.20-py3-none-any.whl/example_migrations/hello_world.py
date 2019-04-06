# -*- coding: utf-8 -*-
"""
    Hello World.

    This is the most simplistic migration technique.

"""

version = 1


def up():
    """
        Migrate Hello World
    """
    print("Hello World")


def down():
    """
        Downgrade Hello World
    """
    print("Goodbye World")
