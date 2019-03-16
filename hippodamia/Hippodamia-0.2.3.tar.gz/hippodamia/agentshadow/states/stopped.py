from hippodamia.agentshadow.states.amonitoringstate import AMonitoringState
from hippodamia.enums import Health


class Stopped(AMonitoringState):
    func_deactivate_recv_messages = None

    def __init__(self, update_available, set_health, reset_max_level, logger):
        AMonitoringState.__init__(self, update_available, set_health, Health.RED, reset_max_level,
                                  logger, __class__.__name__)

    def _on_entry(self):
        self.func_deactivate_recv_messages()
        self.reset_max_level()

        return None

    def _on_exit(self):
        pass
