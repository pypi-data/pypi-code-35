"""
This is a test module, which can flatter a list, up to 3 levels
"""


def print_lol(the_list, level=0):
    for i in the_list:
        if isinstance(i, list):
            print_lol(i, level + 1)  # use recursive is more clear
        else:
            for tab in range(level):
                print("\t", end="")
            print(i)
