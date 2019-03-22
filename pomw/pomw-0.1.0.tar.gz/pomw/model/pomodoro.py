# -*- python-indent-offset: 4; -*-

from datetime import datetime

from .interval import Interval


class Pomodoro(Interval):
    def __init__(
        self,
        start_time=None,
        end_time=None,
        internal_interrupt=0,
        external_interrupt=0,
        void=False,
    ):
        super().__init__(start_time=start_time, end_time=end_time)
        self.internal_interrupt = internal_interrupt
        self.external_interrupt = external_interrupt
        self.void = void

    @staticmethod
    def __json_decode__(d):
        return Pomodoro(
            start_time=d.get("_Interval__start_time", None),
            end_time=d.get("_Interval__end_time", None),
            internal_interrupt=d.get("_Pomodoro__internal_interrupt", 0),
            external_interrupt=d.get("_Pomodoro__external_interrupt", 0),
            void=d.get("_Pomodoro__void", False),
        )

    @property
    def external_interrupt(self):
        return self.__external_interrupt

    @external_interrupt.setter
    def external_interrupt(self, external_interrupt):
        if isinstance(external_interrupt, int):
            self.__external_interrupt = external_interrupt
        else:
            raise TypeError(
                "'external_interrupt' should be of type %s" % (int.__name__)
            )

    @property
    def internal_interrupt(self):
        return self.__internal_interrupt

    @internal_interrupt.setter
    def internal_interrupt(self, internal_interrupt):
        if isinstance(internal_interrupt, int):
            self.__internal_interrupt = internal_interrupt
        else:
            raise TypeError(
                "'internal_interrupt' should be of type %s" % (int.__name__)
            )

    @property
    def void(self):
        return self.__void

    @void.setter
    def void(self, void):
        self.__void = void
