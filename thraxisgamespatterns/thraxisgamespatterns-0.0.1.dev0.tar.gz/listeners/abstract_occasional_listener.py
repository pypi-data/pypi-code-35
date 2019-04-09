# package com.games.thraxis.framework.listeners;
#
# import com.games.thraxis.framework.eventhandling.TGEvent;
#
# /##
#  # Created by Zack on 10/11/2017.
#  #/
#
# public abstract class TGOccasionalListener<S> implements TGListener<S> {
#
# 	protected abstract boolean isInterested(TGEvent<String, S> event);
#
# 	@Override
# 	public void onEvent(TGEvent<String, S> event) {
# 		if (isInterested(event)) {
# 			onInterestedEvent(event);
# 		}
# 	}
#
# 	protected abstract void onInterestedEvent(TGEvent<String, S> event);
# }
from abc import abstractmethod

from listeners.abstract_listener import TGAbstractListener


class TGAbstractOccasionalListener(TGAbstractListener):
    @abstractmethod
    def is_interested(self, event):
        pass

    @abstractmethod
    def on_interested_event(self, event):
        pass

    def on_event(self, event):
        if self.is_interested(event):
            self.on_interested_event(event)
