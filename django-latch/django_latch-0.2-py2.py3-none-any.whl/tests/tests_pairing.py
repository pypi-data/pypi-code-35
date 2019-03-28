import json

from http.client import HTTPException

from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.test import override_settings

from latch.models import UserProfile, LatchSetup
from latch import latch_sdk_python as sdk

from . import LatchTest


class PairingTests(LatchTest):
    @classmethod
    def setUpTestData(cls):
        cls.latch_off_response = sdk.latchresponse.LatchResponse(
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
        super().setUpTestData()

    def setUp(self):
        # Override the unpaired user to be written on an per-test basis.
        # If not, once we run the test_pairing_with_correct_code
        # tests reliying of unpaired users will fail
        self.unpaired_user = User.objects.create_user(
            username="unpaired_user",
            email="unpaired_user@mail.com",
            password="password",
        )

    def test_pair_form_not_accesible_for_anonymous_user(self):
        response = self.client.get("/pair/")

        self.assertEqual(response.status_code, 302)

    def test_pair_form_shown_in_unpaired_account(self):
        self.client.force_login(self.unpaired_user)
        response = self.client.get("/pair/")

        self.assertEqual(response.status_code, 200)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pairing_with_correct_code(self, mock_pair, mock_status):
        mock_pair.return_value = sdk.latchresponse.LatchResponse(
            json.dumps({"data": {"accountId": "123456"}})
        )

        mock_status.return_value = self.latch_off_response

        data = {"latch_pin": "correc"}
        self.client.force_login(self.unpaired_user)
        response = self.client.post("/pair/", data=data, follow=True)

        self.assertContains(response, "Account paired with Latch")
        user_profile = None
        try:
            user_profile = UserProfile.objects.get(user=self.unpaired_user)
        except ObjectDoesNotExist:
            self.fail("Profile object has not been created")

        self.assertEqual(user_profile.latch_accountId, "123456")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pairing_works_when_latch_settings_has_changed(
        self, mock_pair, mock_status
    ):
        # When we change Latch settings, PK != 1
        # This raises errors in our helper methods.

        mock_pair.return_value = sdk.latchresponse.LatchResponse(
            json.dumps({"data": {"accountId": "123456"}})
        )

        mock_status.return_value = self.latch_off_response

        LatchSetup.objects.all().delete()
        setup = LatchSetup.objects.create(
            latch_appid="abcdefghijklmnopqrst",
            latch_secret="abcdefghijklmnopqrstuvwxyzabcdefghijklmno",
        )
        setup.save()

        data = {"latch_pin": "correc"}
        self.client.force_login(self.unpaired_user)
        response = self.client.post("/pair/", data=data, follow=True)

        self.assertContains(response, "Account paired with Latch")
        user_profile = None
        try:
            user_profile = UserProfile.objects.get(user=self.unpaired_user)
        except ObjectDoesNotExist:
            self.fail("Profile object has not been created")

        self.assertEqual(user_profile.latch_accountId, "123456")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pairing_already_paired_user_shows_error(self, mock_pair, mock_status):
        mock_pair.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": "",
                    "error": {
                        "code": 205,
                        "message": "Account and application already paired",
                    },
                }
            )
        )

        mock_status.return_value = self.latch_off_response

        data = {"latch_pin": "incorr"}
        self.client.force_login(self.paired_user)
        response = self.client.post("/pair/", data=data, follow=True)

        self.assertContains(response, "Account is already paired")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pairing_with_wrong_code_shows_error(self, mock_pair):
        mock_pair.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": "",
                    "error": {"code": 206, "message": "Token not found or expired"},
                }
            )
        )

        data = {"latch_pin": "incorr"}
        self.client.force_login(self.unpaired_user)
        response = self.client.post("/pair/", data=data, follow=True)

        self.assertContains(response, "Account not paired with Latch")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pair_failed(self, mock_pair):
        mock_pair.side_effect = HTTPException("HTTP Generic Exception")
        data = {"latch_pin": "correc"}
        self.client.force_login(self.unpaired_user)
        response = self.client.post("/pair/", data=data, follow=True)

        self.assertContains(response, "Error pairing the account")

    @override_settings(DEBUG=True)
    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_error_message_shown_when_debug_is_true(self, mock_pair, mock_status):
        mock_pair.side_effect = HTTPException("HTTP Generic Exception")
        mock_status.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_pin": "correc"}
        self.client.force_login(self.unpaired_user)
        response = self.client.post("/pair/", data=data, follow=True)

        self.assertContains(
            response, "Error pairing the account: HTTP Generic Exception"
        )

    @override_settings(DEBUG=False)
    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_error_message_hidden_when_debug_is_false(self, mock_pair, mock_status):
        mock_pair.side_effect = HTTPException("HTTP Generic Exception")
        mock_status.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_pin": "correc"}
        self.client.force_login(self.unpaired_user)
        response = self.client.post("/pair/", data=data, follow=True)

        self.assertContains(response, "Error pairing the account")
