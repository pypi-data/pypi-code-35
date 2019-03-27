import json
from typing import List, TypeVar, Any, Tuple

import arrow
import attr
import pandas as pd

from cortex.profile.utils import seconds_between_times, first_arg_is_type_wrapper, tuples_with_nans_to_tuples_with_nones

T = TypeVar("T")

__all__ = [
    'list_of_attrs_to_df',
    'map_column',
    'df_to_typed_list',
    'append_seconds_to_df',
    'split_df_into_files_based_on_date',
    'explode_column',
    'head_as_dict',
    'filter_time_column_after',
    'filter_time_column_before',
    'df_to_tuples',
    'parse_set_notation',
    'parse_string_set_notation',
    'parse_set_of_json_strings_notation',
    'df_to_records',
    'merge_list_of_dfs_similarly',
]


def list_of_attrs_to_df(l:List) -> pd.DataFrame:
    return pd.DataFrame([
        attr.asdict(x) for x in l
    ])


def map_column(column: pd.Series, mapper:callable) -> pd.Series:
    return column.map(mapper)


def append_seconds_to_df(df:pd.DataFrame, column_name_to_append:str, start_time_col:str, end_time_col:str) -> pd.DataFrame:
    return df.assign(**{
        column_name_to_append: list(map(
            lambda x: seconds_between_times(arrow.get(x[0]), arrow.get(x[1])),
            df[[start_time_col, end_time_col]].itertuples(index=False, name=None)
        ))
    })


def split_df_into_files_based_on_date(df: pd.DataFrame, on_date: str, file_pattern: str) -> None:
    """
    :param df: Dataframe to split
    :param on_date: Date column to split on
    :param file_pattern: The pattern to save the new files created, where {date} will be replaced with the actual date ...
    :return: Nothing, this function creates new files ...
    """
    for date, df_on_date in df.groupby(on_date):
        df_on_date.reset_index().to_csv(file_pattern.format(date=str(arrow.get(date).date())))


def explode_column(unindexed_df:pd.DataFrame, column:str) -> pd.DataFrame:
    """
    Assumption is df has no index ...
    :param df:
    :param column:
    :return:
    """
    if unindexed_df.empty:
        return unindexed_df
    id_columns = list(set(unindexed_df.columns).difference(set([column])))
    df = (unindexed_df.set_index(id_columns))[column].apply(pd.Series).stack().to_frame(column)
    for column in id_columns:
        df = df.reset_index(level=column)
    return df.reset_index(drop=True)

#  ------------------

def filter_time_column_after(df:pd.DataFrame, time_column:str, shifter:dict) -> pd.DataFrame:
    """

    :param df: The Dataframe to filter
    :param time_column: The name of the time column to filter
    :param shifter: Arrow friendly dict to shift an arrow time ...
    :return:
    """
    return df[df[time_column].map(arrow.get) >= arrow.utcnow().shift(**shifter)].reset_index(drop=True)


def filter_time_column_before(df:pd.DataFrame, time_column:str, shifter:dict) -> pd.DataFrame:
    """

    :param df: The Dataframe to filter
    :param time_column: The name of the time column to filter
    :param shifter: Arrow friendly dict to shift an arrow time ...
    :return:
    """
    return df[df[time_column].map(arrow.get) <= arrow.utcnow().shift(**shifter)].reset_index(drop=True)


#  ------------------


def parse_set_notation(string_series:pd.Series) -> pd.Series:
    if string_series.empty:
        return pd.Series([])
    return string_series.map(parse_string_set_notation)


def parse_string_set_notation(string:str) -> pd.Series:
    return set(string[1:-1].split(","))


def parse_set_of_json_strings_notation(string_series):
    if string_series.empty:
        return []
    return string_series.map(
        first_arg_is_type_wrapper(
            lambda string: list(map(
                lambda x: json.loads(x),
                json.loads("[{}]".format(string[1:-1]))
            )),
            (str)
        )
    )

#  ---------- DF Conversions ----------

def head_as_dict(df:pd.DataFrame) -> str:
    return {} if df.empty else df_to_records(df[0])


def df_to_records(df:pd.DataFrame) -> List[dict]:
    """
    Turns a Dataframe into a list of dicts ...
    :param df:
    :return:
    """
    # return df.to_dict(orient="records")
    return df.to_dict('records')


def df_to_tuples(df:pd.DataFrame, columns:List):
    return tuples_with_nans_to_tuples_with_nones(df[columns].itertuples(index=False, name=None))


def df_to_typed_list(df:pd.DataFrame, t:T) -> List[T]:
    return list(map(
        lambda rec: t(**rec),
        df_to_records(df)
    ))


#  ---------- DF Concatination ----------

def merge_list_of_dfs_similarly(group_list:List[pd.DataFrame], **kwargs) -> pd.DataFrame:
    """
    Merged a list of Dataframes ... into a single Dataframe ... on the same criteria ...
    :param group_list:
    :param kwargs:
    :return:
    """
    if len(group_list) == 0:
        return pd.DataFrame(columns=[kwargs.get("on", kwargs.get("left_on"))])
    if len(group_list) == 1:
        return group_list[0]
    if len(group_list) == 2:
        return pd.merge(group_list[0], group_list[1], **kwargs)
    if len(group_list) >= 3:
        return merge_list_of_dfs_similarly(
            [merge_list_of_dfs_similarly(group_list[:2], **kwargs)] + group_list[2:]
        )
