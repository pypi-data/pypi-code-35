import unittest
from pyquilted.quilted.contact import *


class TestContact(unittest.TestCase):
    def setUp(self):
        self.email = EmailContact('jon.snow@winterfell.got')
        self.phone = PhoneContact('555-123-4567')
        social_dict = {
                "handle": "@jonsnow",
                "sites": ['twitter', 'instagram'],
                "link": "http://github.com/cocoroutine",
                }
        self.social = SocialContact(**social_dict)

    def test_email_contact(self):
        self.assertTrue(hasattr(self.email, 'label'))
        self.assertTrue(hasattr(self.email, 'value'))
        self.assertTrue(hasattr(self.email, 'icons'))
        self.assertTrue(hasattr(self.email, 'link'))

        self.assertIsNotNone(self.email.label)
        self.assertIsNotNone(self.email.value)
        self.assertIsNotNone(self.email.icons)
        self.assertIsNotNone(self.email.link)

        self.assertIsInstance(self.email.icons, list)
        self.assertEqual(self.email.link, 'mailto:jon.snow@winterfell.got')

    def test_phone_contact(self):
        self.assertTrue(hasattr(self.phone, 'label'))
        self.assertTrue(hasattr(self.phone, 'value'))
        self.assertTrue(hasattr(self.phone, 'icons'))
        self.assertTrue(hasattr(self.phone, 'link'))

        self.assertIsNotNone(self.phone.label)
        self.assertIsNotNone(self.phone.value)
        self.assertIsNotNone(self.phone.icons)
        self.assertIsNotNone(self.phone.link)

        self.assertIsInstance(self.phone.icons, list)
        self.assertEqual(self.phone.link, 'tel:+15551234567')

    def test_social_contact(self):
        self.assertTrue(hasattr(self.social, 'label'))
        self.assertTrue(hasattr(self.social, 'value'))
        self.assertTrue(hasattr(self.social, 'icons'))
        self.assertTrue(hasattr(self.social, 'link'))

        self.assertIsNotNone(self.social.label)
        self.assertIsNotNone(self.social.value)
        self.assertIsNotNone(self.social.icons)
        self.assertIsNotNone(self.social.link)

        self.assertIsInstance(self.social.icons, list)


if __name__ == '__main__':
    unittest.main()
