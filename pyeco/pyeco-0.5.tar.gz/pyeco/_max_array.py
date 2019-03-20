# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 22:11:14 2019

@author: Nikita Kuzin
"""

"""
in_array - входной массив
func вычисляет MAX значение числа из массива in_array 
"""
def max_array(in_array):
    max_i=0
    for i, _num in enumerate(in_array):
        if(_num>in_array[max_i]): #_num есть in_array[i]
            max_i=i
    print("MAX num -> " + str(in_array[max_i]))

"""
tests
"""
"""
import numpy as np
in_array = np.array([-176,3,148,-10,36,238,-76])
max_array(in_array)
"""
"""
в можно было так:
print(in_array.max())
"""