#!/usr/bin/env python3

from collections import namedtuple

def dict_to_namedtuple(input_value) -> namedtuple:
    """Convert a dict to a nested namedtuple.

    This function recursively creates a namedtuple object representing the
    given input_value, wherein each nested dict is also converted into a
    namedtuple. If the supplied value is a list, it attempts to create a
    namedtuple for each element in the list. If it's anything else other than
    a dict, it'll return the original value.
    """
    # Check if it's a list.
    if type(input_value) == list:
        # If so, attempt to convert its elements into a namedtuple.
        return [dict_to_namedtuple(element) for element in input_value]
    elif type(input_value) != dict:
        # If it's not a dict and not a list, return it as-is.
        return input_value
    # We've got a dict. Let's convert it.
    # First, obtain a sorted list of the dictionary's keys.
    dict_keys = list(input_value.keys())
    dict_keys.sort()
    # Next, create a namedtuple with the given keys.
    NamedTuple = namedtuple("NamedTuple", dict_keys)
    # Next, create a list to store our values.
    dict_values = list()
    # Next, work through each key in turn, converting as necessary.
    for key in dict_keys:
        # Retrieve the value in input_value[key].
        value = input_value[key]
        # Attempt to convert it to a namedtuple, then add it to dict_values.
        dict_values.append(dict_to_namedtuple(value))
    # Create a namedtuple from the dict_values list.
    return_tuple = NamedTuple(*tuple(dict_values))
    # Return the namedtuple.
    return return_tuple

if __name__ == '__main__':
    # Demonstrate the function in action.

    # Create a demonstration dict.
    demo_dict = {
        "result": "success",
        "message_list": [
            {"id": 1, "msg": "sam called"},
            {"id": 2, "msg": "he wants his groove back"},
            {"id": 3, "msg": "he thinks you took it"},
        ],
        "errors": ["not enough jelly", "too much peanut butter", "no bread"],
        "nest": {
            "type": "bowl",
            "material": "straw",
        }
    }

    # Convert the dict to a namedtuple.
    demo = dict_to_namedtuple(demo_dict)

    # Display the contents of the dict.
    print(f"Result: {demo.result}")
    print("Messages:")
    for message in demo.message_list:
        print(f"  {message.id}: {message.msg}")
    print("Errors:")
    for error in demo.errors:
        print(f"  {error}")
    print(f"Nest: type='{demo.nest.type}', material='{demo.nest.material}'")
