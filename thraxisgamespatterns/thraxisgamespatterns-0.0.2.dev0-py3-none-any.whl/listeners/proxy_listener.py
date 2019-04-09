# package com.games.thraxis.framework.listeners;
#
# import com.games.thraxis.framework.assertions.TGBaseWatchDog;
# import com.games.thraxis.framework.eventhandling.TGEvent;
#
# /##
#  # Created by Zack on 10/11/2017.
#  #/
#
# public class TGListenerProxy<S, T extends TGListener<S>> implements TGListener<S> {
#
# 	private T listener;
#
# 	public TGListenerProxy(T listener) {
# 		this.listener = listener;
# 	}
#
# 	public TGListenerProxy(String eventId) {
# 		this(TGDummyListener.<T>create(eventId));
# 	}
#
# 	@Override
# 	public String getEventId() {
# 		return listener.getEventId();
# 	}
#
# 	@Override
# 	public void onEvent(final TGEvent<String, S> event) {
# 		listener.onEvent(event);
# 	}
#
# 	public void setListener(T listener) {
# 		boolean sameId = this.listener.getEventId().equals(listener.getEventId());
# 		TGBaseWatchDog.DEFAULT.assertTrue(sameId, "Event ID does not match!");
# 		this.listener = listener;
# 	}
# }
from listeners.abstract_listener import TGAbstractListener
from listeners.dummy_listener import TGDummyListener


class TGListenerProxy(TGAbstractListener):
    def __init__(self, listener=None, event_id=None):
        self.listener = TGDummyListener(event_id) if (event_id and not listener) else listener

    def get_event_id(self):
        return self.listener.get_event_id()

    def on_event(self, event):
        self.listener.on_event(event)

    def set_listener(self, listener):
        if not listener.get_event_id() == self.listener.get_event_id():
            self.listener = listener
