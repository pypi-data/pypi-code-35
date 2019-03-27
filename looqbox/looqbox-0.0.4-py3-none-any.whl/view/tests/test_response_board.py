import unittest
from looqbox.view.response_board import ResponseBoard
from looqbox.view.response_frame import ResponseFrame
from looqbox.objects.looq_message import ObjMessage
from looqbox.objects.looq_message import LooqObject
import json


class TestResponseFrame(unittest.TestCase):
    """
    Test response_board file
    """

    def test_instance(self):
        board = ResponseBoard()

        self.assertIsInstance(board, LooqObject, msg="Error in object hierarchy")

    def test_json_creation(self):
        # Testing JSON without pass a frame
        board = ResponseBoard()

        mock_json_keys = ['class', 'type', 'dispose', 'action', 'content']

        self.assertEqual(mock_json_keys, list(json.loads(board.to_json_structure).keys()),
                         msg="Failed basic JSON structure test")

        # Testing JSON with other one or more frames
        test_message = ObjMessage("Unit Test Text")
        test_frame_1 = ResponseFrame(content=[test_message])
        test_frame_2 = ResponseFrame(content=[test_message])

        board_1 = ResponseBoard(content=[test_frame_1])
        mock_json_keys = ['class', 'type', 'dispose', 'action', 'content']

        self.assertEqual(1, len(json.loads(board_1.to_json_structure)["content"]),
                         msg="Number of content list is invalid when passed one frame")

        self.assertEqual(mock_json_keys, list(json.loads(board_1.to_json_structure).keys()),
                         msg="Failed basic JSON structure test")

        board_2 = ResponseBoard(content=[test_frame_1, test_frame_2])
        mock_json_keys = ['class', 'type', 'dispose', 'action', 'content']

        self.assertEqual(2, len(json.loads(board_2.to_json_structure)["content"]),
                         msg="Number of content list is invalid when passed two frames")

        self.assertEqual(mock_json_keys, list(json.loads(board_2.to_json_structure).keys()),
                         msg="Failed basic JSON structure test")

    def test_content_integrity(self):
        test_message = ObjMessage("test text")
        test_frame_1 = ResponseFrame(content=[test_message])

        # Testing if content is a list
        board_test_1 = ResponseBoard(content=[test_frame_1])
        self.assertIs(board_test_1 .content.__class__, list, msg="Error in content with correct type")

        board_test_2 = ResponseBoard(content=test_frame_1)
        self.assertIsNot(board_test_2.content.__class__, list, msg="Error in content with incorrect type")

        board_test_3 = ResponseBoard()
        self.assertIs(board_test_3.content.__class__, list, msg="Error in default content type")


if __name__ == '__main__':
    unittest.main()
