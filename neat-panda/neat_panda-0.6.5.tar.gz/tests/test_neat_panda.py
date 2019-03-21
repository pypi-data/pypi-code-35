#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `neat_panda` package."""

import pytest
import pandas as pd
import numpy as np

from neat_panda import spread, gather

df = pd.DataFrame(
    data={
        "Country": ["Sweden", "Sweden", "Denmark"],
        "Continent": ["Europe", "Europe", "Not known"],
        "Year": [2018, 2019, 2018],
        "Actual": [1, 2, 3],
    }
)


class TestsSpread:
    def test_input_types_1(self):
        with pytest.raises(TypeError):
            spread(df=[1, 2, 3], key="hello", value="Goodbye")

    def test_input_types_key(self):
        with pytest.raises(TypeError):
            spread(df=df, key=1, value="Actual")

    def test_input_types_value(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Country", value=1)

    def test_input_types_fill_bool(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=True)

    def test_input_types_fill(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=pd.DataFrame)

    def test_input_types_convert(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=1, convert="True")

    def test_input_types_sep(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Year", value="Actual", fill=1, convert=True, sep=1)

    def test_user_warning(self):
        with pytest.warns(UserWarning):
            _df = spread(df=df, key="Year", value="Actual", drop=False, convert=True)

    def test_no_nan(self):
        _df = spread(df=df, key="Year", value="Actual", drop=True, convert=True)
        assert _df.isna().any().sum() == 0

    def test_fill_other_than_nan(self):
        df1 = spread(df=df, key="Year", value="Actual", fill="Hej", sep="_")
        df2 = spread(df=df, key="Year", value="Actual", sep="_")
        print(df1)
        _idx1 = sorted(df1.query("Year_2019=='Hej'").index.tolist())
        _idx2 = sorted(df2.query("Year_2019.isna()").index.tolist())
        assert _idx1 == _idx2

    def test_test_spread(self):
        _df = spread(
            df=df,
            key="Year",
            value="Actual",
            fill="NaN",
            drop=False,
            convert=True,
            sep="_",
        )
        print()
        print(_df)
        print()
        print(_df.dtypes)


class TestsGather:
    df_wide = spread(df=df, key="Year", value="Actual")
    # print(df.dtypes)

    def test_equal_df(self, df=df_wide):
        df1 = gather(
            df=df,
            key="Year",
            value="Actual",
            columns=["Country", "Continent"],
            invert_columns=True,
            # convert=True,
        )
        df2 = gather(df=df, key="Year", value="Actual", columns=["2018", "2019"])

        assert df1.equals(df2)

    def test_correct_length_range(self):
        with pytest.raises(IndexError):
            gather(df=df, key="Year", value="Actual", columns=range(2, 100))

    # def test_correct_conversion(self, df=df_wide):
    #    print()
    #    print(df.dtypes)
    #    print()
    #    df = gather(
    #        df=df, key="Year", value="Actual", columns=["2018", "2019"], convert=True
    #    )
    #    print(df.dtypes)
    #

    def test_correct_column_type(self):
        with pytest.raises(TypeError):
            gather(df=df, key="Year", value="Actual", columns="string")

    def test_correct_dropna_type(self):
        with pytest.raises(TypeError):
            gather(
                df=df,
                key="Year",
                value="Actual",
                columns=["2018", "2019"],
                drop_na="Yes",
            )

    def test_correct_invertcolumns_type(self):
        with pytest.raises(TypeError):
            gather(
                df=df,
                key="Year",
                value="Actual",
                columns=["2018", "2019"],
                invert_columns="Yes",
            )

    def test_test_gather(self, df=df_wide):
        __df = gather(
            df=df,
            key="Year",
            value="Actual",
            columns=range(2, 4),
            invert_columns=False,
            drop_na=True,
            # convert=True,
        )
        print()
        print(__df)


# x = gather(df=df, key="year", value="pop", columns=["country","continent"], invert_columns=True).sort_values(by=["country", "year"]).reset_index(drop=True)
# gapminder2 = gapminder[["country", "continent", "year", "pop"]]
# x = spread(df=gapminder2, key="year", value="pop")
# x.equals(gapminder2) -> False since dtyp of year is not equal
'''

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

'''
