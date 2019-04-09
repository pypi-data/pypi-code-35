# package com.games.thraxis.framework.eventhandling;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public interface TGPublisher<I, S> {
#
# 	void discardUnheardEvents();
#
# 	void publish(TGEvent<I, S> event);
#
# 	<T extends S> void publish(I event, T subject);
#
# 	<V> void publishChange(I eventId, V oldValue, V newValue);
# }
from abc import ABC, abstractmethod


class TGAbstractPublisher(ABC):
    @abstractmethod
    def discard_unheard_events(self):
        pass

    @abstractmethod
    def publish(self, event, subject=None):
        pass

    @abstractmethod
    def publish_change(self, event_id, old_value, new_value):
        pass
