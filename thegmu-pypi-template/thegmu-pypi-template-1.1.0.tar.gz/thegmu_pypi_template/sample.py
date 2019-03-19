# -*- coding: utf-8 -*-
"""The GMU Sample - sample module provided with PyPI template repo."""


class Sample():
    """Sample object sample provided with cloning template repo."""

    @staticmethod
    def hello(name="The GMU Project"):
        """This function returns a string of 'Hello name'.

        Accepts an optional name.

        Args:
          name: A optional string for hello testing.

        Returns:
          "Hello name"
        """

        return("Hello %s" % (name, ))
