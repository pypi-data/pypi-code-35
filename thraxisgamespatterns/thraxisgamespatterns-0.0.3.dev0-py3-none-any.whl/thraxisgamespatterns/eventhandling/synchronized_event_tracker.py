# package com.games.thraxis.framework.eventhandling;
#
# import java.util.HashSet;
# import java.util.Set;
#
# /##
#  # Created by Zack on 9/25/2017.
#  #/
#
# public class TGSynchronizedEventTracker<E> implements TGEventTracker<E> {
#
# 	private final Set<E> pendingEvents = new HashSet<>();
#
# 	@Override
# 	public synchronized void forgetPendingEvent(E eventId) {
# 		pendingEvents.remove(eventId);
# 	}
#
# 	@Override
# 	public synchronized boolean isPending(E eventId) {
# 		return pendingEvents.contains(eventId);
# 	}
#
# 	@Override
# 	public synchronized void trackPendingEvent(E eventId) {
# 		pendingEvents.add(eventId);
# 	}
#
# }
from eventhandling.abstract_event_tracker import TGAbstractEventTracker


class TGSynchronizedEventTracker(TGAbstractEventTracker):
    def __init__(self):
        self.events = []

    def forget_pending(self, event_id):
        self.events.remove(event_id)

    def is_pending(self, event_id):
        return self.events.__contains__(event_id)

    def track_pending_event(self, event_id):
        self.events.append(event_id)
