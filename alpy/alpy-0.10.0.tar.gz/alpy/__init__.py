# SPDX-License-Identifier: GPL-3.0-or-later

import atexit
import contextlib
import logging
import pathlib
import sys


class ContextBase:
    def __init__(self):
        self._exit_stack = contextlib.ExitStack()

    def __enter__(self):
        with self._exit_stack:
            result = self._main()
            self._exit_stack = self._exit_stack.pop_all()
            return result

    def __exit__(self, exc_type, exc_value, traceback):
        self._exit_stack.close()

    def _main(self):
        raise NotImplementedError


class ContextWithTestResult(ContextBase):
    def __init__(self):
        test_name = pathlib.Path(sys.argv[0]).resolve().parent.name
        self._logger = logging.getLogger(test_name)
        self._logger.info("Starting test")
        super().__init__()
        self._test_passed = False
        atexit.register(self._print_test_result)

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

        if not exc_type:
            self._test_passed = True

    def _print_test_result(self):
        if self._test_passed:
            self._logger.info("Test passed")
        else:
            self._logger.error("Test failed")

    def _main(self):
        raise NotImplementedError
