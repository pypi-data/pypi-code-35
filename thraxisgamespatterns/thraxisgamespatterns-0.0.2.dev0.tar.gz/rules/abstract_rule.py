# package com.games.thraxis.framework.rules;
#
# /##
#  # Provides common behaviors for stateless condition and action pairs that can apply themselves when appropriate
#  #
#  # Concrete implementations should be stateless and safe to use on multiple threads
#  #/
#
# public abstract class TGBaseRule<C> implements TGRule<C> {
#
# 	@Override
# 	public void considerApplying(C context) {
# 		if (isApplicable(context)) {
# 			applyTo(context);
# 		}
# 	}
# }

from abc import abstractmethod

from rules.abstract_applicable import TGAbstractApplicable


class TGAbstractRule(TGAbstractApplicable):
    @abstractmethod
    def is_applicable(self, context=None):
        pass

    @abstractmethod
    def apply_to(self, context):
        pass

    def consider_applying(self, context):
        if self.is_applicable(context):
            self.apply_to(context)
