import json

from http.client import HTTPException

from unittest.mock import patch

from latch.models import LatchSetup
from latch import latch_sdk_python as sdk

from . import LatchTest


class StatusTest(LatchTest):
    @classmethod
    def setUpTestData(cls):
        cls.latch_response_on = sdk.latchresponse.LatchResponse(
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
        super().setUpTestData()
    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_show_yes_if_latch_is_configured(self, mock_status):
        mock_status.return_value = self.latch_response_on
        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Latch is configured: <b>Yes</b>")

    def test_show_no_if_latch_is_configured(self):
        LatchSetup.objects.get(pk=1).delete()

        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Latch is configured: <b>No</b>")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_tells_if_account_is_paired(self, mock_status):
        mock_status.return_value = self.latch_response_on
        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(
            response,
            "Your accountId is: "
            "<b>abcdefghijlkmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl</b>",
        )

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_tells_if_account_is_not_paired(self, mock_status):
        self.client.force_login(self.unpaired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Your account is <b>not latched</b>")
        self.assertEqual(mock_status.called, False)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_shows_correct_status_when_latch_is_activated(self, mock_status):
        mock_status.return_value = self.latch_response_on

        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Account status: <b>on</b>")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_shows_correct_status_when_latch_is_deactivated(self, mock_status):
        mock_status.return_value = sdk.latchresponse.LatchResponse(
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

        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Account status: <b>off</b>")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_shows_error_message_when_cant_connect_to_latch(self, mock_status):
        mock_status.side_effect = HTTPException("HTTP Generic Exception")

        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Latch connection error")
