"""
A minimalistic server controller for the popular Trackmania racing games.

About scaling
-------------
Despite the limitations of the dedicated server, pymania is scalable under certain conditions:

    - Each instance should use different plugins, because TrackMania callbacks are distributed to
      all connected controllers. While this is not bad, it would have been nice to have a switch to
      use load balancing instead.
    - Certain plugins can be used in all instances ('scalable plugins'), such as remote.
        - All scalable plugins should have a description that they are indeed scalable.
        - Otherwise determine it yourself by looking into the code. Plugins that intercept a lot of
          callbacks to achieve fancy functionality (like a cup plugin or similar) are usually not
          scalable.
"""

import enum

__version__ = '0.1.2'

class ControllerState(enum.Flag):
    """
    Defines combineable controller states.
    """
    #: internal use
    STARTUP = enum.auto()
    #: use for config changes
    RELOAD_CONFIG = enum.auto()
    #: use for plugin code changes
    RELOAD_PLUGINS = enum.auto()
    #: use for shutting down controller
    SHUTDOWN = enum.auto()

class ControllerInterrupt(Exception):
    """
    Raise to manipulate the controller's state. It accepts a combination of :class:`ControllerState`
    flags, e.g. `ControllerState.RELOAD_CONFIG | ControllerState.RELOAD_PLUGINS`.
    """
    def __init__(self, flags, reason):
        super().__init__(str(reason))
        self.flags = flags
