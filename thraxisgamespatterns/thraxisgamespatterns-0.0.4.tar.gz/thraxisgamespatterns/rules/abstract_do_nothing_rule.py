# package com.games.thraxis.framework.rules;
#
# /##
#  # Created by Zack on 10/2/2017.
#  #/
#
# public abstract class TGDoNothingRule<C> extends TGBaseRule<C> {
#
# 	@Override
# 	public void applyTo(C context) {
# 		//DO NOTHING
# 	}
#
# 	@Override
# 	public abstract String toString();
# }

from abc import abstractmethod

from rules.abstract_rule import TGAbstractRule


class TGAbstractDoNothingRule(TGAbstractRule):
    @abstractmethod
    def is_applicable(self, context=None):
        pass

    def apply_to(self, context):
        pass  # Do nothing
