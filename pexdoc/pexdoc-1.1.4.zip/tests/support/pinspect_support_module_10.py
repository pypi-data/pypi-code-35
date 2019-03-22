# pinspect_support_module_10.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,R0205,R0903,W0107,W0212,W0612


class AClass(object):
    """Class tests func. closing and indentation past prev. indent but not in func."""

    # pylint: disable=C0103,E0602
    def method1(self):  # noqa: D401
        """A method."""
        x = 5

        def func1(x):  # noqa: D401
            """A function."""
            return x + 10

        # A comment
        for item in [1, 2]:

            class SubClass(object):
                """This class does not belong in func1."""

                def __init__(self):
                    self.data = 0

            y = x + item

    def method2(self):
        """Another method."""
        pass
