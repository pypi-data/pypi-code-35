import json

from http.client import HTTPException
from unittest.mock import patch

from django.test import override_settings

from latch.models import LatchSetup, UserProfile
from . import LatchTest

class UnpairingTests(LatchTest):
    def test_pair_form_not_accesible_for_anonymous_user(self):
        response = self.client.get("/pair/")

        self.assertEqual(response.status_code, 302)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_unpair_works_correctly(self, mock_unpair):
        mock_unpair.return_value = {
            json.dumps({})
        }
        data = {"latch_confirm": True}
        self.client.force_login(self.paired_user)
        response = self.client.post("/unpair/", data, follow=True)

        self.assertContains(response, "Latch removed from your account")
        mock_unpair.assert_called_once_with(self.paired_profile.latch_accountId)
        self.assertEqual(UserProfile.objects.filter(user=self.paired_user).count(), 0)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_unpairing_works_when_latch_settings_has_changed(self, mock_unpair):
        mock_unpair.return_value = {
            json.dumps({})
        }

        LatchSetup.objects.all().delete()
        setup = LatchSetup.objects.create(latch_appid="abc", latch_secret="abc")
        setup.save()

        data = {"latch_confirm": True}
        self.client.force_login(self.paired_user)
        response = self.client.post("/unpair/", data, follow=True)

        self.assertContains(response, "Latch removed from your account")
        mock_unpair.assert_called_once_with(self.paired_profile.latch_accountId)
        self.assertEqual(UserProfile.objects.filter(user=self.paired_user).count(), 0)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_show_warning_if_account_is_not_latched(self, mock_unpair):
        data = {"latch_confirm": True}
        self.client.force_login(self.unpaired_user)
        response = self.client.post("/unpair/", data, follow=True)

        self.assertContains(response, "Your account is not latched")
        self.assertEqual(mock_unpair.called, False)

    @override_settings(DEBUG=True)
    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_error_message_shown_when_debug_is_true(self, mock_unpair, mock_status):
        mock_unpair.side_effect = HTTPException("HTTP Generic Exception")
        mock_status.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_confirm": True}
        self.client.force_login(self.paired_user)
        response = self.client.post("/unpair/", data, follow=True)

        self.assertContains(response, "Error unpairing the account: HTTP Generic Exception")

    @override_settings(DEBUG=False)
    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_error_message_hidden_when_debug_is_false(self, mock_unpair, mock_status):
        mock_unpair.side_effect = HTTPException("HTTP Generic Exception")
        mock_status.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_confirm": True}
        self.client.force_login(self.paired_user)
        response = self.client.post("/unpair/", data, follow=True)

        self.assertContains(response, "Error unpairing the account")

    @override_settings(DEBUG=True)
    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_profile_is_not_deleted_if_an_error_occurs(self, mock_unpair, mock_status):
        mock_unpair.side_effect = HTTPException("HTTP Generic Exception")
        mock_status.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_confirm": True}
        self.client.force_login(self.paired_user)
        self.client.post("/unpair/", data, follow=True)

        self.assertEqual(UserProfile.objects.filter(user=self.paired_user).count(), 1)
