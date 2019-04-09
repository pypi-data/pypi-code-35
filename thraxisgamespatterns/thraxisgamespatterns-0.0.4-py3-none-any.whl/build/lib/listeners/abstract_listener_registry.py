# package com.games.thraxis.framework.listeners;
#
# import java.util.Collection;
#
# /##
#  # Created by Zack on 9/26/2017.
#  #/
#
# public interface TGListenerRegistry<S> {
#
# 	<T extends S> void deregisterInterest(TGListener<T> listener);
#
# 	void deregisterInterest(Collection<TGListener<? extends S>> listeners);
#
# 	<T extends S> void registerInterest(TGListener<T> listener);
#
# 	<T extends S> void registerTemporaryInterest(TGListener<T> listener, long durationMilliseconds);
# }
from abc import ABC, abstractmethod


class TGAbstractListenerRegistry(ABC):
    @abstractmethod
    def unregister_interest(self, listeners):
        pass

    @abstractmethod
    def register_interest(self, listener):
        pass
