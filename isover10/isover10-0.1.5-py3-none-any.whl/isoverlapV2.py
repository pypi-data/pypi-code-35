import sys
def overlap(*args):
    print ('args = ', args)
    if '-h' in args:
        print ('yes')
        return None
    if len(args)!=2 or (len(args[0])!=2 or len(args[1]) !=2):
       print ('Incorrect usage!')
       print ('usage:', 'overlap((a,b),(c,d))')
       print ('Return True if one line overlaps the other line; \nReturn False if one line DOES not overlap the other, \nNone if there are missing values')
       return None
    
    '''
    Check whether two lines A (x1,x2) and B (x3,x4) on the x-axis whether they overlap or not
    Return True if A Line overlaps B Line; False otherwise
    '''
    def swap(X):
        '''
        this function does make sure the pair is ordered: 
        (a,b) where a<b 
        (10, -5) would become (-5, 10)
        '''
        if X[0]>X[1]:
            return (X[1],X[0])
        return X
    print (args)
    print ('len args 0=', len(args[0]))
    print ('len args 1=', len(args[1]))
    print ('a=',args[0][0])
    print ('b=',args[0][1])
    print ('c=',args[1][0])
    print ('d=',args[1][1])
    quit() 
    A, B = swap ( (args[0][0],args[0][1] )) ,swap ( (args[1][0],args[1][1]) )    

    '''
                  A0------------------A1
      B0------B1                          B0------B1
          if B1<A0 OR B0>A1 then
             Line B does NOT overlap Line A
          else
             Line B DOES ovelap Line A
    '''
    return not (B[1]<A[0] or B[0]>A[1])


#print (overlap((a,b),(c,d)))
'''
print (overlap((1,2),(0.1,1)))
print (overlap((1,2),(1,1)))
'''
print (overlap((1,2),('-h')))
print ('**')
print (overlap('-h'))
