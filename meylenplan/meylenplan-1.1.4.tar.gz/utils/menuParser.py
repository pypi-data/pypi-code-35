import os
import re
import subprocess

from data.menu import Menu
from data.day import Day
from data.meal import Meal
from data.price import Price
from data.date import Date

def parse_menu(text_file):
    try:
        lines = read_file(text_file)
    except FileNotFoundError:
        raise

    lines = filter_garbage(lines)
    lines, valid_from, valid_to = filter_dates(lines)
    meals = create_meals(lines)
    days  = create_day_menus(meals)
    menu = create_menu(days, valid_from, valid_to)
    return menu


def read_file(txt_path):

    with open(txt_path, 'r') as file:
        lines = file.readlines()

    # remove whitespace characters like `\n` at the end of each line
    lines = [line.strip() for line in lines]
    # remove empty lines
    lines = [line for line in lines if line]

    return lines


def filter_garbage(lines):
    filtered_lines = []
    # We are not able to distinguish between a short meal description and a
    # short sentence.
    garbage_pattern = re.compile(
            # Add anything which can't be a meal
            r'.*Bestellungen|'
            r'^040|'
            r'.*Speisen|'
            r'Mitnehmen|'
            r'Ta g e s k a r t e|'
            r'Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag|'
            r'^Intern|^Extern|'
            r'^Normal \/ Groß|'
            r'.*Farbstoff|.*Konservierungsstoffen|.*Antioxidationsmittel|'
            r'.*Geschmacksverstärker|.*Schwefeldioxid|.*Eisensalze|.*Phosphat|'
            r'Z:'
            )

    for line in lines:
        match = re.match(garbage_pattern, line)
        if not match:
            filtered_lines.append(line)

    return filtered_lines


def filter_dates(lines):
    filtered_lines = []
    date_pattern = re.compile(
            # Python doesn't support atomic (non-capturing) groups, sorry
            r'([0-3]{0,1}[0-9]{1})' # Day
            r'(\.|\,){1,}' # Dot or comma between day and month
            r'([0-3]{0,1}[0-9]{1})' # Month
            r'.*(\.|\,)*\s*(\–|\-)\s*' # Possible year and separation between the dates
            r'([0-3]{0,1}[0-9]{1})' # Day
            r'(\.|\,){1,}' # Dot or comma between day and month
            r'([0-3]{0,1}[0-9]{1})' # Month
            r'.*' # Possible garbage
            )

    for line in lines:
        match = re.match(date_pattern, line)
        if match:
            # Python doesn't support atomic (non-capturing) groups, sorry
            valid_from = Date(match[1], match[3])
            valid_to = Date(match[6], match[8])
        else:
            filtered_lines.append(line)

    return filtered_lines, valid_from, valid_to


def create_meals(lines):
    single_prices = []
    meals = []

    # \d+[\,\.]+\d+€ price (sometimes they mix up , and .)
    price_pattern = re.compile(r'(\d+)[\,\.]+(\d+)€')

    # (.+) meal
    # \(([\w\,\.]*)\) additives encapsulated by braces
    # ([\w\,\.]*) additives (sometimes they mix up , and .)
    meal_pattern = re.compile(r'(.+)\(([\w\,\.]*)\)')

    # Match friday's dessert which doesn't have a price and is for sure without any additives ;)
    free_dessert_pattern = re.compile(r'.*dessert', flags = re.IGNORECASE)

    # Arbitrary data
    arbitrary_pattern = re.compile(r'.*')

    for line in lines:
        match = re.match(price_pattern, line)
        if match:
            single_prices.append(float(match[1]) + float(match[2]) / 100)
            continue
        else:
            match = re.match(meal_pattern, line)
            if match:
                meals.append(Meal(name=match[1], additives=match[2]))
                continue
            match = re.match(free_dessert_pattern, line)
            if match:
                meals.append(Meal(name=match[0], additives=None))
                continue
            match = re.match(arbitrary_pattern, line)
            if match:
                meals.append(Meal(name = match[0], additives=None, potentially_not_a_meal=True))
                continue

    # Intern and extern price for each meal
    # Substract free dessert which deesn't have a price
    assert(len(single_prices) == (len(meals) - 1) * 2)
    assert(len(single_prices) % 2 == 0)

    # Combine intern and extern price
    prices = []
    for i in range(0, len(single_prices), 2):
        price_matches = [single_prices[i], single_prices[i + 1]]
        price_matches.sort()
        prices.append(Price(price_matches[0], price_matches[1]))

    # Append free dessert price
    prices.append(Price(0.0, 0.0))

    assert(len(prices) == len(meals))
    for (meal, price) in zip(meals, prices):
        meal.price = price

    return meals


def create_day_menus(meals):
    assert(len(meals) % 5 == 0)

    days = [Day(0, meals[0:5]),
            Day(1, meals[5:10]),
            Day(2, meals[10:15]),
            Day(3, meals[15:20]),
            Day(4, meals[20:25]),
            Day(5, None),
            Day(6, None)
            ]

    return days


def create_menu(days, valid_from, valid_to):
    return Menu(days, valid_from, valid_to)

