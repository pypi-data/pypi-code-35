"""

Module that contains the Version manager class.

"""
from distutils.version import StrictVersion


class VersionManager(object):
    """

    Class that manages the minimum version for executing a operation with
    PKI Express.

    """

    def __init__(self):
        self.__min_version = StrictVersion('0.0')

    def require_version(self, min_version_candidate):
        """

        Requires some minimum version for a operation.
        :param min_version_candidate: The minimum version needed for some
                                      operation.

        """
        candidate = StrictVersion(min_version_candidate)
        if candidate > self.__min_version:
            self.__min_version = candidate

    def require_min_version_flag(self):
        """

        Verifies the requirement to add the min-version flag to the command.
        :return: the requirement to add the min-version flag

        """
        return self.__min_version > StrictVersion('1.3')

    @property
    def min_version(self):
        """

        Gets the minimum version received with all calls to the
        require_min_version_flag() method.

        """
        return self.__min_version


__all__ = ['VersionManager']
