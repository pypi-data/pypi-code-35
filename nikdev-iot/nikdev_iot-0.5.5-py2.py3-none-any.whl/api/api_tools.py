# -*- coding: utf-8 -*-


class ApiTools:

    @staticmethod
    def compare_versions(ver1, ver2):
        """
        Compares 2 given version strings and returns 1, -1 or 0 depending
        on which is largest.

        :param ver1: Version string 1, will represent a return value of 1.
        :type ver1: str
        :param ver2: Version string 2, will represent a return value of -1.
        :type ver2: str
        :return: 1 if ver1 is larger, -1 of ver2 is larger, otherwise 0.
        :rtype: int
        """
        # Cast the version strings to lists of integers
        v1 = ApiTools.split_version(ver1)
        v2 = ApiTools.split_version(ver2)

        for i in range(max(len(v1), len(v2))):
            # If the version list of ver1 is shorter than v2, pad it with a zero
            if i >= len(v1):
                v1 += [0]
            # And vice versa
            if i >= len(v2):
                v2 += [0]

            # If v1 is larger than v2, return 1
            elif v1[i] > v2[i]:
                return 1
            # If v2 is larger than v1, return -1
            elif v1[i] < v2[i]:
                return -1

        # If we haven't decided any "winner" yet, they are the same
        return 0

    @staticmethod
    def split_version(version):
        """
        Takes a given string of a version (ie "1.2.3") and
        splits it into a list ([1, 2, 3]).

        :param version: The version string to convert.
        :type version: str
        :return: A list with the string representation.
        :rtype: list[int]
        """
        return map(lambda x: int(x) if x is not "" else 0, version.split("."))