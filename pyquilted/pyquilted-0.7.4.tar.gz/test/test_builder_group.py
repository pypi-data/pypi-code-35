import unittest
from pyquilted.builder.group import GroupBuilder


class TestBuilderGroup(unittest.TestCase):
    def setUp(self):
        self.builder = GroupBuilder(resume=MockResumePositive())

    def test_builder_group(self):
        self.assertTrue(hasattr(self.builder, 'resume'))
        self.assertTrue(callable(self.builder.create))

    def test_builder_create_postive(self):
        self.assertEqual(len(self.builder.resume.sections), 5)
        resume = self.builder.create()
        self.assertEqual(len(resume.sections), 3)

    def test_builder_create_negative(self):
        builder_neg = GroupBuilder(resume=MockResumeNegative())
        self.assertEqual(len(builder_neg.resume.sections), 4)
        resume = builder_neg.create()
        self.assertEqual(len(resume.sections), 4)


class MockResumePositive:
    def __init__(self):
        self.sections = [
                {"section1": {
                    "label": "E1",
                    "compact": False,
                    "value": "some text"
                }},

                {"section2": {
                    "label": "C1",
                    "compact": True,
                    "value": "some text"
                }},
                {"section3": {
                    "label": "C2",
                    "compact": True,
                    "value": "some text"
                }},
                {"section4": {
                    "label": "C3",
                    "compact": True,
                    "value": "some text"
                }},
                {"section5": {
                    "label": "E2",
                    "compact": False,
                    "value": "some text"
                }}]


class MockResumeNegative:
    def __init__(self):
        self.sections = [
                {"section1": {
                    "label": "C1",
                    "compact": True,
                    "value": "some text"
                }},
                {"section2": {
                    "label": "E1",
                    "compact": False,
                    "value": "some text"
                }},
                {"section3": {
                    "label": "E2",
                    "compact": False,
                    "value": "some text"
                }},
                {"section4": {
                    "label": "C2",
                    "compact": True,
                    "value": "some text"
                }}]


if __name__ == '__main__':
    unittest.main()
