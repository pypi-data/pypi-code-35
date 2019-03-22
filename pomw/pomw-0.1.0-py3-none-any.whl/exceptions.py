# -*- python-indent-offset: 4; -*-


class IntervalIDException(Exception):
    def __init__(self):
        super().__init__("Interval ids start with a '@' character.")


class TimewIntervalNotFoundException(Exception):
    def __init__(self, interval):
        super().__init__(
            f"Timewarrior interval: {interval.start_time} - {interval.end_time} does not exist."
        )


class IntervalTimeException(Exception):
    def __init__(self):
        super().__init__("Interval start_time past end_time.")


class IntervalModificationException(Exception):
    def __init__(self):
        super().__init__("Pomodoro intervals cannot be modified.")


class IntervalRangeException(Exception):
    def __init__(self, interval_id):
        super().__init__("Interval @%d does not exist." % (interval_id))


class TaskNotFoundException(Exception):
    def __init__(self, task_id):
        super().__init__("Task id %d could not be found." % (task_id))


class EntryFoundException(Exception):
    def __init__(self, uuid):
        super().__init__("Entry with uuid %s could not be found." % (uuid))


class ArgumentException(Exception):
    def __init__(self, message):
        super().__init__(message)
