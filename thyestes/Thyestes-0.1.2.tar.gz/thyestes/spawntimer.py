from thyestes.acontroller import AController
from thyestes.timer import Timer
from collections import deque


class SpawnTimer(AController):
    _timer_list = None

    def __init__(self, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger)

        self._timer_list = deque()
        self._logger.info("SpawnTimer.__init__ - finished constructor")

    def _update_timer(self):
        self._logger.info("SpawnTimer._update_timer - adding new timer to deque")
        timer = Timer(self._timer_event, self._stop_timer, self._logger)
        timer.set_timer(self._timer_value)
        self._timer_list.append(timer)
        self._logger.info("SpawnTimer._update_timer - active timer: {}.".format(len(self._timer_list)))

    def _timer_event(self):
        self._logger.info("SpawnTimer._timer_event")
        self._purge_deque()
        self._publish_timer_message()

    def _purge_deque(self):
        """
        purge the deque from all stopped timers.

        notable behavior: the current timer, that fired _timer_event has reached its timeout but has not been stopped
        yet. in fact, i can only be closed after this method has been processed. thus, it will be in this list until the
        next timer fires and _purge_deque is called again. concluding, after the first timer has been created, this
        deque will always have at least on entry.
        """
        self._logger.info("SpawnTimer._purge_deque - removing all stopped timer")
        i = 0
        while len(self._timer_list) > 0 and self._timer_list[0].is_stopped.is_set():
            self._logger.debug("SpawnTimer._purge_deque - removing timer")
            self._timer_list.popleft()
            i+=1
        self._logger.info("SpawnTimer._purge_deque - removed {} expired timer from list (remaining timer: {})".
                          format(i, len(self._timer_list)))

    def _start(self):
        pass

    def _stop(self):
        while len(self._timer_list) > 0:
            self._timer_list[0].is_stopped.wait()
            self._purge_deque()






