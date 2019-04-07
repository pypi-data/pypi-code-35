from time import time
from pelops.mythreading import LoggerThread
import threading


class Timer:
    _logger = None

    _target_reached_handler = None

    _target_time = None
    target_reached = None
    _timer_thread = None
    _thread_lock = None
    is_stopped = None
    _is_running = None

    _stop_signal = None

    def __init__(self, timeout_method, stop_signal, logger):
        self._target_reached_handler = timeout_method
        self._logger = logger

        self._stop_signal = stop_signal

        self.is_stopped = threading.Event()
        self._is_running = threading.Event()
        self._logger.debug("Timer._timer - is_stopped.set")
        self.is_stopped.set()
        self._logger.debug("Timer._timer - _is_running.clear")
        self._is_running.clear()

        self._timer_thread = None
        self.target_reached = False
        self._thread_lock = threading.Lock()

        self._logger.info("Timer.__init__ - created timer")

    def _get_time_diff(self):
        now = time()
        diff = max(0, self._target_time - now)
        self._logger.debug("Timer._get_time_diff - target time: '{}', now: '{}', diff: '{}'".
                           format(self._target_time, now, diff))
        return diff

    def _timer(self):
        self._logger.debug("Timer._timer - is_stopped.clear")
        self.is_stopped.clear()
        self._logger.debug("Timer._timer - _is_running.set")
        self._is_running.set()

        diff = self._get_time_diff()
        while not self.target_reached and not self._stop_signal.is_set():
            self._logger.info("Timer._timer - waiting '{}' seconds.".format(diff))
            self._stop_signal.wait(diff)
            diff = self._get_time_diff()
            if diff == 0:
                self._logger.info("Timer._timer - timeout")
                self.target_reached = True
                self._target_reached_handler()
            elif not self._stop_signal.is_set():
                self._logger.info("Timer._timer - new targettime applied. waiting {} seconds.".format(diff))
            else:
                self._logger.info("Timer._timer - stop signal")

        self._logger.debug("Timer._timer - _is_running.clear")
        self._is_running.clear()
        self._logger.debug("Timer._timer - is_stopped.set")
        self.is_stopped.set()

    def _start_timer(self):
        self._logger.info("Timer._start_timer - acquiring lock")
        with self._thread_lock:
            if self.is_stopped.is_set():
                self._logger.info("Timer._start_timer - starting timer")
                self.target_reached = False
                self._timer_thread = LoggerThread(target=self._timer, name="timer", logger=self._logger)
                self._timer_thread.start()
                self._is_running.wait()
            else:
                self._logger.info("Timer._start_timer - timer already running")

    def set_timer(self, timer_value):
        self._target_time = time() + timer_value
        self._logger.info("Timer.set_timer - waiting '{}' -> set target time to:'{}'.".
                          format(timer_value, self._target_time))
        self._start_timer()
