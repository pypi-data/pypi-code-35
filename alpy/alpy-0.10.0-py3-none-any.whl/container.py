# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import time
from . import utils


def write_logs(container):

    logger = logging.getLogger("container." + container.short_id)

    def log_each_line(level, lines_bytes):
        if lines_bytes:
            for line in lines_bytes.decode("utf-8").splitlines():
                logger.log(level, line)

    log_each_line(logging.DEBUG, container.logs(stdout=True, stderr=False))
    log_each_line(logging.ERROR, container.logs(stdout=False, stderr=True))


def get_signal_number_from_status_code(code):
    if code >= 128:
        return code - 128
    return None


def log_status_code(code, name):
    logger = logging.getLogger(__name__)
    signal_number = get_signal_number_from_status_code(code)
    if signal_number:
        logger.debug(f"Container {name} was killed by signal {signal_number}")
    else:
        logger.debug(f"Container {name} exited with code {code}")


def check_status_code(code):
    signal_number = get_signal_number_from_status_code(code)
    if signal_number:
        raise utils.NonZeroExitCode(
            f"Container process was killed by signal {signal_number}"
        )
    if code != 0:
        raise utils.NonZeroExitCode(
            f"Container process exited with non-zero code {code}"
        )


def run(container, timeout):

    extra_time_for_shutdown = 15
    logger = logging.getLogger(__name__)

    try:
        container.start()
        try:
            result = container.wait(timeout=timeout)
        except:
            logger.error(
                "Timed out waiting for container "
                + container.short_id
                + " to stop by itself"
            )
            try:
                with utils.StepResultLogger(
                    logger,
                    "Issue stop command for container " + container.short_id,
                ):
                    container.stop()
                with utils.StepResultLogger(
                    logger, f"Wait for container {container.short_id} to stop"
                ):
                    result = container.wait(timeout=extra_time_for_shutdown)
            except:
                write_logs(container)
                raise
            else:
                write_logs(container)
                status_code = int(result["StatusCode"])
                log_status_code(status_code, container.short_id)
            raise
        else:
            write_logs(container)
            status_code = int(result["StatusCode"])
            log_status_code(status_code, container.short_id)
            check_status_code(status_code)
    finally:
        container.remove()


class Timeout(Exception):
    pass


def wait_running(container, timeout):

    time_start = time.time()
    while True:
        container.reload()
        if container.status == "running":
            break
        if time.time() > time_start + timeout:
            raise Timeout
        time.sleep(0.5)
