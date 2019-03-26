import numpy as np
import itertools as itertools


def derivative(row):
    if row['delta_time'] != np.nan and row['delta_coord'] != np.nan \
            and row['delta_time'] != 0:
        return (row['delta_coord']) / row['delta_time']
    return np.nan


def magnitude(row, coords):
    s = 0
    for coord in coords:
        s += row[coord] ** 2
    return np.sqrt(s)


def _angular_velocity(row):
    if row['delta_coord_1'] != np.nan and row['delta_coord_2'] != np.nan \
        and row['delta_time'] != np.nan and row['delta_coord_2'] != 0 \
            and row['delta_time'] != 0:
        return np.arctan(row['delta_coord_1'] /
                         row['delta_coord_2']) / row['delta_time']
    return np.nan


def speed_features(data, prefix, columns, combinations=3):
    """
    Calculates speed related columns with given columns

    :param data: dataframe with raw data
    :param prefix: prefix given to the result columns
    :param columns: columns used for calculation
    :param combinations: combinations (2 = all pairs, 3 = pairs and triplets)
    :return: dataframe with additional columns
    """

    data['delta_time'] = data.time.diff()
    calculated_columns = []

    for column in columns:
        data['delta_coord'] = data[column].diff()
        col_name = prefix + '_' + column[-1]
        data[col_name] = data.apply(derivative, axis=1)
        calculated_columns.append(col_name)

    if combinations >= 2:
        for combination in itertools.combinations(calculated_columns, 2):
            data[prefix + '_' + combination[0][-1] + combination[1][-1]] = \
                data.apply(magnitude, axis=1, coords=combination)

    if combinations >= 3:
        for combination in itertools.combinations(calculated_columns, 3):
            data[prefix + '_' + combination[0][-1] + combination[1][-1] +
                 combination[2][-1]] = data.apply(magnitude, axis=1,
                                                  coords=combination)

    data = data.drop(['delta_coord', 'delta_time'], axis=1)

    return data


def angular_velocity(data, prefix, columns):
    """
    Calculates angular velocity columns for dataframe from given columns

    :param data: dataframe with raw data
    :param prefix: prefix given to the result columns
    :param columns: columns used for calculation
    :return: dataframe with angular velocity columns
    """

    data['delta_time'] = data.time.diff()

    for combination in itertools.combinations(columns, 2):
        data['delta_coord_1'] = data[combination[0]].diff()
        data['delta_coord_2'] = data[combination[1]].diff()

        data[prefix + '_' + combination[0] + combination[1]] = \
            data.apply(_angular_velocity, axis=1)

    data = data.drop(['delta_coord_1', 'delta_coord_2',
                      'delta_time'], axis=1)

    return data
