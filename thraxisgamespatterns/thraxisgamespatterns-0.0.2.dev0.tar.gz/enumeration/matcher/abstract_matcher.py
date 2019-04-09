# package com.games.thraxis.framework.enumeration.matcher;
#
# /##
#  # Created by Zack on 9/21/2017.
#  #/
#
# public interface TGMatcher<E> {
# 	boolean isMatch(E element);
#
# }
from abc import ABC, abstractmethod


class TGAbstractMatcher(ABC):
    @abstractmethod
    def is_match(self, element):
        pass
