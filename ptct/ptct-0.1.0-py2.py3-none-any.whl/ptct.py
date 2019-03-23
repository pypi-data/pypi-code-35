# -*- coding: utf-8 -*-

"""Main module."""

import logging
logger = logging.getLogger(__name__)

name_map = {
    "Rankine": "R",
    "Kelvin": "K",
    "Fahrenheit": "F",
    "Celsius": "C"
}


def to_kelvin(value, unit):
    kmap = {
        'C': (lambda c: c + 273.15),
        'F': (lambda f: (f + 459.67) / 1.8),
        'R': (lambda r: r / 1.8),
        'K': (lambda k: k)
    }
    return kmap[unit](float(value))


def to_celsius(value, unit):
    k = to_kelvin(value, unit)
    return k - 273.15


def to_fahrenheit(value, unit):
    k = to_kelvin(value, unit)
    return k * 1.8 - 459.67


def to_rankine(value, unit):
    k = to_kelvin(value, unit)
    return k * 1.8


def convert(value, unit, target):
    # Convert to short name
    if target in name_map.keys():
        target = name_map[target]
    if unit in name_map.keys():
        unit = name_map[unit]
    if unit not in ['K', 'C', 'F', 'R']:
        logger.error("{} is not a supported unit type".format(unit))
        return
    try:
        if target == 'K':
            return to_kelvin(value, unit)
        elif target == 'C':
            return to_celsius(value, unit)
        elif target == 'F':
            return to_fahrenheit(value, unit)
        elif target == 'R':
            return to_rankine(value, unit)
        else:
            logger.error("{} is not a supported unit type".format(target))
            return
    except ValueError:
        logger.error("Could not convert the value {} {}".format(value, unit))
        return None


def check(result, response):
    try:
        if result is None:
            return "invalid"
        elif response is not None:
            return "correct" if int(response) == int(result) else "incorrect"
        return result
    except ValueError:
        return "incorrect"
