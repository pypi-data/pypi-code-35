# package com.games.thraxis.framework.listeners;
#
# /##
#  # Created by Zack on 10/10/2017.
#  #/
#
# public interface TGListenerContainer {
#
# 	void registerListeners();
#
# 	void unregisterListeners();
# }

from abc import ABC, abstractmethod


class TGAbstractListenerContainer(ABC):
    @abstractmethod
    def register_listeners(self):
        pass

    def __init__(self, listener_registry):
        self.listener_registry = listener_registry
        self.listeners = []

    def register_interest(self, listener_list):
        if type(listener_list) is not list:
            listener_list = [listener_list]
        for listener in listener_list:
            self.listeners.append(listener)
            self.listener_registry.register_interest(listener)

    def register_listener(self, listener):
        self.register_interest(listener)

    def unregister_listeners(self):
        self.listener_registry.unregister_interest(self.listeners)
        self.listeners = []
