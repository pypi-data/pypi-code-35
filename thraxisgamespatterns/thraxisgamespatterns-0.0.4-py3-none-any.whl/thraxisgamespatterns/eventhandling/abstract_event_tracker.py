# package com.games.thraxis.framework.eventhandling;
#
# /##
#  # Created by Zack on 9/25/2017.
#  #/
#
# public interface TGEventTracker<E> {
#
# 	void forgetPendingEvent(E eventId);
# 	boolean isPending(E eventId);
# 	void trackPendingEvent(E eventId);
#
# }
from abc import ABC, abstractmethod


class TGAbstractEventTracker(ABC):
    @abstractmethod
    def forget_pending(self, event_id):
        pass

    @abstractmethod
    def is_pending(self, event_id):
        pass

    @abstractmethod
    def track_pending_event(self, event_id):
        pass
