#!/usr/bin/env python3

from math import nan


def compress_list(list_to_compress: list) -> list:
    """
    This function compress a list while maintaining order,
    i.e: [1, 6, 4] is converted to [0, 2, 1].

    :param list_to_compress: list: List to compress.

    """
    if list_to_compress == []:
        return list_to_compress

    compressed_list = [0 for x in list_to_compress]

    for n in range(len(list_to_compress)):
        index_max_n = list_to_compress.index(max(list_to_compress))
        compressed_list[index_max_n] = len(compressed_list) - n - 1
        list_to_compress[index_max_n] = nan

    return compressed_list
