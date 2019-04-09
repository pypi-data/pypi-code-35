# package com.games.thraxis.framework.eventhandling;
#
# /##
#  # Created by Zack on 10/10/2017.
#  #/
#
# public class TGDummyReaction<S> implements TGReaction<S> {
#
# 	public static <T> T create(Class<?> type) {
# 		return create(type.getSimpleName());
# 	}
#
# 	public static <T> T create(String eventId) {
# 		return (T) new TGDummyReaction<>();
# 	}
#
# 	@Override
# 	public void reactTo(S subject) {
# 		//Do nothing
# 	}
# }
from eventhandling.abstract_reaction import TGAbstractReaction


class TGDummyReaction(TGAbstractReaction):
    def react_to(self, subject):
        return  # Do nothing.
