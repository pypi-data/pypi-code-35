from abc import ABC, abstractmethod


class DataCleaner(ABC):
    def get_name(self):
        return self.__class__.__name__

    @abstractmethod
    def clean_x_y(self, x, y):
        return x, y

    @abstractmethod
    def clean_x(self, x):
        return x
