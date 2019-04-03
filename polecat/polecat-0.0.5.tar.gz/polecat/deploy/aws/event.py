from ..event import Event


class LambdaEvent(Event):
    def __init__(self, event):
        super().__init__(event)

    def is_http(self):
        return True
