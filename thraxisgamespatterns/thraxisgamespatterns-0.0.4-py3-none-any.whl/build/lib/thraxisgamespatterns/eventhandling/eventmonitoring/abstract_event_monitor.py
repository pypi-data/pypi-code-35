# package com.games.thraxis.framework.eventhandling.eventmonitoring;
#
# import java.util.Collection;
#
# import com.games.thraxis.framework.listeners.TGListener;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public interface TGEventMonitor {
#
# 	boolean areEventsPending();
#
# 	void checkPendingEvent(String eventId);
#
# 	void checkPendingEvents();
#
# 	boolean isListeningTo(String eventId);
#
# 	boolean isPending(String eventId);
#
# 	boolean isWaitingFor(String eventId);
#
# 	void registerListener(TGListener<?> listener);
#
# 	void unregisterListeners();
#
# 	void unregisterListeners(Collection<TGListener<?>> listeners);
#
# }
from abc import ABC, abstractmethod


class TGAbstractEventMonitor(ABC):
    @abstractmethod
    def are_events_pending(self, listeners=None):
        pass

    @abstractmethod
    def check_pending_event(self, event_id):
        pass

    @abstractmethod
    def check_pending_events(self):
        pass

    @abstractmethod
    def is_listening_to(self, event_id, listeners=None):
        pass

    @abstractmethod
    def is_pending(self, event_id):
        pass

    @abstractmethod
    def is_waiting_for(self, event_id):
        pass

    @abstractmethod
    def register_listener(self, listener):
        pass

    @abstractmethod
    def unregister_listeners(self, listeners=None):
        pass
