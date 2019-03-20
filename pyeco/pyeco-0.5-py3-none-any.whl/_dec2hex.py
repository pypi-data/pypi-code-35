# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:34:23 2019

@author: getsense
"""
import ctypes
from enum import Enum

"""
dec2hex(_dec,_nbits)
_dec -> input decimal: 
8 bits[-128,127], 
16 bits[-32768,32767], 
32 bits[-2147483648,2147483647] 
_nbits -> _dec's number bits: 8,16,32
"""
def dec2hex(_dec,_nbits):
    
    if(_nbits==8):
        _j0=ctypes.c_uint8(_dec)
    if(_nbits==16):
        _j0=ctypes.c_uint16(_dec)        
    if(_nbits==32):
        _j0=ctypes.c_uint32(_dec) 
 
                
    return hex(_j0.value)

"""
hex2dec(_hex,_nbits,_type_sign)
"""
class _type_sign(Enum):
    SIGN=1
    UNSIGN=2
    
def hex2dec(_hex,_nbits,_s):
    if((_nbits==8) and (_s==_type_sign.SIGN)):
        _j0=ctypes.c_int8(_hex)
    if((_nbits==8) and (_s==_type_sign.UNSIGN)):
        _j0=ctypes.c_uint8(_hex)        

    if((_nbits==16) and (_s==_type_sign.SIGN)):
        _j0=ctypes.c_int16(_hex)
    if((_nbits==16) and (_s==_type_sign.UNSIGN)):
        _j0=ctypes.c_uint16(_hex)

    if((_nbits==32) and (_s==_type_sign.SIGN)):
        _j0=ctypes.c_int32(_hex)
    if((_nbits==32) and (_s==_type_sign.UNSIGN)):
        _j0=ctypes.c_uint32(_hex)

        
    return _j0.value

"""
dec2bin(_dec,_nbits)
"""
def dec2bin(_dec,_nbits):
    
    if(_nbits==8):
        _j0=ctypes.c_uint8(_dec)
    if(_nbits==16):
        _j0=ctypes.c_uint16(_dec)        
    if(_nbits==32):
        _j0=ctypes.c_uint32(_dec) 
 
                
    return bin(_j0.value)


"""
bin2dec(_bin,_nbits,_type_sign)
"""
def bin2dec(_bin,_nbits,_s):
    if((_nbits==8) and (_s==_type_sign.SIGN)):
        _j0=ctypes.c_int8(int(_bin,2))
    if((_nbits==8) and (_s==_type_sign.UNSIGN)):
        _j0=ctypes.c_uint8(int(_bin,2))        

    if((_nbits==16) and (_s==_type_sign.SIGN)):
        _j0=ctypes.c_int16(int(_bin,2))
    if((_nbits==16) and (_s==_type_sign.UNSIGN)):
        _j0=ctypes.c_uint16(int(_bin,2))

    if((_nbits==32) and (_s==_type_sign.SIGN)):
        _j0=ctypes.c_int32(int(_bin,2))
    if((_nbits==32) and (_s==_type_sign.UNSIGN)):
        _j0=ctypes.c_uint32(int(_bin,2))

        
    return _j0.value

"""
hex2bin(_hex,_nbits)
"""
def hex2bin(_hex,_nbits):
    
    if(_nbits==8):
        _j0=ctypes.c_uint8(_hex)
    if(_nbits==16):
        _j0=ctypes.c_uint16(_hex)        
    if(_nbits==32):
        _j0=ctypes.c_uint32(_hex) 
 
                
    return bin(_j0.value)

"""
bin2hex(_bin,_nbits)
"""

def bin2hex(_bin,_nbits):
    
    if(_nbits==8):
        _j0=ctypes.c_uint8(int(_bin,2))
    if(_nbits==16):
        _j0=ctypes.c_uint16(int(_bin,2))        
    if(_nbits==32):
        _j0=ctypes.c_uint32(int(_bin,2)) 
 
                
    return hex(_j0.value)


"""
tests
"""
#from pyeco import *
#from pyeco import _type_sign

#print(dec2hex(-127,8))
#print(hex2dec(0x81010181,32,_type_sign.UNSIGN))
#print(dec2bin(-128,16))
#print(bin2dec("11111111111111111111111110000000",32,_type_sign.UNSIGN))
#print(bin2hex("1100000000000011",16))
#print(hex2bin(0x81010181,32))
