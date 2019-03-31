# Copyright 2019 Rafe Kaplan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

import pytest

import fuzidate as fzd

OUTBREAK = datetime.date(1914, 7, 28)
OUTBREAK_FZD = fzd.Fuzidate.from_int(19140728)


def test_from_date():
    assert fzd.Fuzidate.from_date(OUTBREAK).number == 19140728


def test_constants():
    assert fzd.Fuzidate.max.number == 99991231
    assert fzd.Fuzidate.min.number == 10000
    assert fzd.Fuzidate.unknown.number == 0


def test_in_dict():
    {OUTBREAK_FZD: 'outbreak'}


class TestPrecisionOrder:

    @staticmethod
    @pytest.mark.parametrize('prec', [sorted(fzd.Precision)])
    def test_eq(prec):
        assert prec == prec

    @staticmethod
    @pytest.mark.parametrize('index',
                             list(range(len(fzd.Precision))))
    def test_not_eq(index):
        precisions = list(fzd.Precision)
        l = precisions[index]
        r = precisions[(index + 1) % len(fzd.Precision)]
        assert l != r

    @staticmethod
    @pytest.mark.parametrize('index',
                             list(range(len(fzd.Precision) - 1)))
    def test_lt(index):
        precisions = list(fzd.Precision)
        l = precisions[index]
        r = precisions[index + 1]
        assert l < r

    def test_lt_invalid(self):
        with pytest.raises(TypeError):
            fzd.Precision.day < 1


class TestProperties:

    @staticmethod
    def test_number():
        assert OUTBREAK_FZD.number == 19140728

    @staticmethod
    def test_offset():
        assert OUTBREAK_FZD.offset == 0
        assert fzd.Fuzidate.from_int(19140000, 2).offset == 2

    @staticmethod
    def test_year():
        assert OUTBREAK_FZD.year == 1914

    @staticmethod
    def test_year_missing():
        assert fzd.Fuzidate.unknown.year == 0

    @staticmethod
    def test_month():
        assert OUTBREAK_FZD.month == 7

    @staticmethod
    def test_month_missing():
        assert fzd.Fuzidate.from_int(19140000).month == 0

    @staticmethod
    def test_day():
        assert OUTBREAK_FZD.day == 28

    @staticmethod
    def test_day_missing():
        assert fzd.Fuzidate.from_int(19140700).day == 0

    class TestPrecision:

        @staticmethod
        def test_none():
            assert fzd.Fuzidate.unknown.precision is fzd.Precision.none

        @staticmethod
        def test_year():
            assert (fzd.Fuzidate.from_int(19180000).precision
                    is fzd.Precision.year)

        @staticmethod
        def test_month():
            assert (fzd.Fuzidate.from_int(19180700).precision
                    is fzd.Precision.month)

        @staticmethod
        def test_day():
            assert (fzd.Fuzidate.from_int(19180728).precision
                    is fzd.Precision.day)

    class TestIsValid:

        @staticmethod
        def test_true():
            assert OUTBREAK_FZD.is_valid

        @staticmethod
        def test_false():
            assert not fzd.Fuzidate.from_int(1, validate=False).is_valid

    class TestRanges:

        @staticmethod
        @pytest.mark.parametrize('prop', ['high', 'low', 'range'])
        def test_invalid(prop):
            invalid = fzd.Fuzidate.from_int(1, validate=False)
            with pytest.raises(fzd.InvalidFuzidateError):
                getattr(invalid, prop)

        @staticmethod
        def test_range():
            assert OUTBREAK_FZD.range == (OUTBREAK_FZD.high, OUTBREAK_FZD.low)

        class TestHigh:

            @staticmethod
            def test_unknown():
                assert fzd.Fuzidate.unknown.high == datetime.date.max

            @staticmethod
            def test_year():
                year = fzd.Fuzidate.compose(1914)
                assert year.high == datetime.date(1914, 12, 31)

            @staticmethod
            def test_month():
                month = fzd.Fuzidate.compose(1914, 2)
                assert month.high == datetime.date(1914, 2, 28)

            @staticmethod
            def test_month_leap_year():
                month = fzd.Fuzidate.compose(1916, 2)
                assert month.high == datetime.date(1916, 2, 29)

            @staticmethod
            def test_day():
                assert OUTBREAK_FZD.high == datetime.date(1914, 7, 28)

            @staticmethod
            def test_year_offset():
                year = fzd.Fuzidate.compose(1914, offset=5)
                assert year.high == datetime.date(1919, 12, 31)

            @staticmethod
            def test_month_offset():
                year = fzd.Fuzidate.compose(1914, 7, offset=5 + 12 + 2)
                assert year.high == datetime.date(1916, 2, 29)

            @staticmethod
            def test_month_leap_year_offset():
                year = fzd.Fuzidate.compose(1914, 7, offset=5 + (12 * 3) + 2)
                assert year.high == datetime.date(1918, 2, 28)

            @staticmethod
            def test_month_offset_december():
                month = fzd.Fuzidate.compose(1914, 7, offset=17)
                assert month.high == datetime.date(1915, 12, 31)

            @staticmethod
            def test_month_offset_january():
                month = fzd.Fuzidate.compose(1914, 7, offset=18)
                assert month.high == datetime.date(1916, 1, 31)

            @staticmethod
            def test_day_offset():
                assert fzd.Fuzidate.compose(1914, 7, 28, 25).high == (
                    datetime.date(1914, 8, 22))

        class TestLow:

            @staticmethod
            def test_unknown():
                assert fzd.Fuzidate.unknown.low == datetime.date.min

            @staticmethod
            def test_year():
                year = fzd.Fuzidate.compose(1914)
                assert year.low == datetime.date(1914, 1, 1)

            @staticmethod
            def test_month():
                month = fzd.Fuzidate.compose(1914, 7)
                assert month.low == datetime.date(1914, 7, 1)

            @staticmethod
            def test_day():
                assert OUTBREAK_FZD.low == datetime.date(1914, 7, 28)


class TestBool:

    @staticmethod
    def test_true():
        assert OUTBREAK_FZD

    @staticmethod
    def test_false():
        assert not fzd.Fuzidate.unknown

    @staticmethod
    def test_invalid():
        with pytest.raises(fzd.InvalidFuzidateError):
            bool(fzd.Fuzidate.from_int(0, offset=1))


class TestToString:

    @staticmethod
    def test_repr():
        assert repr(fzd.Fuzidate.unknown) == 'Fuzidate.from_int(0)'
        assert repr(OUTBREAK_FZD) == 'Fuzidate.from_int(19140728)'

    class TestStr:

        @staticmethod
        def test_unknown():
            assert str(fzd.Fuzidate.unknown) == '0'

        @staticmethod
        def test_year():
            assert str(fzd.Fuzidate.from_int(19140000)) == '1914'
            assert str(fzd.Fuzidate.from_int(100000)) == '10'

        @staticmethod
        def test_month():
            assert str(fzd.Fuzidate.from_int(19140700)) == '1914-07'

        @staticmethod
        def test_day():
            assert str(fzd.Fuzidate.from_int(19140701)) == '1914-07-01'

        @staticmethod
        def test_invalid_unknown():
            assert (str(fzd.Fuzidate.from_int(0, offset=2, validate=False))
                    == '0+2')

        @staticmethod
        def test_year_offset():
            assert str(fzd.Fuzidate.from_int(19140000, 2)) == '1914+2'
            assert str(fzd.Fuzidate.from_int(100000, 3)) == '10+3'

        @staticmethod
        def test_month_offset():
            assert str(fzd.Fuzidate.from_int(19140700, 2)) == '1914-07+2'

        @staticmethod
        def test_day_offset():
            assert str(fzd.Fuzidate.from_int(19140701, 2)) == '1914-07-01+2'

        @staticmethod
        def test_invalid_missing_year():
            assert (str(fzd.Fuzidate.from_int(701, 2, validate=False))
                    == '0-07-01+2')


class TestParse:

    @staticmethod
    def test_parse_year():
        assert fzd.Fuzidate.parse('1914') == fzd.Fuzidate.from_int(19140000)

    @staticmethod
    def test_parse_month():
        assert fzd.Fuzidate.parse('1914-7') == fzd.Fuzidate.from_int(19140700)

    @staticmethod
    def test_parse_padded_month():
        assert fzd.Fuzidate.parse('1914-07') == fzd.Fuzidate.from_int(19140700)

    @staticmethod
    def test_parse_day():
        assert (fzd.Fuzidate.parse('1914-07-28')
                == fzd.Fuzidate.from_int(19140728))

    @staticmethod
    def test_parse_padded_day():
        assert (fzd.Fuzidate.parse('1914-07-028')
                == fzd.Fuzidate.from_int(19140728))

    @staticmethod
    def test_parse_year_offset():
        assert (fzd.Fuzidate.parse('1914+2')
                == fzd.Fuzidate.from_int(19140000, 2))

    @staticmethod
    def test_parse_month_offset():
        assert (fzd.Fuzidate.parse('1914-7+2')
                == fzd.Fuzidate.from_int(19140700, 2))

    @staticmethod
    def test_parse_day_offset():
        assert (fzd.Fuzidate.parse('1914-07-28+2')
                == fzd.Fuzidate.from_int(19140728, 2))

    @staticmethod
    def test_unparseable():
        with pytest.raises(ValueError, match=r'Fuzidate parse error'):
            fzd.Fuzidate.parse('invalid')

    @staticmethod
    def test_parse_invalid():
        assert (fzd.Fuzidate.parse('1914-07-40+2', validate=False)
                == fzd.Fuzidate.from_int(19140740, 2, validate=False))

    @staticmethod
    def test_check_valid():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Invalid day: 40'):
            fzd.Fuzidate.parse('1914-07-40+2')


class TestFuzidateOrder:

    class TestEq:

        @staticmethod
        def test_invalid_eq_type():
            assert OUTBREAK_FZD != 19140728
            assert 19140728 != OUTBREAK_FZD

        @staticmethod
        def test_is_same():
            assert OUTBREAK_FZD == OUTBREAK_FZD

        @staticmethod
        def test_is_eq():
            assert OUTBREAK_FZD == fzd.Fuzidate.from_int(19140728)

        @staticmethod
        @pytest.mark.parametrize('number', [19181111, 19140700, 19140000, 0])
        def test_is_ne(number):
            assert OUTBREAK_FZD != fzd.Fuzidate.from_int(number)

    class TestLt:

        @staticmethod
        def test_invalid_lt_type():
            with pytest.raises(TypeError):
                assert OUTBREAK_FZD < 19140728
            with pytest.raises(TypeError):
                assert 19140728 < OUTBREAK_FZD

        @staticmethod
        @pytest.mark.parametrize('number', [19140729, 19140800, 19150000])
        def test_is_lt(number):
            assert OUTBREAK_FZD < fzd.Fuzidate.from_int(number)

        @staticmethod
        @pytest.mark.parametrize('number', [19140727, 19140700, 19140000])
        def test_is_ge(number):
            assert OUTBREAK_FZD >= fzd.Fuzidate.from_int(number)


class TestCompose:

    @staticmethod
    def test_default():
        assert fzd.Fuzidate.compose() == fzd.Fuzidate.unknown

    @staticmethod
    def test_year():
        assert fzd.Fuzidate.compose(1914) == fzd.Fuzidate.from_int(19140000)

    @staticmethod
    def test_month():
        assert fzd.Fuzidate.compose(1914, 7) == fzd.Fuzidate.from_int(19140700)

    @staticmethod
    def test_day():
        assert fzd.Fuzidate.compose(1914, 7, 28) == fzd.Fuzidate.from_int(
            19140728)

    @staticmethod
    def test_with_offset():
        assert fzd.Fuzidate.compose(1914, 7, 28, 20) == fzd.Fuzidate.from_int(
            19140728, 20)

    @staticmethod
    def test_year_lt_0():
        fzd.Fuzidate.compose(-1, 7, 28, validate=False)

    @staticmethod
    def test_month_lt_0():
        fzd.Fuzidate.compose(1914, -1, 28, validate=False)

    @staticmethod
    def test_day_lt_0():
        fzd.Fuzidate.compose(1914, 7, -1, validate=False)

    @staticmethod
    def test_check_valid():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Day must not be negative'):
            fzd.Fuzidate.compose(1914, 7, -1)


class TestFromInt:

    @staticmethod
    def test_valid():
        assert fzd.Fuzidate.from_int(19140700, 2) == fzd.Fuzidate.compose(
            1914,
            7,
            offset=2)

    @staticmethod
    def test_invalid():
        assert (fzd.Fuzidate.from_int(-19140700, 2, validate=False) ==
                fzd.Fuzidate.compose(-1915, 93, offset=2, validate=False))

    @staticmethod
    def test_check_valid():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Year must not be negative'):
            fzd.Fuzidate.from_int(-19140700, 2)


class TestCheckValid:

    @staticmethod
    def test_offset_on_unknown():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Unknown fuzidate may not have offset'):
            fzd.Fuzidate.from_int(0, 1).check_valid()

    @staticmethod
    def test_negative_year():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Year must not be negative'):
            fzd.Fuzidate.compose(-1, 7, 28).check_valid()

    @staticmethod
    def test_negative_month():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Month must not be negative'):
            fzd.Fuzidate.compose(1914, -1, 28).check_valid()

    @staticmethod
    def test_negative_day():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Day must not be negative'):
            fzd.Fuzidate.compose(1914, 7, -1).check_valid()

    @staticmethod
    def test_negative_offset():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Offset must not be negative'):
            fzd.Fuzidate.from_int(19140728, -1).check_valid()

    @staticmethod
    def test_day_set():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Day must not be set'):
            fzd.Fuzidate.from_int(19180001).check_valid()

    @staticmethod
    def test_month_set():
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Month must not be set'):
            fzd.Fuzidate.from_int(100).check_valid()

    @staticmethod
    def test_invalid_day():
        invalid = fzd.Fuzidate.compose(1914, 2, 29, validate=False)
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Invalid day: 29'):
            invalid.check_valid()

    @staticmethod
    def test_invalid_day_leap_year():
        invalid = fzd.Fuzidate.compose(1916, 2, 30, validate=False)
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Invalid day: 30'):
            invalid.check_valid()

    @staticmethod
    def test_invalid_month():
        invalid = fzd.Fuzidate.compose(1914, 13, validate=False)
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Invalid month: 13'):
            invalid.check_valid()

    @staticmethod
    def test_invalid_year():
        invalid = fzd.Fuzidate.compose(datetime.date.max.year + 1,
                                       validate=False)
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Invalid year: 10000'):
            invalid.check_valid()

    @staticmethod
    def test_invalid_year_by_offset():
        invalid = fzd.Fuzidate.compose(datetime.date.max.year, offset=1,
                                       validate=False)
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Offset out of range'):
            invalid.check_valid()

    @staticmethod
    def test_invalid_month_by_offset():
        invalid = fzd.Fuzidate.compose(datetime.date.max.year, 12, offset=1,
                                       validate=False)
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Offset out of range'):
            invalid.check_valid()

    @staticmethod
    def test_invalid_day_by_offset():
        invalid = fzd.Fuzidate.compose(datetime.date.max.year, 12, 31,
                                       offset=1, validate=False)
        with pytest.raises(fzd.InvalidFuzidateError,
                           match='Offset out of range'):
            invalid.check_valid()
