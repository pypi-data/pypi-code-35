# package com.games.thraxis.framework.listeners;
#
# import com.games.thraxis.framework.eventhandling.TGEvent;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public abstract class TGEventSubjectUnusedListener extends TGBaseListener<String> {
#
# 	public TGEventSubjectUnusedListener(String eventId) {
# 		super(eventId);
# 	}
#
# 	@Override
# 	public void onEvent(TGEvent<String, String> event) {
# 		onEvent();
# 	}
#
# 	protected abstract void onEvent();
# }
from abc import abstractmethod

from listeners.abstract_listener import TGAbstractListener


class TGAbstractEventSubjectUnusedListener(TGAbstractListener):
    @abstractmethod
    def on_event(self, event=None):
        pass
