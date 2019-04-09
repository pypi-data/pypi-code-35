# package com.games.thraxis.framework.listeners;
#
# import com.games.thraxis.framework.eventhandling.TGEvent;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public abstract class TGEventSubjectListener<S> extends TGBaseListener<S> {
#
# 	public TGEventSubjectListener(String eventId) {
# 		super(eventId);
# 	}
#
# 	@Override
# 	public void onEvent(TGEvent<String, S> event) {
# 		onEventHandle(event.getSubject());
# 	}
#
# 	protected abstract void onEventHandle(S subject);
# }

from abc import abstractmethod

from listeners.abstract_listener import TGAbstractListener


class TGAbstractEventSubjectListener(TGAbstractListener):
    def on_event(self, event=None):
        self.on_event_handle(event.get_subject())

    @abstractmethod
    def on_event_handle(self, subject):
        pass
