import unittest
from pyquilted.quilted.contact import *
from pyquilted.quilted.contacts_list import ContactsList
from pyquilted.quilted.heading_simple import HeadingSimple
from pyquilted.quilted.education import Education
from pyquilted.quilted.resume import Resume


class TestResume(unittest.TestCase):
    def test_resume(self):
        resume = Resume()
        self.assertIsInstance(resume.contacts, list)
        self.assertIsInstance(resume.sections, list)
        self.assertIsInstance(resume.style, dict)

    def test_add_heading(self):
        heading = HeadingSimple(name="Jon Snow")
        resume = Resume()
        resume.add_section(heading)

        self.assertIsNotNone(resume.heading)

    def test_add_contacts(self):
        email = EmailContact('jon.snow@winterfell.got')
        contacts = ContactsList()
        contacts.append(email)
        resume = Resume()
        resume.add_section(contacts)
        valid = [
                {
                    'label': 'email',
                    'value': 'jon.snow@winterfell.got',
                    'icons': ['fa-envelope'],
                    'link': 'mailto:jon.snow@winterfell.got'
                }
                ]
        self.assertIsInstance(resume.contacts, list)
        self.assertIsInstance(resume.contacts[0], dict)
        self.assertEqual(resume.contacts, valid)

    def test_add_section(self):
        education = Education('The Night\'s Watch')
        resume = Resume()
        resume.add_section(education)
        valid = [
                {
                    "education": {
                        "label": "Education",
                        "value": "The Night's Watch",
                        "icon": "fa-graduation-cap"
                    }
                }
                ]
        self.assertIsInstance(resume.sections, list)
        self.assertIsInstance(resume.sections[0], dict)
        self.assertEqual(resume.sections, valid)


if __name__ == '__main__':
    unittest.main()
