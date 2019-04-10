"""
# list_to_number converts a list of numbers to a number

# number_to_list converts a number to a list of its digits

# list_to_string converts a list to a string

# string_to_list converts a string to a list

# divisors returns all divisors of a number

#permutations gives a list with all permutations of the elements of a list or a string

# Fib (n) returns the nth number from the fibinacci series

# fibo (n) returns a list up to and including the nth fibonacci number

# is_fibo (n) returns True or False depending on whether or not n occurs in the row of fibonacci numbers
insert(l,x), l is list of lists, x is one element
"""
# list_to_num makes a number from a list of digits

# num_to_list converts a number to a list of digits

# list_to_str makes a string from a list

# str_to_list makes a list from a string (the same as list() )

# divisors makes a list of all the divisors of a number

# permutations creates a list of all the permutations from a list or a string

# Fib(n) gives the n-th number from the fibinacci sequence

# fibo(n) gives a list of the first n numbers from the fibonacci sequence

# is_fibo(n) : True if a number is in the fibonacci sequence, else False

def list_to_num(gl):
    g = 0
    for c in gl: g = g * 10 + c
    return g

def num_to_list(g):
    gl = []
    while (g > 0):
        c = g%10
        gl = [c] + gl
        g = int(g/10)
    return gl

def list_to_str(sl):
    s = ''
    for l in sl: s += l
    return s

def str_to_list(s):
    l = []
    for i in range(0,len(s)): l += s[i]
    return l

def divisors(g):
    ldelers = [1,g]
    max = int(g**.5)
    for i in range(2,max+1):
        if (g%i == 0):
            if (i*i == g): ldelers = ldelers + [i]
            else: ldelers = ldelers + [i] + [int(g/i)]
    ldelers.sort()
    return ldelers

def voegin(l,x):
    r = []
    # l is lijst van lijsten, x is één element
    for hl in l:
        for i in range(0,len(hl)):
            h = hl[0:i] + [x] + hl[i:]
            if h not in r: r += [h]
        h = hl + [x]
        if h not in r: r += [h]
    return r

def permutations(l):
    s = []
    if type(l) == type('str'):
        s = 'str'
        l = string_naar_lijst(l)
    ll = len(l)
    if ll == 1: r = [l]
    else: r = voegin(permutaties(l[0:ll-1]),l[ll-1])
    if type(s) == type('str'):
        r2 = []
        for x in r: r2 += [lijst_naar_string(x)]
        return r2
    else: return r

def Fib(n):
    f1 = 1
    f2 = 2
    for i in range(3,n):
        f3 = f1 + f2
        f1 = f2
        f2 = f3

    return f3

def fibo(n):
    l = [0,1]
    for i in range(2,n+1): l += [l[i-1] + l[i-2]]

    return l

def is_fibo(n):
    teken = int(n/abs(n))
    k1 = 5*n*n + 4
    k2 = 5*n*n - 4*teken
    wk1 = int(k1**.5)
    wk2 = int(k2**.5)
    
    return ( wk1*wk1 == k1 or wk2*wk2 == k2)

    

def list_to_number(gl):
    #lijst naar getal
    g = 0
    for c in gl: g = g * 10 + c
    return g

def number_to_list(g):
    #getal naar lijst
    gl = []
    while (g > 0):
        c = g%10
        gl = [c] + gl
        g = int(g/10)
    return gl

def list_to_string(sl):
    #lijst naar string
    s = ''
    for l in sl: s += l
    return s

def string_to_list(s):
    # string naar lijst
    l = []
    for i in range(0,len(s)): l += s[i]
    return l

def divisors(g):
    #alle delers van g
    ldelers = [1,g]
    max = int(g**.5)
    for i in range(2,max+1):
        if (g%i == 0):
            if (i*i == g): ldelers = ldelers + [i]
            else: ldelers = ldelers + [i] + [int(g/i)]
    ldelers.sort()
    return ldelers

def insert(l,x):
    r = []
    # l is lijst van lijsten, x is één element
    for hl in l:
        for i in range(0,len(hl)):
            h = hl[0:i] + [x] + hl[i:]
            if h not in r: r += [h]
        h = hl + [x]
        if h not in r: r += [h]
    return r

def permutations(l):
    #alle perm. van elem in l
    s = []
    if type(l) == type('str'):
        s = 'str'
        l = string_naar_lijst(l)
    ll = len(l)
    if ll == 1: r = [l]
    else: r = voegin(permutaties(l[0:ll-1]),l[ll-1])
    if type(s) == type('str'):
        r2 = []
        for x in r: r2 += [lijst_naar_string(x)]
        return r2
    else: return r

def Fib(n):
    f1 = 1
    f2 = 2
    for i in range(3,n):
        f3 = f1 + f2
        f1 = f2
        f2 = f3

    return f3

def fibo(n):
    l = [0,1]
    for i in range(2,n+1): l += [l[i-1] + l[i-2]]

    return l

def is_fibo(n):
    teken = int(n/abs(n))
    k1 = 5*n*n + 4
    k2 = 5*n*n - 4*teken
    wk1 = int(k1**.5)
    wk2 = int(k2**.5)
    
    return ( wk1*wk1 == k1 or wk2*wk2 == k2)
__all__ = ['Fib', 'divisors', 'fibo', 'insert', 'is_fibo', 'list_to_number', 'list_to_string', 'number_to_list', 'permutations', 'string_to_list']

