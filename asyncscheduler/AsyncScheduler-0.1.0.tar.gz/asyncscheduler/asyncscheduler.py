import sched
import threading
from time import time as timefunc


class AsyncScheduler:
    """
    AsyncScheduler is a wrapper for sched.scheduler that provides asynchronous operation out of the box. Thus, starting
    the scheduler does not block the execution of the next statements. Further, adding and removing events can be done
    without manually stopping/starting the scheduler.

    The event itself is executed synchronously. Consequently, it the execution of the calling method takes longer than
    the delay to the next event, execution of the next method is postponed until the previous method returns.
    """
    # usually scheduler is initialized with timefunc=time and
    # delayfunc=sleep. the problem is when using sleep, that if the
    # last event has been removed from scheduler using scheduler.cancel(),
    # the scheduler continues to sleep until the set delay has passed
    # altough no event exists that will be processed. the quick fix for
    # this is to use threading.Event.wait() instead. if Event.set() is
    # never called, the loop in scheduler.run behaves exactly like when
    # using sleep(). But with Event.set() a recalculation of the delay to
    # the next event can always be enforced. Thereafter, if Event.set() is
    # called after scheduler.cancel() the scheduler can adapt to the
    # new situation.

    scheduler = None  # instance of sched.scheduler
    _thread = None  # thread that runs the scheduler
    _delayfunc = None  # delay function for sched.scheduler. using Event instead of sleep enables to interrupt the scheduler
    _stop = None  # stop signal - if set, the AsyncScheduler shuts down

    def __init__(self):
        self._stop = threading.Event()
        self._delayfunc = threading.Event()
        self.scheduler = sched.scheduler(timefunc, self._delayfunc.wait)

    def _run(self):
        """thread method - runs the scheduler until stop signal is set"""
        while not self._stop.is_set():
            self.scheduler.run()
            if self.scheduler.empty():
                # scheduler.run() exits immediately if the event queue is empty.
                # wait until some method call changes the queue
                self._delayfunc.wait()
            self._delayfunc.clear()

    def enterabs(self, time, priority, action, args=(), kwargs={}):
        """
        Add an event to the scheduler. It will be executed at the provided time with 'action(*argument, **kwargs)'.
        In case of two events scheduled for the same time the priority is used for execution order. A lower number
        means a higher priority.

        :param time: call the action at this time stamp.
        :param priority: events scheduled for the same time are processed according to their priority.
        :param action: function that is called upon expirey
        :param args: tuple of arguments for this function
        :param kwargs: dict of arguments for this function
        :return: instance of the event
        """
        event = self.scheduler.enterabs(time, priority, action, argument=args, kwargs=kwargs)
        self._delayfunc.set()
        return event

    def enter(self, delay, priority, action, args=(), kwargs={}):
        """
        Add an event to the scheduler. It will be executed after the provided delay with 'func(*argument, **kwargs)'.
        In case of two events scheduled for the same time the priority is used for execution order. A lower number
        means a higher priority.

        :param delay: delay call of func for this amount of seconds. e.g. 12.34
        :param priority: events scheduled for the same time are processed according to their priority.
        :param action: function that is called upon expirey
        :param args: tuple of arguments for this function
        :param kwargs: dict of arguments for this function
        :return: instance of the event
        """
        event = self.scheduler.enter(delay, priority, action, argument=args, kwargs=kwargs)
        self._delayfunc.set()
        return event

    def cancel(self, event):
        """
        Removes the provided event from the scheduler. In case of an unknown event, a ValueError will be raised.

        :param event: event instance as returned from enter/enterabs.
        """
        self.scheduler.cancel(event)
        self._delayfunc.set()

    def clear_scheduler(self):
        """Cancels all scheduled events."""
        for event in self.scheduler.queue:
            self.scheduler.cancel(event)
        self._delayfunc.set()

    def start(self):
        """Starts the scheduler."""
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name=self.__class__.__name__)
        self._thread.start()

    def stop(self, wait=True):
        """
        Stops the scheduler and clears the event queue.

        :param wait: if set to False, the queue is cleared. otherwise, the method does not return until the last event
        has been triggered.
        """
        self._stop.set()
        if not wait:
            self.clear_scheduler()
        if self.scheduler.empty():
            self._delayfunc.set()
        self._thread.join()

