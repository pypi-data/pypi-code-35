import math

pi180 = (math.pi/180.0)

def degrees_to_radians(angle) :
    return pi180 * float(angle)

def sin_degrees(angle) :
    return math.sin(degrees_to_radians(angle))

def cos_degrees(angle) :
    return math.cos(degrees_to_radians(angle))
