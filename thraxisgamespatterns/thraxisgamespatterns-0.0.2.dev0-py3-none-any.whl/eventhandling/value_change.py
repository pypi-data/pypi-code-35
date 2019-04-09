# package com.games.thraxis.framework.eventhandling;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public class TGBaseValueChange<V> implements TGValueChange<V> {
#
# 	private final String eventId;
# 	private final V newValue;
# 	private final V oldValue;
#
# 	public TGBaseValueChange(String eventId, V newValue, V oldValue) {
# 		this.eventId = eventId;
# 		this.newValue = newValue;
# 		this.oldValue = oldValue;
# 	}
#
# 	@Override
# 	public String getEventId() {
# 		return eventId;
# 	}
#
# 	@Override
# 	public V getNewValue() {
# 		return newValue;
# 	}
#
# 	@Override
# 	public V getOldValue() {
# 		return oldValue;
# 	}
# }


class TGValueChange:
    def __init__(self, event_id, new_value, old_value):
        self.event_id = event_id
        self.new_value = new_value
        self.old_value = old_value
