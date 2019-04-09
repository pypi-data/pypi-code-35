# package com.games.thraxis.framework.enumeration.matcher;
#
# import java.util.Collection;
# import java.util.Collections;
#
# import android.support.annotation.NonNull;
#
# /##
#  # Created by Zack on 9/21/2017.
#  #/
#
# public abstract class TGValueMatcher<E, V> implements TGMatcher<E> {
#
# 	private final Collection<V> valuesBeingMatched;
#
# 	public TGValueMatcher(@NonNull Collection<V> valuesBeingMatched) {
# 		this.valuesBeingMatched = valuesBeingMatched;
# 	}
#
# 	public TGValueMatcher(@NonNull V valueBeingMatched){
# 		this.valuesBeingMatched = Collections.singleton(valueBeingMatched);
# 	}
#
# 	protected abstract V getValueToMatchFrom(E element);
#
# 	@Override
# 	public boolean isMatch(E element) {
# 		return element != null && valuesBeingMatched.contains(getValueToMatchFrom(element));
# 	}
# }
from abc import abstractmethod

from enumeration.matcher.abstract_matcher import TGAbstractMatcher


class TGAbstractValueMatcher(TGAbstractMatcher):
    def __init__(self, values_being_matched):
        if type(values_being_matched) is not list:
            values_being_matched = [values_being_matched]
        self.values_being_matched = values_being_matched

    def is_match(self, element):
        return element is not None and self.values_being_matched.contains(self.get_value_to_match_from(element))

    @abstractmethod
    def get_value_to_match_from(self, element):
        pass
