from latch.models import LatchSetup

from . import LatchTest


class UnconfiguredTest(LatchTest):
    def setUp(self):
        super().setUp()
        LatchSetup.objects.get(pk=1).delete()

    def test_pair_form_shows_unconfigured_latch_warning(self):
        self.client.force_login(self.paired_user)
        response = self.client.get("/pair/", follow=True)

        self.assertContains(response, "Latch is not configured")

    def test_unpair_form_shows_unconfigured_latch_warning(self):
        self.client.force_login(self.paired_user)
        response = self.client.get("/unpair/", follow=True)

        self.assertContains(response, "Latch is not configured")

    def test_status_shows_unconfigured_latch_warning(self):
        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Latch is configured: <b>No</b>")
