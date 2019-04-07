# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import subprocess


class StepResultLogger:
    def __init__(self, logger, description):
        self._logger = logger
        self._description = description

    def __enter__(self):
        self._logger.info(self._description + "...")

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._logger.error(self._description + "... failed")
        else:
            self._logger.info(self._description + "... done")


def step(description):
    return StepResultLogger(logging.getLogger("step"), description)


class NonZeroExitCode(Exception):
    pass


def close_verbose_process(
    *, process, process_name, logger, check=True, timeout
):

    try:
        stdout_data, stderr_data = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.error(f"{process_name} is still running")
        with StepResultLogger(logger, f"Kill {process_name}"):
            process.kill()
            stdout_data, stderr_data = process.communicate()

    for line in stdout_data.splitlines():
        logger.debug("< " + line)

    for line in stderr_data.splitlines():
        logger.error("< " + line)

    return_code = process.returncode

    if return_code >= 0:
        logger.debug(f"{process_name} exited with code {return_code}")
    else:
        logger.debug(
            f"{process_name} " f"was killed by signal {-1 * return_code}"
        )
    if check and return_code > 0:
        raise NonZeroExitCode(
            f"Process {process.args} exited with non-zero code {return_code}"
        )
    if check and return_code < 0:
        raise NonZeroExitCode(
            f"Process {process.args} was killed by signal {-1 * return_code}"
        )

    return return_code
