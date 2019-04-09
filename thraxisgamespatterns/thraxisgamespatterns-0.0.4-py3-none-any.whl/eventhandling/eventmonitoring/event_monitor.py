# package com.games.thraxis.framework.eventhandling.eventmonitoring;
#
# import java.util.Collection;
# import java.util.HashSet;
#
# import com.games.thraxis.framework.application.TGRegistry;
# import com.games.thraxis.framework.eventhandling.TGEventTracker;
# import com.games.thraxis.framework.listeners.TGListener;
# import com.games.thraxis.framework.listeners.TGListenerRegistry;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public class TGBasicEventMonitor extends TGBaseEventMonitor {
#
# 	private final TGEventTracker<String> eventTracker;
# 	private final TGListenerRegistry<Object> listenerRegistry;
# 	private final Collection<TGListener<?>> listeners = new HashSet<>();
#
# 	public TGBasicEventMonitor(TGRegistry registry) {
# 		this.eventTracker = registry.getEventTracker();
# 		this.listenerRegistry = registry.getListenerRegistry();
# 	}
#
# 	@Override
# 	public boolean areEventsPending() {
# 		return areEventsPending(listeners);
# 	}
#
# 	@Override
# 	public void checkPendingEvent(String eventId) {
# 		//Do nothing, decorators may override
# 	}
#
# 	@Override
# 	public void checkPendingEvents() {
# 		//Do nothing, decorators may override
# 	}
#
# 	@Override
# 	public boolean isListeningTo(String eventId) {
# 		return isListeningTo(listeners, eventId);
# 	}
#
# 	@Override
# 	public boolean isPending(String eventId) {
# 		return eventTracker.isPending(eventId);
# 	}
#
# 	@Override
# 	public void registerListener(TGListener<?> listener) {
# 		listeners.add(listener);
# 		listenerRegistry.registerInterest(listener);
# 	}
#
# 	@Override
# 	public void unregisterListeners() {
# 		listenerRegistry.deregisterInterest(listeners);
# 		listeners.clear();
# 	}
#
# 	@Override
# 	public void unregisterListeners(Collection<TGListener<?>> listeners) {
# 		listenerRegistry.deregisterInterest(listeners);
# 		listeners.removeAll(listeners);
# 	}
# }
from eventhandling.eventmonitoring.abstract_base_event_monitor import TGAbstractBaseEventMonitor


class TGBasicEventMonitor(TGAbstractBaseEventMonitor):
    def __init__(self, registry):
        self.event_tracker = registry.get_event_tracker()
        self.listener_registry = registry.get_listener_registry()
        self.listeners = []

    def are_events_pending(self, listeners=None):
        return super().are_events_pending(self.listeners)

    def check_pending_event(self, event_id):
        return  # Do nothing - decorators will override as needed.

    def check_pending_events(self):
        return  # Do nothing - decorators will override as needed.

    def is_listening_to(self, event_id, listeners=None):
        return super().is_listening_to(self.listeners, event_id)

    def is_pending(self, event_id):
        return self.event_tracker.is_pending(event_id)

    def register_listener(self, listener):
        self.listeners.append(listener)
        self.listener_registry.register_interest(listener)

    def unregister_listeners(self, listeners=None):
        self.listener_registry.unregister_interest(listeners)
        listeners.clear()
