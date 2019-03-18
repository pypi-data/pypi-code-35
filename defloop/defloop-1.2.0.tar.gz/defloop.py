"""this is simple def loop program"""
def defloop (the_list, level):
	for ilist in the_list:
		if isinstance(ilist, list):
			defloop(ilist)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(ilist)