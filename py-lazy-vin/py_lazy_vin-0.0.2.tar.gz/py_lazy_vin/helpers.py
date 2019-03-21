from random import randint

class Helpers():

    @staticmethod
    def get_random_number_of_length(length):
        range_start = 10**(length - 1)
        range_end = (10**length) - 1
        return randint(range_start, range_end)

    @staticmethod
    def get_number_as_string(number):
        return str(number)

    @staticmethod
    def char_is_number(char):
        return char.isdigit()
