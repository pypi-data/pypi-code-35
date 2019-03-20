import logging
import time
from multiprocessing import Pipe, Process, get_context
from rover_position_rjg.data.data import *
from rover_position_rjg.data.data_pump.data_provider import DataProvider
from rover_position_rjg.data.data_pump.data_pump import DataPump


class ProcessDataPump(DataPump[TValue]):
    """A DataPump that spawns a sub-process to read data"""

    HALT_COMMAND = 'halt'
    PAUSE_COMMAND = 'pause'
    RESUME_COMMAND = 'resume'

    def __init__(self,
                 provider_fn: callable(DataProvider[TValue]),
                 data_ready_timeout: float,
                 name: str,
                 initial_samples_to_reject: int = 0,
                 samples_to_reject_on_resume: int = 1
                 ):
        """
        Constructor.
        :param provider_fn: Function that creates the DataProvider this pump will use
        :param data_ready_timeout: timeout when calling DataProvider.poll()
        :param name: displayed in log messages to distinguish this DataPump from any others.
        :param initial_samples_to_reject: number of initial samples to reject. Default 0. Used to get rid
        of dodgy samples from devices that need a while to warm up
        :param samples_to_reject_on_resume: number of samples to reject after resuming from pause
        """
        self.provider_fn = provider_fn
        self._name = name
        self.timeout = data_ready_timeout
        self.receive_pipe, self.send_pipe = Pipe(False)
        self.receive_control_pipe, self.send_control_pipe = Pipe(False)
        self.process: Process = None
        self.samples_to_reject = initial_samples_to_reject
        self.samples_to_reject_on_resume = samples_to_reject_on_resume
        self.logger = logging.getLogger(__name__)

    @property
    def name(self):
        return self._name

    def process_loop(self):
        logging.basicConfig(format='{} %(message)s (PID %(process)d)'.format(self.name), level=logging.INFO)
        self.logger.info("DataPump process started.")
        data_provider = self.provider_fn()  # type: DataProvider[TValue]
        running = True
        paused = False
        try:
            while running:
                if self.receive_control_pipe.poll():
                    command = self.receive_control_pipe.recv()
                    if command[0] == ProcessDataPump.HALT_COMMAND:
                        running = False
                    elif command[0] == ProcessDataPump.PAUSE_COMMAND:
                        paused = True
                    elif command[0] == ProcessDataPump.RESUME_COMMAND:
                        self.samples_to_reject = self.samples_to_reject_on_resume
                        paused = False
                else:
                    if not paused:
                        if data_provider.poll(self.timeout):
                            data = data_provider.get()
                            if self.samples_to_reject > 0:
                                self.samples_to_reject -= 1
                            else:
                                self.send_pipe.send(data)
                            # self.logger.debug("Pumped data at time {} on thread {}".format(data.timestamp, threading.get_ident())
                    else:
                        # Sleep a while to keep the CPU load down
                        time.sleep(max(self.timeout, 0.1))
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            data_provider.close()
        self.logger.info("DataPump process stopped.")
        return 0

    def poll(self, timeout: float) -> bool:
        return self.receive_pipe.poll(timeout)

    def recv(self) -> Data[TValue]:
        return self.receive_pipe.recv()

    def fileno(self) -> int:
        return self.receive_pipe.fileno()

    def run(self):
        if self.process is None:
            # Make sure we run the pump in a separate process
            process_context = get_context('spawn')
            self.process = process_context.Process(target=self.process_loop, daemon=True)
            self.process.start()

    def halt(self):
        if self.process is not None:
            self.send_control_pipe.send([ProcessDataPump.HALT_COMMAND])
            timeout = 2
            self._wait_for_process_to_end(timeout)
            if self.process.is_alive():
                self.logger.info("DataPump process did not stop after {} seconds.")
            self.process = None

    def pause(self):
        if self.process is not None:
            self.send_control_pipe.send([ProcessDataPump.PAUSE_COMMAND])

    def resume(self):
        if self.process is not None:
            self.send_control_pipe.send([ProcessDataPump.RESUME_COMMAND])

    def _wait_for_process_to_end(self, timeout: float):
        """ Waits for the process to exit.
        :param timeout: timeout in seconds
        """
        step = 0.1
        while self.process.is_alive() and timeout > 0:
            timeout = timeout - step
            time.sleep(step)

    def set_frequency(self, frequency: float):
        if self.process is not None:
            self.send_control_pipe.send(['frequency', frequency])
