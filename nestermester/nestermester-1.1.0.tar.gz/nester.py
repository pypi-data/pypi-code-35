def print_lol(the_list, num_tabs=0, show_depth=False, list_depth=0):
    """This fucntion takes positional argument called "the_list", which 
    is a Python3 list (of - possibly - nested lists). Each data item in
    the list is recursively printed on the screen in it's own line.
    -------------------------------------------------------------------
    The second argument is called "num_tabs" and will offset every line
    by number of tabs. Default value is zero.
    -------------------------------------------------------------------
    The third argument is a bool that controls visualisation of lists'
    depth. Default value is False.
    -------------------------------------------------------------------
    The forth argument is called "list_depth" and initially is equal to
    zero.It will be incremented depending how deep the list is nested 
    inside.
    """
    for list_item in the_list:
        if isinstance(list_item, list):
            print_lol(list_item, num_tabs, show_depth, list_depth+1)
        else:
            for tab in range(num_tabs):
                print("\t", end="")
            if show_depth:
                for tab in range(list_depth):
                    print("\t", end="")
            print(list_item)



print_lol([3,3,3,[3,3,3]],1,True)