# -*- coding: utf-8 -*-

"""Main module."""
from random import choice
from helpers import Helpers
from hard_coded_vins import HARD_CODED_VINS
from vin_character_weights import VIN_CHARACTER_WEIGHTS
from alpha_to_numerical import ALPHA_TO_NUMERICAL_MAP
from cd_val_to_vin_char import CD_VAL_TO_VIN_CHAR_MAP

class LazyVin:
    _vin_list = ()
    _unique_identifier_length = 6

    def __init__(self):
        self._vin_list = HARD_CODED_VINS

    def get_random_dirty_vin(self):
        random_vin = choice(self._vin_list)
        return random_vin

    def get_random_clean_vin(self):
        dirty_vin = self.get_random_dirty_vin()
        # dirty_vin = ''
        clean_vin = dirty_vin[0:(len(dirty_vin) - self._unique_identifier_length)]
        random_unique_id = Helpers.get_random_number_of_length(self._unique_identifier_length)
        clean_vin += Helpers.get_number_as_string(random_unique_id)
        return clean_vin

    def fix_check_digit(self, vin):
        check_digit_modulo_divisor = 11
        check_digit_index = 8 # NOTE: 9th character in the VIN

        # Split string into list of characters
        char_list = list(vin)
        # Set check_digit_index to '0'. # NOTE: We set this to zero to make the summation easier later on.
        char_list[check_digit_index] = '0'
        # Begin transliteration using alpha => number dictionary.
        numerical_values_list = self._get_numerical_values_as_list(char_list)
        # Get weighted products
        weighted_products_list = self._get_weighted_products_list(numerical_values_list)
        # Sum the products list
        sum_of_weighted_values = sum(weighted_products_list)
        # Get the value of sum % 11
        modulo = sum_of_weighted_values % check_digit_modulo_divisor
        # Transliterate modulo using check_digit_value => vin_char map
        check_digit_character = CD_VAL_TO_VIN_CHAR_MAP[modulo]
        char_list[check_digit_index] = check_digit_character

        corrected_vin = ''.join(char_list)

        return corrected_vin

    def _get_numerical_values_as_list(self, character_list):
        numerical_list = []

        for char in character_list:
            if (Helpers.char_is_number(char)):
                numerical_list.append(int(char))
            else:
                # Replace alpha characters using transliteration map.
                replaced_value = ALPHA_TO_NUMERICAL_MAP[char.lower()] # The map expects lowercase.
                numerical_list.append(replaced_value)

        return numerical_list

    def _get_weighted_products_list(self, values_list):
        weighted_list = []

        for index in range(0, len(values_list)):
            character_value = values_list[index]
            weighted_multiplier = VIN_CHARACTER_WEIGHTS[index + 1]
            weighted_list.append(character_value * weighted_multiplier)

        return weighted_list
