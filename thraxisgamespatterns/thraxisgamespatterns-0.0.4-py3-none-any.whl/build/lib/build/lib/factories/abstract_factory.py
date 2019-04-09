# package com.games.thraxis.framework.factories;
#
# /##
#  # Created by Zack on 10/2/2017.
#  #/
#
# public interface TGFactory<P> {
#
# 	P create();
# }

from abc import ABC, abstractmethod


class TGAbstractFactory(ABC):
    @abstractmethod
    def create(self, options=None):
        pass
