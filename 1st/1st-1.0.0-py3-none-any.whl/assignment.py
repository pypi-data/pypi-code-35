def abc():
    s=input()
    s1=sorted(s)
    s2=list(set(s1))
    s2=sorted(s2)
    dic={s2[i]:s1.count(s2[i])for i in range(len(s2))}
    dic1=((sorted(dic,key=dic.get,reverse=True))[0:3])
    print(dic1)
    
if (__name__=="__abc__"):
    main()
