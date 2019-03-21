import sys

from unittest import TestCase

from stackifyapm.handlers.exceptions import get_exception_context
from stackifyapm.handlers.exceptions import get_exception_frames


class TestGetExceptionContextTest(TestCase):

    def setUp(self):
        self.exception = None
        self.traceback = None

        try:
            raise Exception('Sample raised exception')
        except Exception:
            exc_info = sys.exc_info()
            self.exception = exc_info and exc_info[1]
            self.traceback = exc_info and exc_info[2]

    def test_should_create_exception_context(self):
        exception_context = get_exception_context(self.exception, self.traceback)

        assert not exception_context == {}
        assert set(exception_context.keys()) == {'message', 'exception', 'caughtBy', 'timestamp', 'frames'}

    def test_exception_context_should_contain_values(self):
        exception_context = get_exception_context(self.exception, self.traceback)

        assert exception_context['caughtBy'] == 'TestGetExceptionContextTest'
        assert exception_context['exception'] == 'Exception'
        assert exception_context['message'] == 'Sample raised exception'
        assert exception_context['timestamp']
        assert exception_context['frames']


class TestGetExceptionFramesTest(TestCase):

    def setUp(self):
        self.exception = None
        self.traceback = None

        try:
            raise Exception('Sample raised exception')
        except Exception:
            exc_info = sys.exc_info()
            self.exception = exc_info and exc_info[1]
            self.traceback = exc_info and exc_info[2]

    def test_should_return_caught_by(self):
        _, cautht_by = get_exception_frames(self.exception, self.traceback)

        assert cautht_by == 'TestGetExceptionFramesTest'

    def test_should_return_frames(self):
        frames, _ = get_exception_frames(self.exception, self.traceback)

        assert frames
        assert len(frames) == 1

    def test_frames_should_contain_method(self):
        frames, _ = get_exception_frames(self.exception, self.traceback)

        assert len(frames) == 1
        assert 'method' in frames[0].keys()
