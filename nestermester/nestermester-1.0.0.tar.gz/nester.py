def print_lol(the_list):
    for list_item in the_list:
        if isinstance(list_item, list):
            print_lol(list_item)
        else:
            print(list_item)