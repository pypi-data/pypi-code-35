# package com.games.thraxis.framework.eventhandling;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public interface TGEvent<I, S> {
# I getId();
# 	S getSubject();
# 	long getTimestamp();
# }
# package com.games.thraxis.framework.eventhandling;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public class TGBaseEvent<I, S> implements TGEvent<I, S> {
#
# 	private final I id;
# 	private final S subject;
# 	private final long timestamp = System.currentTimeMillis();
#
# 	public TGBaseEvent(I id, S subject) {
# 		this.id = id;
# 		this.subject = subject;
# 	}
#
# 	@Override
# 	public I getId() {
# 		return id;
# 	}
#
# 	@Override
# 	public S getSubject() {
# 		return subject;
# 	}
#
# 	@Override
# 	public long getTimestamp() {
# 		return timestamp;
# 	}
# }

import datetime


class TGEvent:
    def __init__(self, event_id, subject):
        self.event_id = event_id
        self.subject = subject
        self.timestamp = datetime.datetime
