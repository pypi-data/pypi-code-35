# package com.games.thraxis.framework.rules;
#
# /##
#  # API for objects that may apply in a given situation
#  #/
#
# public interface TGApplicability<C> {
#
# 	boolean isApplicable(C context);
# }


from abc import ABC, abstractmethod


class TGAbstractApplicable(ABC):

    @abstractmethod
    def is_applicable(self, context=None):
        pass

    @abstractmethod
    def apply_to(self, context):
        pass
