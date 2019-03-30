# coding=utf-8
import time

'''
 :Description:    控件类
 :author          80071482/bony
 :@version         V1.1
 :@Date            2017年05月
'''


class Element(object):
    def __init__(self, x=None, y=None, device=None):
        self.TEXT = None
        self.BOUND = None
        self.X_COORDINATE = x
        self.Y_COORDINATE = y
        self._device_ = device
        self._WIDTH = None
        self._HIGH = None

    def init_screen_size(self):
        self._WIDTH = int(self.BOUND[2]) - int(self.BOUND[0])
        self._HIGH = int(self.BOUND[3]) - int(self.BOUND[1])

    def get_width(self):
        """
        获取元素宽度
        """
        return self._WIDTH

    def get_high(self):
        """
        获取元素高度
        """
        return self._HIGH

    def click(self):
        self._device_.click(self.X_COORDINATE, self.Y_COORDINATE)

    def input(self, text):
        self.click()
        time.sleep(1)
        self._device_.input(text)

    def long_click(self):
        self._device_.longPress(self.X_COORDINATE, self.Y_COORDINATE)

    def swipe_left(self):
        """
        元素向左滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
            self._device_.swipe(int(self.BOUND[2]), int(self.BOUND[1]) + (self._HIGH / 2), int(self.BOUND[0]),
                                int(self.BOUND[1]) + (self._HIGH / 2))
        else:
            self._device_.swipe(int(self.BOUND[2]), int(self.BOUND[1]) + (self._HIGH / 2), int(self.BOUND[0]),
                                int(self.BOUND[1]) + (self._HIGH / 2))

    def swipe_right(self):
        """
        元素向右滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
            self._device_.swipe(int(self.BOUND[0]), self.BOUND[1] + (self._HIGH / 2), int(self.BOUND[2]),
                                int(self.BOUND[1]) + (self._HIGH / 2))
        else:
            self._device_.swipe(int(self.BOUND[0]), self.BOUND[1] + (self._HIGH / 2), int(self.BOUND[2]),
                                int(self.BOUND[1]) + (self._HIGH / 2))

    def swipe_up(self):
        """
        元素向上滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
            self._device_.swipe(int(self.BOUND[2]) + (self._WIDTH / 2), int(self.BOUND[3]),
                                int(self.BOUND[2]) + (self._WIDTH / 2),
                                int(self.BOUND[1]))
        else:
            self._device_.swipe(int(self.BOUND[2]) + (self._WIDTH / 2), int(self.BOUND[3]),
                                int(self.BOUND[2]) + (self._WIDTH / 2),
                                int(self.BOUND[1]))

    def swipe_down(self):
        """
        元素向下滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
            self._device_.swipe(int(self.BOUND[2]) + (self._WIDTH / 2), int(self.BOUND[1]),
                                int(self.BOUND[2]) + (self._WIDTH / 2),
                                int(self.BOUND[3]))
        else:
            self._device_.swipe(int(self.BOUND[2]) + (self._WIDTH / 2), int(self.BOUND[1]),
                                int(self.BOUND[2]) + (self._WIDTH / 2),
                                int(self.BOUND[3]))
