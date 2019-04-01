import os
from typing import List
from multiprocessing import Process
from signal import (
    SIGTERM,
    SIGINT,
    signal as signal_func,
    Signals
)

from macrobase_driver import MacrobaseDriver

from structlog import get_logger

log = get_logger('macrobase_pool')


class DriversProccesesPool:

    class Signal:
        stopped = False

    def __init__(self):
        self._processes = []

    def _serve(self, driver: MacrobaseDriver):
        return driver.run()

    def _add(self, drivers: List[MacrobaseDriver]):
        def sig_handler(signal, frame):
            pid = None
            f_locals_self = frame.f_locals.get('self')

            if f_locals_self is not None and hasattr(f_locals_self, 'pid'):
                pid = f_locals_self.pid

            signals = Signals(signal)

            if signals.name == 'SIGINT':
                log.debug(f'User has stop process {pid}. Shutting down.')
            elif signals.name == 'SIGTERM':
                log.debug(f'Process has stop process {pid}. Shutting down.')
            else:
                log.debug(f'Received unknown signal {signals.name} from proccess {pid}. Shutting down.')

            for process in self._processes:
                os.kill(process.pid, SIGINT)

            exit()

        signal_func(SIGINT, lambda s, f: sig_handler(s, f))
        signal_func(SIGTERM, lambda s, f: sig_handler(s, f))

        for driver in drivers:
            process = Process(
                target=self._serve,
                kwargs={
                    'driver': driver
                },
            )
            # process.daemon = True
            self._processes.append(process)

    def start(self, drivers: List[MacrobaseDriver]):
        self._add(drivers)

        for process in self._processes:
            process.start()
            log.debug(f'Process {process.pid} started')

        self.join_and_terminate()

    def join_and_terminate(self):
        for process in self._processes:
            process.join()

        self.terminate()

    def terminate(self):
        # the above processes will block this until they're stopped
        for process in self._processes:
            process.terminate()
