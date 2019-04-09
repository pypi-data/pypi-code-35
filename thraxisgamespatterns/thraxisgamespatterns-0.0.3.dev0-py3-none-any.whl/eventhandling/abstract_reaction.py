# package com.games.thraxis.framework.eventhandling;
#
# /##
#  # Created by Zack on 9/25/2017.
#  #/
#
# public interface TGReaction<S> {
#
# 	void reactTo(S subject);
# }
from abc import ABC, abstractmethod


class TGAbstractReaction(ABC):
    @abstractmethod
    def react_to(self, subject):
        pass
