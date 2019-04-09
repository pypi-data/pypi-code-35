# package com.games.thraxis.framework.rules;
#
# /##
#  # Created by Zack on 10/2/2017.
#  #/
#
# public abstract class TGOtherwiseRule<C> extends TGBaseRule<C> {
#
# 	@Override
# 	public boolean isApplicable(C context) {
# 		return true;
# 	}
#
#
# 	@Override
# 	public abstract String toString();
# }
#
from abc import abstractmethod

from rules.abstract_rule import TGAbstractRule


class TGAbstractOtherwiseRule(TGAbstractRule):

    @abstractmethod
    def apply_to(self, context):
        pass

    @abstractmethod
    def is_applicable(self, context=None):
        return True
