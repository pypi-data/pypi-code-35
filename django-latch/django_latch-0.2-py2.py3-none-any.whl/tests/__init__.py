# pylint: disable=invalid-name
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from latch.models import LatchSetup, UserProfile


class LatchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.latch_setup = LatchSetup.objects.create(
            latch_appid="abcdefghijklmnopqrst",
            latch_secret="abcdefghijklmnopqrstuvwxyzabcdefghijklmno",
        )

        cls.paired_user = User.objects.create_user(
            username="paired", email="paired@mail.com", password="password"
        )

        cls.paired_profile = UserProfile.objects.create(
            user=cls.paired_user,
            latch_accountId="abcdefghijlkmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl",
        )

        cls.unpaired_user = User.objects.create_user(
            username="unpaired", email="unpaired@mail.com", password="password"
        )
