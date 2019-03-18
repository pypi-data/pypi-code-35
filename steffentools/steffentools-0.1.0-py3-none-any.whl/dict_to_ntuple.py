"""The dict_to_ntuple module, containing the dict_to_ntuple function."""


from collections import namedtuple


def dict_to_ntuple(input_value):
    """Recursively convert a dict to a nested namedtuple.

    Parameters
    ----------
    input_value : any
        The input value to the function can be any type of data. If it is a
        dict, dict_to_ntuple will attempt to create a namedtuple from it,
        deriving attribute names from the dict's keys. If the input_value is
        a list, dict_to_ntuple will iterate over the list, attempting to
        convert each of its values to a namedtuple. If the input_value is any
        other data type, dict_to_ntuple will return it as-is.

    Returns
    -------
    return_tuple : namedtuple
        A nested namedtuple representing the original input_value with keys
        converted into attribute names.

    """
    # Check if it's a list.
    if isinstance(input_value, list):
        # If so, attempt to convert its elements into a namedtuple.
        return [dict_to_ntuple(element) for element in input_value]
    if not isinstance(input_value, dict):
        # If it's not a dict and not a list, return it as-is.
        return input_value
    if not input_value.keys():
        # The dictionary has no entries. Return the empty dict.
        return input_value
    # We've got a dict with entries. Let's convert it.
    # First, obtain a sorted list of the dictionary's keys.
    dict_keys = list(input_value.keys())
    dict_keys.sort()
    # Next, create a namedtuple with the given keys.
    ntuple = namedtuple("ntuple", dict_keys)
    # Next, create a list to store our values.
    dict_values = list()
    # Next, work through each key in turn, converting as necessary.
    for key in dict_keys:
        # Retrieve the value in input_value[key].
        value = input_value[key]
        # Attempt to convert it to a namedtuple, then add it to dict_values.
        dict_values.append(dict_to_ntuple(value))
    # Create a namedtuple from the dict_values list.
    return_tuple = ntuple(*tuple(dict_values))
    # Return the namedtuple.
    return return_tuple


if __name__ == "__main__":
    # Demonstrate the function in action.

    # Create a demonstration dict.
    DEMO_DICT = {
        "result": "success",
        "message_list": [
            {"id": 1, "msg": "sam called"},
            {"id": 2, "msg": "he wants his groove back"},
            {"id": 3, "msg": "he thinks you took it"},
        ],
        "errors": ["not enough jelly", "too much peanut butter", "no bread"],
        "nest": {"type": "bowl", "material": "straw"},
    }

    # Convert the dict to a namedtuple.
    DEMO = dict_to_ntuple(DEMO_DICT)

    # Display the contents of the dict.
    print(f"Result: {DEMO.result}")
    print("Messages:")
    for message in DEMO.message_list:
        print(f"  {message.id}: {message.msg}")
    print("Errors:")
    for error in DEMO.errors:
        print(f"  {error}")
    print(f"Nest: type='{DEMO.nest.type}', material='{DEMO.nest.material}'")
