def abs_max(series):
    return series[series.abs().idxmax()]


def abs_min(series):
    return series[series.abs().idxmin()]


def lower_quartile(series):
    return series.quantile(.25)


def upper_quartile(series):
    return series.quantile(.75)


def inter_quartile_range(series):
    return series.quantile(.75) - series.quantile(.25)


def duration(series):
    return series.values[-1] - series.values[0]


def start_of_series(series):
    return series.values[0]


def end_of_series(series):
    return series.values[-1]


speed_functions = ['mean', abs_min, abs_max, 'median', lower_quartile,
                   upper_quartile, inter_quartile_range]
time_functions = [duration]
position_functions = [start_of_series, end_of_series]

speed_columns = ['horizontal_velocity', 'vertical_velocity',
                 'tangential_velocity', 'tangential_acceleration',
                 'tangential_jerk', 'angular_velocity',
                 'horizontal_acceleration', 'vertical_acceleration',
                 'horizontal_jerk', 'vertical_jerk']
time_columns = ['time']
position_columns = ['x', 'y']


def features_for_segment(data, group_by_columns=None):
    """
    Function to compute basic features from given pandas DataFrame.
    DataFrame is required to have columns:
    'horizontal_velocity', 'vertical_velocity', 'tangential_velocity',
    'tangential_acceleration', 'tangential_jerk', 'angular_velocity',
    'horizontal_acceleration', 'vertical_acceleration', 'horizontal_jerk',
    'vertical_jerk', x, y, time, id_user, segment, part

    :param data: pandas DataFrame with specified columns
    :param group_by_columns: list of strings with column names to use in
                            groupby
    :return: DataFrame containing computed features from data
    """

    if group_by_columns is None:
        group_by_columns = ['id_user', 'segment']
    columns = {*speed_columns, *position_columns, *time_columns}
    if not columns.issubset(data.columns):
        return None

    features_df = (data.groupby(group_by_columns)
                   .agg({**{key: speed_functions for key in speed_columns},
                         **{key: time_functions for key in time_columns},
                         **{key: position_functions for key in
                            position_columns}}))
    features_df.columns = ["_".join(y) for y in features_df.columns.ravel()]
    features_df.reset_index(inplace=True)

    return features_df
