from abc import ABC, abstractmethod


class DataCleaner(ABC):
    def get_name(self):
        return self.__class__.__name__

    @abstractmethod
    def clean_training_data(self, x, y):
        return x, y

    @abstractmethod
    def clean_testing_data(self, x):
        return x
