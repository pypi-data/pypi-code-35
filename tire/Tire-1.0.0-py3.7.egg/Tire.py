def Tire():
    s=input()
    s1=sorted(s)
    s2=list(set(s1))
    s2=sorted(s2)
    dict2={s2[i]:s1.count(s2[i])for i in range(len(s2))}
    dict1=((sorted(dict2, key=dict2.get, reverse=True))[0:3])
    print(dict1)
print(Tire())    

