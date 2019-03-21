# -*- coding: utf-8 -*-

import pandas as pd
from typing import Union, Optional, List
from ._helpers import _control_types, _assure_consistent_value_dtypes, _custom_columns


def spread(
    df: pd.DataFrame,
    key: str,
    value: str,
    fill: Union[str, int, float] = "NaN",
    convert: bool = False,
    drop: bool = False,
    sep: Optional[str] = None,
) -> pd.DataFrame:
    """Spread a key-value pair across multiple columns.
    Behaves similar to the tidyr spread function.\n
    Does not work with multi index dataframes.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame
    key : str
        Column to use to make new frame’s columns
    value : str
        Column which contains values corresponding to the new frame’s columns
    fill : Union[str, int, float], optional
        Missing values will be replaced with this value.\n
        (the default is "NaN", which is numpy.nan)
    convert : bool, optional
        If True, the function tries to set the new columns datatypes to the original frame's value column datatype.
        However, if fill is equal to "NaN", all columns with a 'filled' value is set to the object type since Numpy.nan is of that type\n
        (the default is False, which ...)
    drop : bool, optional
        If True, all rows that contains at least one "NaN" is dropped.
        (the default is False)
    sep : Optional[str], optional
        If set, the names of the new columns will be given by "<key_name><sep><key_value>".\n
        E.g. if set to '-' and the key column is called 'Year' and contains 2018 and 2019 the new columns will be\n
        'Year-2018' and 'Year-2019'. (the default is None, and using previous example, the new column names will be '2018' and '2019')

    Returns
    -------
    pd.DataFrame
        A widened dataframe

    Example
    -------
    from neat_panda import spread
    from gapminder import gapminder

    gapminder2 = gapminder[["country", "continent", "year", "pop"]]
    gapminder3 = spread(df=gapminder2, key="year", value="pop")
    # or
    gapminder3 = gapminder2.pipe(spread, key="year", value="pop")

    print(gapminder3)

           country continent      1952      1957      1962  ...
    0  Afghanistan      Asia   8425333   9240934  10267083  ...
    1      Albania    Europe   1282697   1476505   1728137  ...
    2      Algeria    Africa   9279525  10270856  11000948  ...
    3       Angola    Africa   4232095   4561361   4826015  ...
    4    Argentina  Americas  17876956  19610538  21283783  ...
    .          ...       ...       ...       ...       ...  ...
    """

    _control_types(
        _df=df, _key=key, _value=value, _fill=fill, _convert=convert, _sep=sep
    )
    _drop = [key, value]
    _columns = [i for i in df.columns.tolist() if i not in _drop]
    _df = df.set_index(_columns).pivot(columns=key)
    _df.columns = _df.columns.droplevel()
    new_df = pd.DataFrame(_df.to_records())
    _new_columns = [i for i in new_df.columns if i not in df.columns]
    if sep:
        custom_columns = _custom_columns(
            new_df.columns.to_list(), _new_columns, key, sep
        )
        new_df.columns = custom_columns
        _new_columns = [i for i in new_df.columns if i not in df.columns]
    if fill != "NaN":
        new_df[_new_columns] = new_df[_new_columns].fillna(fill)
    if drop:
        new_df = new_df.dropna(how="any")
    if convert:
        new_df = _assure_consistent_value_dtypes(new_df, df, _new_columns, value)
    return new_df


def gather(
    df: pd.DataFrame,
    key: str,
    value: str,
    columns: Union[List[str], range],
    drop_na: bool = False,
    convert: bool = False,
    invert_columns: bool = False,
) -> pd.DataFrame:
    """Collapses/unpivots multiple columns into two columns, one with the key and one with the value.
    Behaves similir to the tidyr function gather.

    Parameters
    ----------
    df : pd.DataFrame
        An untidy dataframe
    key : str
        Name of the new key column
    value : str
        Name of the new value column
    columns : Union[List[str], range]
        If invert_columns is set to False, as per default, the columns to unpivot.
        If invert columns is set to True, the columns NOT to pivot. 
        Columns should be given as a list of string or a range of columns indexes.
    drop_na : bool, optional
        If True, all rows that contains at least one "NaN" is dropped.
        (the default is False)
    convert : bool, optional
        If True, the function uses infer_objects to set datatype (the default is False)
    invert_columns : bool, optional
        Should be used in conjunction with columns. If set to True, the columns set will be switched to the ones not present in the list (range).
        (the default is False)

    Returns
    -------
    pd.DataFrame
        A tidy dataframe
    """

    _control_types(
        _df=df,
        _key=key,
        _value=value,
        _columns=columns,
        _drop_na=drop_na,
        _convert=convert,
        _invert_columns=invert_columns,
    )
    _all_columns = df.columns.to_list()
    if isinstance(columns, range):
        _temp_col = []
        _index = list(columns)
        for i, j in enumerate(_all_columns):
            if i in _index:
                _temp_col.append(j)
        columns = _temp_col
    if invert_columns:
        columns = [i for i in _all_columns if i not in columns]
    _id_vars = [i for i in _all_columns if i not in columns]
    new_df = pd.melt(
        frame=df, id_vars=_id_vars, value_vars=columns, value_name=value, var_name=key
    )
    if drop_na:
        new_df = new_df.dropna(how="all", subset=[value])
    if convert:
        _dtype = new_df[value].infer_objects().dtypes
        new_df[value] = new_df[value].astype(_dtype)
    return new_df


if __name__ == "__main__":
    pass
