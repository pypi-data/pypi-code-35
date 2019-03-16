def func():
    s=input()
    g1=""
    g2=""
    g3=""
    f=""
    sl1=[]
    sl2=[]
    sl3=[]
    k=len(s)
    dict1={}
    dict2={}
    l2=[]
    for i in range(k):
        ch=s[i]
        c=0
        for j in range(k):
        
            if(s[i]==s[j]):
                
                c=c+1
            
        dict1.update({s[i]:c})
    l1=list(dict1.values())
    listlen=len(l1)
    for j in range(listlen):
        for j1 in range(j+1,listlen):
            if(l1[j]==l1[j1]):
                l1[j1]=0
    l1.sort(reverse=True)
    l2=list(dict1.keys())
    for b in range(listlen):
        if(dict1[l2[b]]==l1[0]): 
            g1=g1+l2[b]  
        if(dict1[l2[b]]==l1[1]):
            g2=g2+l2[b]
        if(dict1[l2[b]]==l1[2]):
            g3=g3+l2[b]
    for c in range(len(g1)):
        sl1.append(g1[c])
    for c in range(len(g2)):
        sl2.append(g2[c])
    for c in range(len(g3)):
        sl3.append(g3[c])
   
    sl1.sort()
    sl2.sort()
    sl3.sort()
    if(len(sl1) >= 3):
        for x1 in range(0,3):
            print(sl1[x1],l1[0],sep=' ')
    else:
        for x2 in range(0,len(sl1)):
            print(sl1[x2],l1[0],sep=' ')
        if(len(sl2) >=3-len(sl1)):
            for y1 in range(0,(3-len(sl1))):
                            
                            print(sl2[y1],l1[1],sep=' ')
        else:
            for y2 in range(0,len(sl2)):
                            print(sl2[y2],l1[1],sep='' )
            print(sl3[0])                


