# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def dec_hex(str1): #十转十六
    a = str(hex(eval(str1)))
    b = a.replace("0x",'')
    print('十进制  \t%s\t十六进制\t%s'%(str1, a))
    return b
 
def hex_dec(str2): #十六转十
    b = eval("0x" + str2)
    a = str(b).replace("0x",'')
    print('十六进制\t%s\t十进制  \t%s'%(str2, a))
    return b
 
if __name__ == '__main__':
    str1 = "16" # 十进制
    str2 = "10" # 十六进制
    print(dec_hex(str1))
    print(hex_dec(str2))
    #Our group's package is uploaded in account 4320180939871