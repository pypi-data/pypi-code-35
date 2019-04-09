def print_lol(the_list,level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			for stop_case in range(level):
				print("\t",end="")
			print(each_item)