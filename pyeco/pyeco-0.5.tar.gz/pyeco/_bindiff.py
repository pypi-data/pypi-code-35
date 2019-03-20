# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:34:23 2019

@author: getsense
"""
import numpy as np
from enum import Enum

class _adr_size(Enum):
    BYTE=1 #8 bits
    _NBITS=2 #_nbits размер слова

"""
_file1 - первый file,
_file2 - второй file,
_nbits - размер слова: 8,16,32 bits,
_size - сколько слов сравнивать
_flag - выводить adr в _nbits словах или в bytes  
_base_adr - некий base adr, нужен для реальной локации данных
"""
def bindiff(_file1,_file2,_nbits,_size,_flag,_base_adr):
    
    if(_nbits==8):
        dt = np.dtype('u1')
    if(_nbits==16):
        dt = np.dtype('u2')        
    if(_nbits==32):
        dt = np.dtype('u4')
 
    data1 = np.fromfile(_file1, dt, _size )
    data2 = np.fromfile(_file2, dt, _size )
    print(_file1+" | "+_file2)
    for idx, _i0 in enumerate(data1):
        if(_i0!=data2[idx]):
            if(_flag == _adr_size.BYTE):
                print(hex(_base_adr+idx*int(_nbits/8)) + ": " + hex(_i0) + " | " + hex(data2[idx]))
            else:
                if(_flag == _adr_size._NBITS):
                    print(hex(_base_adr+idx) + ": " + hex(_i0) + " | " + hex(data2[idx]))
    

                
    return 0x0





"""
tests
"""
#from pyeco import *
#from pyeco import _adr_size
#bindiff("e:/spil.bin","e:/u-boot.bin",32,int(0xce0/4),_adr_size.BYTE,0xe6300000)

