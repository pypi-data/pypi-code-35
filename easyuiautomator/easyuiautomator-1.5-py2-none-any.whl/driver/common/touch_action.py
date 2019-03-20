# coding=utf-8
"""
Created on 2015年11月5日

@author: thomas.ning
"""
import copy
from easyuiautomator.driver.common.mobilecommand import MobileCommand as Command


class TouchAction(object):
    """
    used to complex command
    """
    def __init__(self, driver=None):
        self._driver = driver
        self._actions = []
        self._id = None
        self._x = 0.0
        self._y = 0.0

    def tap(self, element=None, x=None, y=None, count=1):
        """
        Perform a tap action on the element

        :Args:
         - element - the element to tap
         - x - (optional) x coordinate to tap, relative to the top left corner of the element.
         - y - (optional) y coordinate. If y is used, x must also be set, and vice versa

        :Usage:
        """
        opts = self._get_opts(element, x, y)
        opts['count'] = count
        self._add_action('tap', opts)
        return self

    def press(self, el=None, x=None, y=None):
        """
        Begin a chain with a press down action at a particular element or point
        """
        self._add_action('press', self._get_opts(el, x, y))
        return self

    def long_press(self, el=None, x=None, y=None, duration=1000):
        """
        Begin a chain with a press down that lasts `duration` milliseconds
        """
        self._add_action('longPress', self._get_opts(el, x, y, duration))
        return self

    def wait(self, ms=0):
        """
        Pause for `ms` milliseconds.
        """
        if ms is None:
            ms = 0
        opts = {'ms': ms}
        self._add_action('wait', opts)
        return self

    def move_to(self, el=None, x=None, y=None):
        """
        Move the pointer from the previous point to the element or point specified
        """
        self._add_action('moveTo', self._get_opts(el, x, y))
        return self

    def release(self):
        """
        End the action by lifting the pointer off the screen
        """
        self._add_action('release', {'id':self._id,'x':self._x, 'y':self._y})
        return self

    def perform(self):
        """
        Perform the action by sending the commands to the server to be operated upon
        """
        params = {'actions': self._actions}
        self._driver._execute(Command.TOUCH_ACTION, params)
        # get rid of actions so the object can be reused
        self._actions = []
        return self

    @property
    def json_wire_gestures(self):
        gestures = []
        for action in self._actions:
            gestures.append(copy.deepcopy(action))
        return gestures

    def _add_action(self, action, options):
        gesture = {
            'action': action,
            'options': options,
        }
        self._actions.append(gesture)

    def _get_opts(self, element, x, y, duration=None):
        opts = {}
        if element is not None:
            opts['id'] = element.id
            self._id = element.id
        # it makes no sense to have x but no y, or vice versa.
        if x is None or y is None:
            x, y = None, None
        opts['x'] = x
        opts['y'] = y
        self._x = x
        self._y = y
        if duration is not None:
            opts['duration'] = duration
        return opts
