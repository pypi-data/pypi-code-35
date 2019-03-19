from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Any, TypeVar, Generic
from rover_position_rjg.data.data import TValue, Data

TOutputValue = TypeVar('TOutputValue')


class DataFilter(Generic[TValue, TOutputValue], ABC):
    """Filters received data before passing it on to other receivers"""
    receivers = ...  # type: List[DataFilter[TOutputValue, Any]]

    def __init__(self, name: str = ''):
        self.name = name
        self.receivers = []

    def add(self, receiver: DataFilter[TOutputValue, Any]) -> DataFilter[TOutputValue, Any]:
        """Adds an object that will receive filtered output"""
        self.receivers.append(receiver)
        return receiver

    def remove(self, receiver: DataFilter[TOutputValue, Any]) -> DataFilter[TOutputValue, Any]:
        """Removes an existing receiver
        :type receiver: DataFilter[TValue, TOutputValue]
        """
        if receiver in self.receivers:
            self.receivers.remove(receiver)
        return receiver

    def find(self, name: str) -> DataFilter[TOutputValue, Any]:
        """Performs a depth first search for a filter with
        the given name."""
        if self.name == name:
            return self
        for child in self.receivers:
            found = child.find(name)
            if found:
                return found

    def send(self, value: Data[TOutputValue]) -> None:
        """Sends the value to all the receivers"""
        for receiver in self.receivers:
            receiver.receive(value)

    def close(self):
        """Closes all child receivers and removes them.
        Override this method to clean up resources."""
        for receiver in self.receivers:
            receiver.close()
        self.receivers.clear()

    @abstractmethod
    def receive(self, data: Data[TValue]) -> None:
        """Handles the next piece of data"""
        pass
