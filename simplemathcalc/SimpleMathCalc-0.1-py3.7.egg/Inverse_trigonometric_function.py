# -*- coding: utf-8 -*-
# if you want to calculatea a inverse trigonometric function，
#please input inversetrig("function",number)
#when you import this py
import math
def inversetrig(function,number):
    if function == "asin":
        result= math.asin(float(number))
        print(result)
    elif function =="acos":
        result = math.acos(float(number))
        print(result)
    elif function =="atan":
        result = math.atan(float(number))
        print(result)
# Our group's package is uploaded in account 4320180939871.