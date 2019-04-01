from copy import copy
from functools import partial

def default_cost(cost=0):
    def _inner_cost(func):
        func.default_cost = cost
        return func
    return _inner_cost


def task(cost):
    def _construct_task(func):
        return construct_task(func, cost)
    return _construct_task


def construct_task(func, default_cost=1):
    '''
    Constructs a task from a function.
    A task is a function object with the attribute `is_task` set to True.
    If the function provided has a duration (or "cost") associated with it, it will run once per `cost` invocations.
    A task has an attribute, `completed`, which will be False unless the target function has just executed.
    :param func: the function to be transformed into a task. Cost is added to this function via the default_cost decorator.
    :return: A Task, which is a function object which may run every `cost` invocations.
    '''
    func = copy(func)

    # Mutable value here lets us break out of `invoker`'s closure. Format is [expected_duration, ticks_passed]
    completion_status = [0, 0]
    def max_ticks(): return completion_status[0]
    def ticks_passed(): return completion_status[1]
    def sufficient_time_passed(): return ticks_passed() >= max_ticks()
    def just_ran(): return completion_status[1] is 0

    # If there's no cost set up, just run the target function, but remember to set func.completed to True when we do.
    if 'default_cost' not in dir(func):
        func.cost = default_cost
    # We rename `default_cost` to `cost` here, so that invoker gets `invoker.cost` when we set `invoker.func_dict` later
    else:
        func.cost = func.default_cost

    # The function has a cost associated with it, so only run after a limited number of invocations.
    completion_status[0] = func.cost

    def invoker(*args, **kwargs):
        completion_status[1] += min(func.cost, 1)

        if sufficient_time_passed():
            completion_status[1] -= completion_status[0]
            return func(*args, **kwargs)

        # Didn't return function result; must not have enough invocations yet.
        return None

    invoker.invocations = completion_status[1]
    invoker.just_ran = just_ran
    invoker.func_name = func.func_name
    invoker.func_dict = func.func_dict
    return invoker

class ListenerTracker(object):
    def __init__(self,
                 ticks_passed_since_added=0,
                 total_ticks_performed=0):
        self.ticks_passed_since_added = ticks_passed_since_added
        self.total_ticks_performed = total_ticks_performed


class Clock(object):
    def __init__(self, max_ticks=-1):
        self.max_ticks = max_ticks  # -1 => runs indefinitely
        self.ticks_passed = 0
        self.listeners = {}

    @property
    def time_exhausted(self):
        if self.max_ticks is None:
            return False
        return self.ticks_passed >= self.max_ticks and self.max_ticks is not -1

    def add_listener(self, actor):
        # We need things to be able to `perform()` so we can `tick()` properly.
        if 'yield_tasks' not in dir(actor):
            class BadListenerException(Exception):
                pass
            raise BadListenerException("Listener provided must adhere to the actor spec expected; specifically, it should have a `perform()` method which returns a generator of functions.")

        self.listeners[actor.yield_tasks()] = ListenerTracker()

    def tick(self, ticks_remaining=None):
        '''
        Allow time to pass for the actors attached to this clock
        :param ticks_remaining: The number of ticks to pass. If None, ticks until max_ticks passed.
        Note that if max_ticks is None and ticks_remaining is None, simulation runs indefinitely.
        Default: None.
        :return: None.
        '''
        if ticks_remaining is None:
            ticks_remaining = self.max_ticks
            
        while not self.time_exhausted and ticks_remaining is not 0:
            for actor_task, actor_time_tracker in self.listeners.items():
                actor_time_tracker.ticks_passed_since_added += 1
                while actor_time_tracker.ticks_passed_since_added > actor_time_tracker.total_ticks_performed:
                    new_task = next(actor_task)
                    new_task()

                    # Assume a task with no cost has zero cost (i.e. not a task)
                    if not hasattr(new_task, 'cost'):
                        ticks_just_passed = 0
                    else:
                        ticks_just_passed = min(new_task.cost, 1)

                    actor_time_tracker.total_ticks_performed += ticks_just_passed

            self.ticks_passed += 1
            ticks_remaining -= 1
