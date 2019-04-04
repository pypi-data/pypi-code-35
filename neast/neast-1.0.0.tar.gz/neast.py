# def创建函数
def print_lol(the_list):
    for the_list_item in the_list:
        if isinstance(the_list_item, list):
            print_lol(the_list_item)
        else:
            print(the_list_item)
