def logo():
	s=input()
	s1=sorted(s)
	dict1={}
	s1=list(set(s))
	dict1={s1[i]:s.count(s1[i]for i in range(len(s1)))}
	print((sorted(dict1.items(),key=lambda x: x[1],reverse=True))[0:3])







	
