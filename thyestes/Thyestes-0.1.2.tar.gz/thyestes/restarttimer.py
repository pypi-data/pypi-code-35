from thyestes.acontroller import AController
from thyestes.timer import Timer


class RestartTimer(AController):
    _timer = None

    def __init__(self, config, mqtt_client, logger):
        AController.__init__(self, config, mqtt_client, logger)

        self._timer = Timer(self._publish_timer_message, self._stop_timer, self._logger)
        self._logger.info("RestartTimer.__init__ - finished constructor")

    def _update_timer(self):
        self._timer.set_timer(self._timer_value)

    def _start(self):
        pass

    def _stop(self):
        self._timer.is_stopped.wait()




