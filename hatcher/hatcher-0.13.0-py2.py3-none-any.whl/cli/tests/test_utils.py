#  Copyright (c) 2016, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from datetime import datetime

import pytz

from hatcher.testing import unittest
from hatcher.tests.common import patch
from .. import utils


class TestTimeFormatting(unittest.TestCase):

    def test_time_formatting_western(self):
        # Given
        expected = '2016-07-09 05:29:07 CDT (-0500)'

        def datetime_now(tz=None):
            return datetime(2016, 7, 9, 10, 29, 7, tzinfo=tz)

        time_format = utils.get_timeformat()
        with patch.object(utils, 'datetime') as mock_datetime:
            mock_datetime.now = datetime_now
            with patch('tzlocal.get_localzone') as get_localzone:
                get_localzone.return_value = pytz.timezone('America/Chicago')
                localtime = utils.get_localtime()

        # When
        formatted_date = localtime.strftime(time_format)

        # Then
        self.assertEqual(formatted_date, expected)

    def test_time_formatting_eastern(self):
        # Given
        expected = '2016-06-17 21:52:30 AEST (+1000)'

        def datetime_now(tz=None):
            return datetime(2016, 6, 17, 11, 52, 30, tzinfo=tz)

        time_format = utils.get_timeformat()
        with patch.object(utils, 'datetime') as mock_datetime:
            mock_datetime.now = datetime_now
            with patch('tzlocal.get_localzone') as get_localzone:
                get_localzone.return_value = pytz.timezone('Australia/Sydney')
                localtime = utils.get_localtime()

        # When
        formatted_date = localtime.strftime(time_format)

        # Then
        self.assertEqual(formatted_date, expected)

    def test_time_formatting_utc_fallback(self):
        # Given
        expected = '2016-06-17 11:52:30 UTC (+0000)'

        def datetime_now(tz=None):
            return datetime(2016, 6, 17, 11, 52, 30, tzinfo=tz)

        time_format = utils.get_timeformat()
        with patch.object(utils, 'datetime') as mock_datetime:
            mock_datetime.now = datetime_now
            with patch('tzlocal.get_localzone') as get_localzone:
                get_localzone.side_effect = pytz.UnknownTimeZoneError
                localtime = utils.get_localtime()

        # When
        formatted_date = localtime.strftime(time_format)

        # Then
        self.assertEqual(formatted_date, expected)

    def test_time_formatting_unnamed_timezone(self):
        # Given
        expected = '2016-06-17 13:52:30 +02 (+0200)'

        def datetime_now(tz=None):
            return datetime(2016, 6, 17, 11, 52, 30, tzinfo=tz)

        time_format = utils.get_timeformat()
        with patch.object(utils, 'datetime') as mock_datetime:
            mock_datetime.now = datetime_now
            with patch('tzlocal.get_localzone') as get_localzone:
                # CEST
                get_localzone.return_value = pytz.timezone('Etc/GMT-2')
                localtime = utils.get_localtime()

        # When
        formatted_date = localtime.strftime(time_format)

        # Then
        self.assertEqual(formatted_date, expected)

    def test_time_formatting_half_hour_zone(self):
        # Given
        expected = '2016-06-17 17:22:30 IST (+0530)'

        def datetime_now(tz=None):
            return datetime(2016, 6, 17, 11, 52, 30, tzinfo=tz)

        time_format = utils.get_timeformat()
        with patch.object(utils, 'datetime') as mock_datetime:
            mock_datetime.now = datetime_now
            with patch('tzlocal.get_localzone') as get_localzone:
                get_localzone.return_value = pytz.timezone('Asia/Kolkata')
                localtime = utils.get_localtime()

        # When
        formatted_date = localtime.strftime(time_format)

        # Then
        self.assertEqual(formatted_date, expected)
