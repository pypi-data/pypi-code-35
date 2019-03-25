def print_lol(the_list,level=0):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,level+1)
        else:
		    print("\t"*level,end='')
            print(item)
