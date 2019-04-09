# package com.games.thraxis.framework.listeners;
#
# import com.games.thraxis.framework.eventhandling.TGEvent;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public interface TGListener<S> {
#
# 	String getEventId();
# 	void onEvent(TGEvent<String, S> event);
#
# }

from abc import ABC, abstractmethod


class TGAbstractListener(ABC):
    def __init__(self, event_id):
        self.event_id = event_id

    def get_event_id(self):
        return self.event_id

    @abstractmethod
    def on_event(self, event=None):
        pass
