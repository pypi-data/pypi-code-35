import unittest
from pyquilted.builder.contacts import ContactsBuilder
from pyquilted.yaml_loader import YamlLoader


class TestBuilderContacts(unittest.TestCase):
    def test_mapper_contacts(self):
        with open('test/validations/contacts.yml') as f:
            data = YamlLoader.ordered_load(f)
        mapper = ContactsBuilder(data['contacts'])
        contacts = mapper.deserialize()

        valid = [
                {
                    'label': 'email',
                    'value': 'jon.snow@winterfell.got',
                    'icons': ['fa-envelope'],
                    'link': 'mailto:jon.snow@winterfell.got'
                },
                {
                    'label': 'phone',
                    'value': '555-123-4567',
                    'icons': ['fa-phone'],
                    'link': 'tel:+15551234567'
                },
                {
                    'label': 'social',
                    'value': '@jonsnowEGOT',
                    'icons': ['fa-twitter', 'fa-instagram'],
                    'link': None 
                }
                ]
        self.assertEqual(contacts.serialize(), valid)


if __name__ == '__main__':
    unittest.main()
