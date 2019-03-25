from state import * 
class {{ state }}(State):
    def __init__(self):
        self.name = "{{ state }}"
        self.description = "{{ description }}"
        self.definition = {}

    """
    Auto gen prototypes of transitions
    """

