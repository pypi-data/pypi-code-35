from looqbox.objects.tests import ObjForm
from looqbox.objects.tests import LooqObject
import unittest
import json


class TestObjectList(unittest.TestCase):
    """
    Test looq_list file
    """

    def test_instance(self):
        looq_object_form = ObjForm(
            {
                "type": "input", "label": "Loja", "value": "3",
                "name": "loja", "readonly": True
            },
            {
                "type": "input", "label": "Loja2",
                "value": "3", "name": "loja2", "readonly": True
            },
            title="Form"
        )

        self.assertIsInstance(looq_object_form, LooqObject)

    def test_json_creation(self):
        # Testing JSON keys

        looq_object_form = ObjForm(
            {
                "type": "input", "label": "Loja", "value": "3",
                "name": "loja", "readonly": True
            },
            {
                "type": "input", "label": "Loja2",
                "value": "3", "name": "loja2", "readonly": True
            },
            title="Form"
        )

        json_keys = list(json.loads(looq_object_form.to_json_structure).keys())
        self.assertAlmostEqual(json_keys, ["objectType", "title", "method", "action", "filepath", "fields"],
                               msg="Failed basic JSON structure test")


if __name__ == '__main__':
    unittest.main()
