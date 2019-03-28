import json

from unittest.mock import patch

from . import LatchTest

class SignalsTests(LatchTest):
    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_signals_gets_called_before_delete(self, mock_unpair):
        mock_unpair.return_value = {
            json.dumps({})
        }

        self.paired_user.delete()
        mock_unpair.assert_called_once_with(self.paired_profile.latch_accountId)
