# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import socket
import contextlib
import threading
import pexpect
import pexpect.fdpexpect
from . import utils
from . import pexpect_log


class SerialConsole:
    def __init__(self, *, host, port, timeout):
        logger = logging.getLogger(__name__)
        with utils.StepResultLogger(logger, "Connect to serial console"):
            self._serial_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            try:
                self._serial_socket.connect((host, port))

                self.fdpexpect_handle = pexpect.fdpexpect.fdspawn(
                    self._serial_socket, timeout=timeout
                )
                self._logfile_read = pexpect_log.LogfileRead(logger)
                self.fdpexpect_handle.logfile_read = self._logfile_read
                self.fdpexpect_handle.logfile_send = pexpect_log.LogfileSend(
                    logger
                )
            except:
                self._serial_socket.close()
                raise

    def expect_exact(self, pattern):
        self.fdpexpect_handle.expect_exact(pattern)
        self._logfile_read.log_remaining_text()

    def sendline(self, data):
        self.fdpexpect_handle.sendline(data)

    @contextlib.contextmanager
    def read_in_background(self):
        stop_reading = threading.Event()

        def console_read():
            while not stop_reading.is_set():
                self.fdpexpect_handle.expect_exact(pexpect.TIMEOUT, timeout=0.5)

        thread = threading.Thread(target=console_read)
        thread.start()
        yield
        stop_reading.set()
        thread.join()

    def close(self):
        logger = logging.getLogger(__name__)
        with utils.StepResultLogger(logger, "Close serial console"):
            self.fdpexpect_handle.expect_exact(
                [pexpect.EOF, pexpect.TIMEOUT], timeout=1
            )

            self.fdpexpect_handle.close()
            self._logfile_read.log_remaining_text()
