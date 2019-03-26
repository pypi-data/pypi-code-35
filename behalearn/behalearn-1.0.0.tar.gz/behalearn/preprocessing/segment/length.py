import numpy as np


def calculate_length(data):
    """
    Function that calculates distance of 2 points

    :param data: list of 2 rows, where row is list of point's coordinates
                respectively (x, y, ..)
    :return: distance of 2 points
    """
    result = 0
    for i in range(len(data[0])):
        result += abs(data[0][i] - data[1][i]) ** 2
    result = np.sqrt(result)
    return result


def air_length(df):
    """
    Function that calculates air distance of sorted DataFrame of points

    :param df: DataFrame of points, where row means point and column means
                single coordinate('x', 'y' ..)
    :return: air distance of first and last point in DataFrame
    """

    if df.shape[0] <= 1:
        return 0

    return calculate_length(df.iloc[[0, -1]].values)


def real_length(df):
    """
    Function that calculates real distance of sorted DataFrame of points

    :param df: DataFrame of points, where row means point and column means
                single coordinate('x', 'y' ..)
    :return: real distance of trajectory defined by DataFrame
    """

    if df.shape[0] <= 1:
        return 0

    len_sum = 0
    data = df.values
    for row_index in range(1, len(data)):
        len_sum += calculate_length(data[[row_index, row_index - 1]])
    return len_sum
