import unittest
from pyquilted.quilted.contact import *
from pyquilted.quilted.contact_factory import ContactFactory


class TestContactsFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ContactFactory()

    def test_contact_factory(self):
        self.assertTrue(hasattr(self.factory, 'create'))

    def test_contact_factory_email(self):
        email = self.factory.create('email', 'test@test.com')
        self.assertIsInstance(email, EmailContact)

    def test_contact_factory_phone(self):
        phone = self.factory.create('phone', '123456789')
        self.assertIsInstance(phone, PhoneContact)

    def test_contact_factory_social(self):
        social = self.factory.create('social',
                {'handle':'@jonsnow', 'sites':['twitter']})
        self.assertIsInstance(social, SocialContact)


if __name__ == '__main__':
    unittest.main()
