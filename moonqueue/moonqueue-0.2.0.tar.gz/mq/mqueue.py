"""
:author: Gatsby Lee
:since: 2019-04-04
"""
import abc

class MQueue(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def push(self, serialized_msg_list: list):
        pass

    @abc.abstractmethod
    def pop(self):
        pass
