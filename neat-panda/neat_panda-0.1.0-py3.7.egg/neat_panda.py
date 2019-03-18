# -*- coding: utf-8 -*-

"""Main module."""
import pandas as pd
from typing import Union, Optional, List
from warnings import warn


def _control_types(
    _df,
    _key,
    _value,
    _fill="NaN",
    _convert=False,
    _sep=None,
    _columns=[],
    _drop_na=False,
):
    if not isinstance(_df, pd.DataFrame):
        raise TypeError("write something")
    if not isinstance(_key, str):
        raise TypeError()
    if not isinstance(_value, str):
        raise TypeError()
    if isinstance(_fill, bool):
        raise TypeError
    if not isinstance(_fill, (str, float, int)):
        raise TypeError()
    if not isinstance(_convert, bool):
        raise TypeError()
    if not isinstance(_sep, (str, type(None))):
        raise TypeError
    if not isinstance(_columns, list):
        raise TypeError
    if not isinstance(_drop_na, bool):
        raise TypeError


def _assure_consistent_value_dtypes(new_df, old_df, columns, value):
    """
    """
    print(old_df[value].dtypes)

    _dtype = old_df[value].dtypes
    try:
        new_df[columns] = new_df[columns].astype(_dtype)
    except ValueError:
        warn(
            """Because the parameter drop is set to False and NA is generated\n
            when the dataframe is widened, the type of the new columns is set to Object."""
        )
        new_df[columns] = new_df[columns].astype("O")
    return new_df


def _custom_columns(columns, new_columns, key, sep):
    _cols = [i for i in columns if i not in new_columns]
    _custom = [key + sep + i for i in new_columns]
    print(_cols + _custom)
    return _cols + _custom


def spread(
    df: pd.DataFrame,
    key: str,
    value: str,
    fill: Union[str, int, float] = "NaN",
    convert: bool = False,
    drop: bool = False,
    sep: Optional[str] = None,
) -> pd.DataFrame:
    """behaves similar to the tidyr gather function.\n
    Does not work with multi index
    """
    _control_types(
        _df=df, _key=key, _value=value, _fill=fill, _convert=convert, _sep=sep
    )
    _drop = [key, value]
    _columns = [i for i in df.columns.tolist() if i not in _drop]
    try:
        _df = df.set_index(_columns).pivot(columns=key)
    except ValueError:
        raise ValueError("something about that ")
    _df.columns = _df.columns.droplevel()
    new_df = pd.DataFrame(_df.to_records())
    _new_columns = [i for i in new_df.columns if i not in df.columns]
    if drop:
        new_df = new_df.dropna(how="any")
    if fill != "NaN":
        new_df[_new_columns] = new_df[_new_columns].fillna(fill)
    if convert:
        new_df = _assure_consistent_value_dtypes(new_df, df, _new_columns, value)
    if sep:
        custom_columns = _custom_columns(
            new_df.columns.to_list(), _new_columns, key, sep
        )
        new_df.columns = custom_columns
    return new_df


def gather(
    df: pd.DataFrame,
    key: str,
    value: str,
    columns: Optional[List[str]] = None,
    drop_na: bool = False,
    convert: bool = False,
) -> pd.DataFrame:
    """behaves similar to the tidyr gather function.\n
    Does not work with multi index
    """
    _control_types(
        _df=df,
        _key=key,
        _value=value,
        _columns=columns,
        _drop_na=drop_na,
        _convert=convert,
    )
    _all_columns = df.columns.to_list()
    _id_vars = [i for i in _all_columns if i not in columns]
    new_df = pd.melt(
        frame=df, id_vars=_id_vars, value_vars=columns, value_name=value, var_name=key
    )
    if drop_na:
        new_df = new_df.dropna(how="all", subset=[value])
    if convert:
        _dtype = df[value].infer_objects().dtypes
        new_df[value] = new_df[value].astype(_dtype)
    return new_df


if __name__ == "__main__":
    pass
