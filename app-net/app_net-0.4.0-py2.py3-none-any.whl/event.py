# -*- coding: utf-8 -*-
"""
Event Module
------------

Contains the event decorator and should have nothing else.
"""

__all__ = [
    'event'
]

# std imports
from functools import wraps

# package imports
import net


def event(name):
    """
    Registers a function as an event trigger. Event triggers are hooks into the
    event system between peers. Peers that ``net.subscribe`` to a peer, register
    an event on that peer.

    Lets say PeerA subscribes to an event on PeerB using the following code.

    .. code-block:: python

        # code on PeerA

        peerB_id = "peerb"

        @net.subscribe("doing_something")
        def handleEvent(whatPeerBDid):
            ...do something

    The subscribe decorator has communicated with PeerB and registered itself as
    on the list of peer to update if "doing_something" is ever triggered. On
    PeerB's side we have the following.

    .. code-block:: python

        # code on PeerB

        @net.event("doing_something")
        def imDoingSomething(*args, **kwargs):
            return args, kwargs

    .. note::

        All functions flagged as an event MUST return args and kwargs exactly as
        displayed above.

    Now lets say in PeerB we want to trigger the event in a for loop and have it
    hand off the values to all the subscribed peers, PeerA in this case.

    .. code-block:: python

        for i in range(0, 10):
            imDoingSomething(i)  # <- this will notify PeerA and pass the value of 'i'.

    Keep in mind, you can have any number of peers subscribe to any kind of
    event. So if we had 5 peers subscribe to PeerB they would all be passed this
    value at runtime.

    Lastly, these event functions act as a buffer between the runtime code of
    your application and the delivery of the content to the peer. For example:

    .. code-block:: python

        var = MyCustomObject()  # some JSON incompatible object

        ...do a bunch of delivery prep and muddy up the application code...

        imDoingSomething(var)

    Instead

    .. code-block:: python

        @net.event("doing_something")
        def imDoingSomething(*args, **kwargs):

            obj = args[0]

            ...clean and prepare for transit here...

            args[0] = cleanedObj

            return args, kwargs

    As you can see, these functions act as a hook into the delivery system when
    the event is triggered.

    There are protections put in place to try to prevent the peer that triggered
    the event to be blocked by a bad handle on the subscribed peer. For the
    purpose of protecting the event triggering peer from remote errors, all
    connection errors and remote runtime errors will be caught and logged. But
    nothing will halt the running application.

    i.e. event -> remote peer errors -> event peer will log and ignore

    Stale peer subscriptions will be added to the stale list and pruned. Since
    the subscriptions are created per client request, the event peer will not
    know until a request is made that the subscribed peer went offline.
    """
    def wrapper(func):
        @wraps(func)
        def interface(*args, **kwargs):

            new_args, new_kwargs = func(*args, **kwargs)
            net.Peer().trigger_event(name, *new_args, **new_kwargs)

            return new_args, new_kwargs
        return interface
    return wrapper
