# -*- coding: utf-8 -*-
"""
    Goodbye World.

    This is the most simplistic migration technique.
"""

version = 30


def up():
    """
        This migration should delete the world.
    """
    print("Goodbye World")


def down():
    """
        This migration should create the world.
    """
    print("Hello World")
