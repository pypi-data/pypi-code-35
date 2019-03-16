class KTDKError(Exception):
    def __init__(self, msg: str = None, **kwargs):
        super().__init__(**kwargs)
        self.msg = msg


class KTDKAssertionError(KTDKError):
    pass


class RequireFailedError(KTDKAssertionError):
    pass


class KillCheckError(KTDKAssertionError):
    pass


class RequiredTaskFailed(KTDKAssertionError):
    pass


class TaskRunFailed(KTDKError):
    pass
