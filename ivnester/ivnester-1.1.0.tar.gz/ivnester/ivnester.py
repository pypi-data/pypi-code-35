"""这是nester模块，提供了一个print_lol()的函数。"""

def print_lol(the_list, level=0):
    """这个函数取一个位置函数，名为“the_list”。"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
