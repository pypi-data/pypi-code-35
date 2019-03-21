#!/usr/bin/env python3
import json
from numpy import vectorize
with open('letter_price_info.json') as f:
    letter_price_info_input = json.load(f)

with open('parcel_price_info.json') as f:
    parcel_price_info_input = json.load(f)

with open('zone_country_info.json') as f:
    zone_country_info_input = json.load(f)

class Stamp:
    zone_country_info = zone_country_info_input
    letter_price_info = letter_price_info_input
    parcel_price_info = parcel_price_info_input

    def __init__(self, weight=0, country_name="", item_type=""):
        self.unit_price = 0
        self.country_name = ""
        self.weight = 0
        self.zone_number = -1
        self.item_type = ""
        self.all_price_table = self.get_all_price_table()

    def get_price_table(self, price_info, item_type):
        if item_type == "letter":
            price_table = [0]*3
            weight_index = {'Up to 50g':0, 'Over 50g up to 250g':1, 'Over 250g up to 500g':2}
            for weight_opt, price_list in price_info.items():
                price_table[weight_index[weight_opt]] = [price_list[0], price_list[1],price_list[1],price_list[2],price_list[1]] + [price_list[2]]*4

        elif item_type == "parcel":
            price_table = [0]*9
            weight_index = {'Up to 500g':0, 'Up to 1kg':1, 'Up to 1.5kg':2,
                            'Up to 2kg':3, 'Up to 3kg':4, 'Up to 5kg':5,
                           'Up to 10kg':6, 'Up to 15kg':7,'Up to 20kg':8}

            for weight_opt, price_list in price_info.items():
                price_table[weight_index[weight_opt]] = price_list
        else:
            return -1

        return price_table

    def get_all_price_table(self):
        letter_price_info = self.letter_price_info
        parcel_price_info = self.parcel_price_info
        all_price_table={}

        all_price_table['letter'] = self.get_price_table(self.letter_price_info, 'letter')
        all_price_table['parcel'] = self.get_price_table(self.parcel_price_info, 'parcel')

        return all_price_table

    def get_weight_index(self, weight, item_type):
        weight_opt_letter = ['Up to 50g', 'Over 50g up to 250g', 'Over 250g up to 500g']
        weight_opt_parcel = ['Up to 500g', 'Up to 1kg', 'Up to 1.5kg', 'Up to 2kg',
                             'Up to 3kg', 'Up to 5kg', 'Up to 6kg', 'Up to 15kg','Up to 20kg']
        index = -1;

        if item_type == 'letter':
            if 0 < weight <= 0.05:
                index = 0
            elif 0.05 < weight <= 0.25:
                index = 1
            elif 0.25 < weight <= 0.5:
                index = 2
            else:
                index = -1
        elif item_type == 'parcel':
            if 0 < weight <= 0.5:
                index = 0
            elif 0.5 < weight <= 1:
                index = 1
            elif 1 < weight <= 1.5:
                index = 2
            elif 1.5 < weight <= 2:
                index = 3
            elif 2 < weight <= 3:
                index = 4
            elif 3 < weight <= 5:
                index = 5
            elif 5 < weight <= 6:
                index = 6
            elif 6 < weight <= 15:
                index = 7
            elif 15 < weight <= 20:
                index = 8
            else:
                index = -1
        else:
            index = -1

        return index

    def get_zone_index(self, zone):
        if zone in range(1,10):
            index = zone - 1
        else:
            index = -1

        return index

    def get_zone_number(self, country_name):
        zone_country_info = self.zone_country_info
        zone_number = -1
        zone_found = ''
        for zone, country_list in zone_country_info.items():
            #normalize country_name and country_list
            country_name_norm = country_name.strip().title()
            country_list_norm = [country_name_in_list.strip().title() for country_name_in_list in country_list]
            if country_name_norm in country_list_norm:
                zone_found = zone
                #parsing zone name to find zone_number
                zone_number = int(zone_found.split(' ')[1])
                break

        return zone_number

    def get_country_list(self):
        zone_country_info = self.zone_country_info
        country_list =[]
        for dummy,countries in zone_country_info.items():
            country_list += countries
        country_list = list(set(country_list))

        return country_list

    def construct_stamp_param(self, weight, country_name, item_type):

        zone_country_info = self.zone_country_info

        is_valid_country_name, country_name = self.validate_country_name(country_name)
        is_valid_item_type, item_type = self.validate_item_type(item_type)
        is_valid_weight, weight = self.validate_weight(weight,item_type)

        if not (is_valid_country_name and is_valid_item_type and is_valid_weight):
            return False

        zone_number = self.get_zone_number(country_name)

        self.country_name = country_name
        self.weight = weight
        self.zone_number = zone_number
        self.item_type = item_type

        return True


    def construct_stamp_user(self):
        is_valid = False
        while not is_valid:
            country_name = input('please input the country_name: ')
            is_valid, country_name = self.validate_country_name(country_name)

        is_valid = False
        while not is_valid:
            item_type_option = input('please input the item_type (0: letter | 1:parcel): ')
            item_type_option = item_type_option.strip()
            if item_type_option == '0':
                item_type = 'letter'
                is_valid = True
            elif item_type_option == '1':
                item_type = 'parcel'
                is_valid = True
            else:
                is_valid = False
                print('only option 0 or 1')

        is_valid = False
        while not is_valid:
            weight = input('please input the weight in kg: ')
            is_valid, weight = self.validate_weight(weight, item_type)


        return self.construct_stamp_param(weight, country_name, item_type)

    def get_zone_number(self, country_name):
        zone_country_info = self.zone_country_info
        zone_number = -1
        zone_found = ''
        for zone, country_list in zone_country_info.items():
            #normalize country_name and country_list
            country_name_norm = country_name.strip().title()
            country_list_norm = [country_name_in_list.strip().title() for country_name_in_list in country_list]
            if country_name_norm in country_list_norm:
                zone_found = zone
                #parsing zone name to find zone_number
                zone_number = int(zone_found.split(' ')[1])
                break

        return zone_number

    def calc_unit_price(self):
        zone_country_info = self.zone_country_info
        all_price_table = self.all_price_table
        price = -1
        weight = self.weight
        country_name = self.country_name
        item_type = self.item_type

        weight_index = self.get_weight_index(weight, item_type)
        zone_number = self.get_zone_number(country_name)
        zone_index = self.get_zone_index(zone_number)


        if -1 not in [weight_index, zone_index]:
            price = all_price_table[item_type][weight_index][zone_index]
            self.unit_price = price
        else:
            return -1

        return price

    def update_unit_price(self):
        price = self.calc_unit_price()
        if price != -1:
            self.unit_price = price
        else:
            print('invalid unit price, cannot update the price')

    def update_item_type(self, item_type):
        is_valid, item_type = self.validate_item_type(item_type)
        if is_valid:
            self.item_type = item_type
            self.update_unit_price()
        else:
            print('cannot update the stamp method')

    def update_weight(self, weight):
        is_valid, item_type = self.validate_weight(weight, self.item_type)
        if is_valid:
            self.weight = weight
            self.update_unit_price()
        else:
            return False

    def __eq__(self, other_item):
        if self.country_name == other_item.country_name and \
        self.item_type == other_item.item_type and \
        self.weight == other_item.weight:
            return True
        else:
            return False

    def __str__(self):
        text=''
        text+='{0:>15}: $ {1:<15.2f}\n'.format('unit_price', self.unit_price)
        text+='{0:>15}: {1:<15}\n'.format('country_name', self.country_name)
        text+='{0:>15}: {1:<15.4f}\n'.format('weight', self.weight)
        text+='{0:>15}: {1:<15}'.format('item_type', self.item_type)
        return text

    def validate_country_name(self, country_name):
        country_list = self.get_country_list()
        country_list_norm = [ country.strip().lower() for country in country_list]
        country_name_norm = country_name.strip().lower()
        if country_name_norm in country_list_norm:
            return True, country_name
        else:
            print('{0} does not exist in the country list.'.format(country_name))
            return False, ''

    def validate_weight(self, weight, item_type):
        if type(weight) == str:
            if self.is_float(weight):
                weight = float(weight)
            else:
                print("{0} is not a valid number".format(weight))
                return False, -1

        index = self.get_weight_index(weight, item_type)

        if index != -1:
            return True, weight
        else:
            weight_range_letter = '(0, 0.5]'
            weight_range_parcel = "(0, 20]"
            if item_type == 'letter':
                weight_range = weight_range_letter
            else:
                weight_range = weight_range_parcel
            print("{0} is not a valid weight, the valid range for {1} is {2}".format(weight, item_type, weight_range))
            return False, -1

    def validate_item_type(self, item_type):
        item_type = item_type.lower().strip()
        if item_type  in ['letter', 'parcel']:
            return True, item_type
        else:
            print(item_type + ' is not valid stamp method, choose between letter and parcel')
            return False, ''

    def is_float(self, number_txt):
        try:
            float(number_txt)
            return True
        except:
            return False
