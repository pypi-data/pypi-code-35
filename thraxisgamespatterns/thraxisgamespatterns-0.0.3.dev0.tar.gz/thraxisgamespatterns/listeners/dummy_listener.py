# package com.games.thraxis.framework.listeners;
#
# import com.games.thraxis.framework.eventhandling.TGEvent;
#
# /##
#  # Created by Zack on 10/10/2017.
#  #/
#
# public class TGDummyListener<S> implements TGListener<S> {
#
# 	public static <T> T create(Class<?> type) {
# 		return create(type.getSimpleName());
# 	}
#
# 	public static <T> T create(String eventId) {
# 		return (T) new TGDummyListener<>(eventId);
# 	}
#
# 	private final String eventId;
#
# 	public TGDummyListener(String eventId) {
# 		this.eventId = eventId;
# 	}
#
# 	@Override
# 	public String getEventId() {
# 		return eventId;
# 	}
#
# 	@Override
# 	public void onEvent(TGEvent<String, S> event) {
# 		//Ignore the event
# 	}
# }
from listeners.abstract_listener import TGAbstractListener


class TGDummyListener(TGAbstractListener):

    def on_event(self, event):
        pass  # Ignore the event.
