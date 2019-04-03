from unittest import TestCase

from vivotool.utils.relationxmltordf import RelationshipTranslator


class RelationshipTranslatorTestSuite(TestCase):

    # relationship document object for testing
    def setUp(self):
        self.translator = RelationshipTranslator()

        self.publication_doc = {
            "@direction": "from",
            "@category": "publication",
            "@id": 3456,
            "api:object": {
                "@id": 3456
            }
        }

        self.user_doc = {
            "@direction": "to",
            "@category": "user",
            "@id": 2345,
            "api:object": {
                "@category": "user",
                "@id": 2345,
                "@username": "username",
                "api:user-identifier-associations": {
                    "api:user-identifier-association": [
                        {
                            "@scheme": "email-address",
                            "#text": "username@vt.edu"
                        }
                    ]
                }
            }
        }

        self.doc = {
            "entry": {
                "api:relationship": {
                    "@id": 1234,
                    "api:related": [self.publication_doc, self.user_doc]
                }
            }
        }

    """Basic test cases."""

    def test_get_user_record(self):
        user_doc = self.translator.get_user_record(self.doc)
        self.assertEqual(user_doc["@category"], "user")

    def test_get_user_email(self):
        self.assertEqual(
            self.translator.get_user_email(
                self.user_doc),
            "username@vt.edu")

    def test_get_user_id(self):
        self.assertEqual(self.translator.get_user_id(self.user_doc), 2345)

    def test_get_username(self):
        self.assertEqual(
            self.translator.get_username(
                self.user_doc), "username")

    def test_get_publication_record(self):
        pub_doc = self.translator.get_publication_record(self.doc)
        self.assertEqual(pub_doc["@category"], "publication")

    def test_get_publication_id(self):
        self.assertEqual(
            self.translator.get_publication_id(
                self.publication_doc), 3456)

    def test_get_authorship_id(self):
        self.assertEqual(self.translator.get_authorship_id(self.doc), 1234)
