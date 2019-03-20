from datetime import timedelta
from timeit import default_timer


class Timer:
    _info = None
    elapsed_time = None

    def __init__(self, message: str = '', log_function=print) -> None:
        """
        Initialize the timer.
        :param message: Message and elapsed time is printed, upon timing stop
        :param log_function: Function receives the output message, when timing is stopped
        """
        if not type(message) == str:
            raise TypeError
        self._message = message + ' '
        self._log_function = log_function

    def start(self) -> None:
        """
        Start the timing
        :return:
        """
        self._start = default_timer()  # Use default timer for maximum accuracy

    def stop(self) -> float:
        """
        Stop the timing and put out message
        :return: Elapsed time in seconds
        """

        # Get time difference
        self.elapsed_time = default_timer() - self._start

        # Print result if function is specified
        if self._log_function:
            output = timedelta(seconds=self.elapsed_time)
            self._log_function('%sTIME ELAPSED: %s' % (self._message, output))

        return self.elapsed_time

    def __enter__(self):
        """
        Built-in for with-statement
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Built-in for with-statement
        """
        self.stop()
