# package com.games.thraxis.framework.eventhandling;
#
# import java.util.ArrayList;
# import java.util.Collection;
# import java.util.Collections;
# import java.util.HashMap;
# import java.util.LinkedHashMap;
# import java.util.List;
# import java.util.Map;
#
# import android.os.Handler;
# import android.os.Looper;
#
# import com.games.thraxis.framework.assertions.TGWatchDog;
# import com.games.thraxis.framework.listeners.TGListener;
# import com.games.thraxis.framework.listeners.TGListenerRegistry;
# import com.games.thraxis.framework.logging.TGLogger;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public class TGEventDistributor<S> implements TGPublisher<String, S>, TGListenerRegistry<S> {
#
# 	private static final int MAX_UNHEARD_EVENTS = 10;
# 	private final String UNPUBLISHED = "UNPUBLISHED";
# 	private final Map<String, List<TGListener<? extends S>>> listenerMap = createListenerMap();
# 	private final TGLogger logger;
# 	private final Looper mainLooper = Looper.getMainLooper();
# 	private final LinkedHashMap<String, TGEvent<String, S>> unheardEvents = createUnheardEventsMap();
# 	private final TGWatchDog watchdog;
#
# 	public TGEventDistributor(TGWatchDog watchdog, TGLogger logger) {
# 		this.watchdog = watchdog;
# 		this.logger = logger;
# 	}
#
# 	protected void checkUnheardEvents(TGListener<? extends S> listener) {
# 		TGEvent<String, S> event = unheardEvents.remove(listener.getEventId());
# 		if (event != null) {
# 			logDebug("unheardEventWillBeHeard: %s", listener.getEventId());
# 			distribute(event, listener);
# 		}
# 	}
#
# 	protected void considerRemoving(String eventId, List<TGListener<? extends S>> listeners) {
# 		if (listeners.isEmpty()) {
# 			listenerMap.remove(eventId);
# 		}
#
# 	}
#
# 	protected <V> TGEvent<String, S> createChangeEvent(String eventId, V oldValue, V newValue) {
# 		TGValueChange<V> change = new TGBaseValueChange<>(eventId, oldValue, newValue);
# 		return (TGEvent<String, S>) new TGBaseEvent<>(change.getEventId(), change);
# 	}
#
# 	@Override
# 	public <T extends S> void deregisterInterest(TGListener<T> listener) {
# 		watchdog.assertUiThread();
# 		if (listenerMap.containsKey((listener.getEventId()))) {
# 			List<TGListener<? extends S>> listeners = listenerMap.get(listener.getEventId());
# 			listeners.remove(listener);
# 			considerRemoving(listener.getEventId(), listeners);
# 		}
# 	}
#
# 	@Override
# 	public void deregisterInterest(Collection<TGListener<? extends S>> listeners) {
# 		watchdog.assertUiThread();
# 		for (TGListener<? extends S> listener : listeners) {
# 			deregisterInterest(listener);
# 		}
# 	}
#
# 	@Override
# 	public void discardUnheardEvents() {
# 		watchdog.assertUiThread();
# 		unheardEvents.clear();
# 	}
#
# 	protected void distribute(TGEvent<String, S> event, TGListener<? extends S> listener) {
# 		((TGListener<S>) listener).onEvent(event);
# 	}
#
# 	protected void distributeEvent(TGEvent<String, S> event) {
# 		List<TGListener<? extends S>> listeners = listenerMap.get(event.getId());
# 		if (listeners != null) {
# 			distributeEvent(event, listeners);
# 		} else {
# 			handleNoListeners(event);
# 		}
# 	}
#
# 	protected void distributeEvent(TGEvent<String, S> event, List<TGListener<? extends S>> listeners) {
# 		List<TGListener<? extends S>> originalListeners = new ArrayList<>(listeners);
# 		for (TGListener<? extends S> listener : originalListeners) {
# 			logDebug("distributeEvent: %s", listener.getEventId());
# 			distribute(event, listener);
# 		}
# 	}
#
# 	protected void handleNoListeners(TGEvent<String, S> event) {
# 		logDebug("handleNoListeners: %s", event.getId());
# 		makeRoomForUnheardEvent();
# 		unheardEvents.put(event.getId(), event);
# 	}
#
# 	protected int logDebug(String format, Object... arguments) {
# 		return logger.debug(getClass(), format, arguments);
# 	}
#
# 	protected void makeRoomForUnheardEvent() {
# 		if (unheardEvents.size() >= MAX_UNHEARD_EVENTS) {
# 			Object discarded = unheardEvents.remove(unheardEvents.keySet().iterator().next());
# 			logDebug("discarding: %s", discarded);
# 		}
# 	}
#
# 	@Override
# 	public void publish(TGEvent<String, S> event) {
# 		watchdog.assertUiThread();
# 		logDebug("publish: %s", event.getId());
# 		distributeEvent(event);
# 	}
#
# 	@Override
# 	public <T extends S> void publish(String eventId, T subject) {
# 		watchdog.assertUiThread();
# 		publish(new TGBaseEvent<String, S>(eventId, subject));
# 	}
#
# 	@Override
# 	public <V> void publishChange(String eventId, V oldValue, V newValue) {
# 		watchdog.assertUiThread();
# 		watchdog.assertNotNull(eventId);
# 		watchdog.assertNotNull(oldValue);
# 		watchdog.assertNotNull(newValue);
# 		if (!oldValue.equals(newValue)) {
# 			logDebug("publishChange: %s from=%s to=%s", eventId, oldValue, newValue);
# 			distributeEvent(createChangeEvent(eventId, oldValue, newValue));
# 		}
# 	}
#
# 	@Override
# 	public <T extends S> void registerInterest(TGListener<T> listener) {
# 		watchdog.assertUiThread();
# 		watchdog.assertNotNull(listener.getEventId());
# 		if (!listenerMap.containsKey(listener.getEventId())) {
# 			List<TGListener<? extends S>> listeners = new ArrayList<>();
# 			listenerMap.put(listener.getEventId(), listeners);
# 		}
# 		List<TGListener<? extends S>> list = listenerMap.get(listener.getEventId());
# 		watchdog.assertFalse(list.contains(listener), "Attempt to re-register listener");
# 		list.add(listener);
# 		checkUnheardEvents(listener);
# 	}
#
# 	@Override
# 	public <T extends S> void registerTemporaryInterest(final TGListener<T> listener, long durationMilliseconds) {
# 		registerInterest(listener);
# 		new Handler(mainLooper).postDelayed(new Runnable() {
# 			@Override
# 			public void run() {
# 				deregisterInterest(listener);
# 			}
# 		}, durationMilliseconds);
# 	}
# }

from collections import OrderedDict

from eventhandling.abstract_publisher import TGAbstractPublisher
from eventhandling.event import TGEvent
from eventhandling.value_change import TGValueChange
from listeners.abstract_listener_registry import TGAbstractListenerRegistry

MAX_UNHEARD_EVENTS = 10
UNPUBLISHED = "UNPUBLISHED"


class TGEventDistributor(TGAbstractPublisher, TGAbstractListenerRegistry):
    def __init__(self, logger):
        self.logger = logger
        self.listener_map = {UNPUBLISHED: []}
        self.unheard_events = OrderedDict()

    def check_unheard_events(self, listener):
        event = self.unheard_events.pop(listener.get_event_id())
        if event:
            self.distribute(event, listener)

    def consider_removing(self, event_id, listeners):
        if not listeners:
            self.listener_map.pop(event_id, None)

    def create_change_event(self, event_id, old_value, new_value):
        change = TGValueChange(event_id, old_value, new_value)
        return TGEvent(change.event_id, change)

    def unregister_interest(self, listeners):
        if type(listeners) is not list:
            listeners = [listeners]
        for listener in listeners:
            if listener.get_event_id() in self.listener_map:
                listeners = self.listener_map.get(listener.get_event_id())
                listeners.remove(listener)
                self.consider_removing(listener.get_event_id(), listeners)

    def discard_unheard_events(self):
        self.unheard_events.clear()

    def distribute(self, event, listener):
        listener.on_event(event)

    def distribute_event(self, event, listeners=None):
        if not listeners or type(listeners) is not list:
            listeners = self.listener_map.get(event.get_id())
        if listeners:
            original_listeners = listeners
            for listener in original_listeners:
                self.distribute(event, listener)
        else:
            self.handle_no_listeners(event)

    def handle_no_listeners(self, event):
        self.make_room_for_unheard_event()
        self.unheard_events.update({event.get_id(): event})

    def make_room_for_unheard_event(self):
        if len(self.unheard_events) >= MAX_UNHEARD_EVENTS:
            self.unheard_events.popitem()

    def publish(self, event, subject=None):
        self.distribute_event(event)

    def publish_change(self, event_id, old_value, new_value):
        if event_id and old_value and new_value and not (old_value == new_value):
            self.distribute_event(self.create_change_event(event_id, old_value, new_value))

    def register_interest(self, listener):
        if listener.get_event_id() and not self.listener_map.__contains__(listener.get_event_id()):
            self.listener_map.update({listener.get_event_id(): []})
        listener_list = self.listener_map.get(listener.get_event_id())
        listener_list.append(listener)
        self.check_unheard_events(listener)
