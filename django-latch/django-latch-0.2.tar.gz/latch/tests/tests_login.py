import json

from http.client import HTTPException
from unittest.mock import MagicMock, patch
from django.test import override_settings

from latch import latch_sdk_python as sdk
from . import LatchTest

ON_MOCK = MagicMock(
    return_value=sdk.latchresponse.LatchResponse(
        json.dumps(
            {
                "data": {
                    "operations": {
                        "abcdefghijklmnopqrst": {
                            "status": "on",
                            "operations": {"status": "on"},
                        }
                    }
                }
            }
        )
    )
)

OFF_MOCK = MagicMock(
    return_value=sdk.latchresponse.LatchResponse(
        json.dumps(
            {
                "data": {
                    "operations": {
                        "abcdefghijklmnopqrst": {
                            "status": "off",
                            "operations": {"status": "off"},
                        }
                    }
                }
            }
        )
    )
)

ERR_MOCK = MagicMock(
    side_effect=HTTPException("Generic HTTP Exception")
)


@patch("latch.latch_sdk_python.latchapp.LatchApp.status", new=ON_MOCK)
class LoginPairedUserLatchOnTest(LatchTest):
    def test_login_correct_when_latch_is_on_with_good_credencials(self):
        self.assertEqual(
            self.client.login(username="paired", password="password"), True
        )

    def test_login_incorrect_when_latch_is_on_with_wrong_credencials(self):
        self.assertEqual(self.client.login(username="paired", password="wrong"), False)


@patch("latch.latch_sdk_python.latchapp.LatchApp.status", new=OFF_MOCK)
class LoginPairedUserLatchOffTest(LatchTest):
    def test_login_incorrect_when_latch_is_off_with_good_credentials(self):
        self.assertEqual(
            self.client.login(username="paired", password="password"), False
        )

    def test_login_incorrect_when_latch_is_off_with_wrong_credentials(self):
        self.assertEqual(self.client.login(username="paired", password="wrong"), False)


@patch("latch.latch_sdk_python.latchapp.LatchApp.status")
class LoginUnpairedUserTest(LatchTest):
    def test_login_correct_with_good_credentials(self, mock_status):
        self.assertEqual(
            self.client.login(username="unpaired", password="password"), True
        )
        self.assertEqual(mock_status.called, False)

    def test_login_incorrect_with_wrong_credentials(self, mock_status):
        self.assertEqual(
            self.client.login(username="unpaired", password="wrong"), False
        )
        self.assertEqual(mock_status.called, False)

@patch("latch.latch_sdk_python.latchapp.LatchApp.status", new=ERR_MOCK)
class LoginWithLatchUnreachable(LatchTest):
    @override_settings(LATCH_BYPASS_WHEN_UNREACHABLE=True)
    def test_login_correct_when_bypass_activated(self):
        self.assertEqual(
            self.client.login(username="paired", password="password"), True
        )

    @override_settings(LATCH_BYPASS_WHEN_UNREACHABLE=False)
    def test_login_correct_when_bypass_deactivated(self):
        self.assertEqual(
            self.client.login(username="paired", password="password"), False
        )

    def test_login_correct_when_bypass_has_no_value(self):
        self.assertEqual(
            self.client.login(username="paired", password="password"), True
        )
