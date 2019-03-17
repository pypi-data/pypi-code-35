from abc import ABCMeta, abstractmethod, abstractproperty


class BaseModel(object):

    __metaclass__ = ABCMeta

    @abstractproperty
    def model(self):
        """ Return Model

        :return: obj model
        """

    @abstractmethod
    def reset(self):
        """ Reset model with base structure

        :return: None
        """

    @abstractmethod
    def load(self, values):
        """ Load model with passed values

        :param values: dict k/v to load into model
        :return: obj model
        """
