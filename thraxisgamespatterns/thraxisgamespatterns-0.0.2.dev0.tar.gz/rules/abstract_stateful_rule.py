# package com.games.thraxis.framework.rules;
#
# /##
#  # Provides common behaviors for stateless condition and action pairs that can apply themselves when appropriate
#  #
#  # Concrete implementations should be stateless and safe to use on multiple threads
#  #/
#
# public abstract class TGBaseStatefulRule implements TGStatefulRule {
#
# 	@Override
# 	public void considerApplying() {
# 		if (isApplicable()) {
# 			apply();
# 		}
# 	}
#
# 	@Override
# 	public final void applyTo(Void context) {
# 		apply();
# 	}
#
# 	@Override
# 	public boolean isApplicable(Void context) {
# 		return isApplicable();
# 	}
# }
from abc import abstractmethod

from rules.abstract_applicable import TGAbstractApplicable


class TGAbstractStatefulRule(TGAbstractApplicable):

    def consider_applying(self):
        if self.is_applicable():
            self.apply()

    def apply_to(self, context=None):
        self.apply()

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def is_applicable(self, context=None):
        pass
