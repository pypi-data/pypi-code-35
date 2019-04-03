
# class savelist(object):
def write(data):
	r=""
	for i in data:
		r+=str(i)+"\n"
	return r.strip()
	# if type(data) is list:
	#   r=""
	#   for i in data:
	#       r+=str(i)+"\n"
	#   return r.strip()
	# elif type(data) is str:


def read(data):
	if type(data) is str:
		l=[]
		for i in data.strip().split("\n"):
			l.append(i)
		return l
	
	elif type(data) is list:
		l=[]
		for i in data:
			l.append(i.strip())
		return l

# def write(data):
# 	r=""
# 	for i in data:
# 		r+=str(i)+"\n"
# 	return r.strip()
# 	# if type(data) is list:
# 	# 	r=""
# 	# 	for i in data:
# 	# 		r+=str(i)+"\n"
# 	# 	return r.strip()
# 	# elif type(data) is str:


# def read(data):
# 	if type(data) is str:
# 		l=[]
# 		for i in data.strip().split("\n"):
# 			l.append(i)
# 		return l
	
# 	elif type(data) is list:
# 		l=[]
# 		for i in data:
# 			l.append(i.strip())
# 		return l