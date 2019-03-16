from hippodamia_agent.states.aagentstate import AAgentState


class Terminating(AAgentState):
    send_offboarding_message = None

    def __init__(self, logger, history):
        AAgentState.__init__(self, logger, history, None)

    def _on_entry(self):
        self.send_offboarding_message()
        return None

    def _on_exit(self):
        pass
