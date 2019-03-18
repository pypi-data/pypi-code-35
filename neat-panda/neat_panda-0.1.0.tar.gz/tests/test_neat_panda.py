#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `neat_panda` package."""

import pytest
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

from neat_panda import spread, gather

df = pd.DataFrame(
    data={
        "Country": ["Sweden", "Sweden", "Denmark"],
        "Continent": ["Europe", "Europe", "Not known"],
        "Year": [2018, 2019, 2018],
        "Actual": [1, 2, 3],
    }
)


class TestTypesSpread:
    def test_input_types_1(self):
        with pytest.raises(TypeError):
            spread([1, 2, 3])

    def test_input_types_key(self):
        with pytest.raises(TypeError):
            spread(df=df, key=1, value="Actual")

    def test_input_types_value(self):
        with pytest.raises(TypeError):
            spread(df=df, key="Country", value=1)

    def test_input_types_fill(self):
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

    def test_test_spread(self):
        _df = spread(
            df=df,
            key="Year",
            value="Actual",
            fill="hek",
            drop=False,
            convert=True,
            sep="_",
        )
        print()
        print(_df)


class TestTypesGather:
    df = spread(df=df, key="Year", value="Actual")

    def test_equal_df(self, df=df):
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

    def test_test_gather(self, df=df):
        __df = gather(
            df=df,
            key="Year",
            value="Actual",
            columns=["Country", "Continent"],
            invert_columns=True,
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
