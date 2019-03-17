#Package created by Tinos Psomadakis
#Version 0.0.7
import webbrowser
import os
import math
from .constants import *

try:
    io=open("intro.txt","r+")
    a=io.read()
    print(a)
    io.close()
except FileNotFoundError as o:
    pass

def intro():
    os.remove("intro.txt")
    
def version():
    print('''
Currently running Version tiquations 0.0.7a
Changelog:
-Fixed up file formatting with __init__.py, equations.py and constants.py
-Added energy, potential difference and charge equations
-Added power, current and potential difference equations
-Fixed typo with delta_velocity
-Renamed tiquations.vars() to tiquations.variables()
-To access the old vars() command, type constants.variables(). This will give you a list of the constants.
-Added intro that can be disabled, read help() for info.

0.0.7a:
Hotfix to fix code-breaking bug

''')

#Quadratic formula solver
def quadratic(num1,num2,num3):
    result1 = (-num2 + math.sqrt(num2**2 - (4 * (num1) * (num3))))
    ans1 = (result1 / (2 * num1))
    print("Positive value: ")
    print(ans1)
    print("-------------------------------------------------------------")
    print("Negative value: ")
    result2 = (-num2 - math.sqrt(num2**2 - 4 * (num1) * (num3)))
    ans2 = (result2 / (2 * num1))
    print(ans2)


#Solve distance using speed and time
def distance_dst(speed, time):
    result = speed*time
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve speed using distance and time
def speed_dst(distance, time):
    result = distance/time
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve time using speed and distance
def time_dst(distance, speed):
    result = distance/speed
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve force using mass and acceleration
def force_fma(mass,acceleration):
    result = mass*acceleration
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve mass using force and acceleration
def mass_fma(force,acceleration):
    result = force/acceleration
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve acceleration using mass and force
def acceleration_fma(force,mass):
    result = force/mass
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve weight using mass and gravitational field strength
def weight_wmg(mass, gravitational_field_strength):
    result = mass*gravitational_field_strength
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve mass using weight and gravitational field strength
def mass_wmg(weight, gravitational_field_strength):
    result = weight/gravitational_field_strength
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve gravitational field strength using weight and mass
def gravity_wmg(weight, mass):
    result = weight/mass
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve for area of circle using radius
def circle_area_rad(radius):
    result = pi*(radius**2)
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve for area of circle using diameter
def circle_area_dia(diameter):
    result = (1/4)*(pi*(diameter**2))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve for diameter of circle using radius
def circle_diam_rad(radius):
    result = radius*2
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve for diameter of circle using area
def circle_diam_are(area):
    result = 2*(math.sqrt(area/pi))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve for circumference of circle using area
def circle_circum(radius):
    result = 2*(pi*radius)
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve acceleration using Change in velocity and time
def acceleration_avt(delta_velocity,time):
    result = delta_velocity/time
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve Change in velocity using acceleration and time
def delta_velocity_avt(acceleration,time):
    result = acceleration*time
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve time taken using acceleration and change in velocity
def time_avt(acceleration,delta_velocity):
    result = delta_velocity/acceleration
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve pressure using force and area
def pressure_fpa(force, area):
    result = force/area
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve force using pressure and area
def force_fpa(pressure, area):
    result = pressure/area
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve area using pressure and force
def area_fpa(force, pressure):
    result = force*pressure
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve volume of a cylinder
def cylinder_vol(radius,height):
    result = pi*(radius**2*(height))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve surface area of a cylinder
def cylinder_surface_are(radius,height):
    result = (2*(pi*radius*height))+2*(pi*(radius**2))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve area of a trapezoid
def trapezoid_area(base_short,base_long,height):
    result = ((base_short+base_long)/2)*height
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve height of a trapezoid
def trapezoid_height(base_short,base_long,area):
    result = 2*(area/(base_short+base_long))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
#Solve surface area of a trapezoid
def trapezoid_surface_are(base_short,base_long,height):
    result = ((base_short+base_logn)/2)*height
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve a using pythagoras
def pythagoras_a(b,c):
    result = math.sqrt((c**2)-(b**2))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

#Solve b using pythagoras
def pythagoras_b(a,c):
    result = math.sqrt((c**2)-(a**2))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit) 
    
#Solve c using pythagoras
def pythagoras_c(a,b):
    result = math.sqrt((a**2)+(b**2))
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
def energy_evq(potential_difference,charge):
    result = potential_difference*charge
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

def potential_dif_evq(energy,charge):
    result = energy/charge
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

def charge_evq(energy,potential_difference):
    result = energy/potential_difference
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
def power_piv(current, potential_difference):
    result = current*potential_difference
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)

def current_piv(power, potential_difference):
    result = power/potential_difference
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
def potential_dif_piv(power, current):
    result = power/current
    unit = input("What unit are you measuring the distance in?")
    print(result,unit)
    
def power_pet(energy,time):
    result = energy/time
    
def help():
    webbrowser.open_new_tab('https://tinosps.wixsite.com/tiquations')
    #General
    print('''
A python package containing useful equations for science and maths.
Created by Tinos Psomadakis\n
          ''')
    #Commands
    print("To disable the thank you intro, do tiquations.intro()\n")
    print('''
Commands:

quadratic(a,b,c) - Find quadratic formula from an equation like 3x^2+6x+2 = 0 where a=3, b=6 and c=2.
distance_dst(speed,time) - Find distance using speed and time
speed_dst(distance,time) - Find speed using distance and time
time_dst(distance,speed) - Find time using distance and speed
force_fma(mass,acceleration) - Find force using mass and acceleration
mass_fma(force,acceleration) - Find mass using force and acceleration
acceleration_fma(force,mass) - Find acceleration using force and mass
weight_wmg(mass, gravitational_field_strength) - Find weight using mass and gravitational field strength
mass_wmg(weight, gravitational_field_strength) - Find mass using weight and gravitational field strength
gravity_wmg(weight, mass) - Find gravitational field strength using weight and mass
circle_area_rad(radius) - Find area of a circle using radius
circle_area_dia(diameter) - Find area of a circle using diameter
circle_diam_rad(radius) - Find diameter of a circle using radius
circle_diam_are(area) - Find diameter of a circle using area
circle_circum(radius) - Find circumference of a circle
acceleration_avt(delta_velocity,time) - Find acceleration using change in velocity and time
delta_velocity_avt(acceleration,time) - Find change in velocity using acceleration and time
time_avt(acceleration,delta_velocity) - Find time taken using change in velocity and acceleration
pressure_fpa(force, area) - Find pressure using force and area
force_fpa(pressure, area) - Find force using pressure and area
area_fpa(force, pressure) - Find area using force and pressure
cylinder_vol(radius,height) - Find volume of cylinder
cylinder_surface_are(radius,height) - Find surface area of cylinder
trapezoid_area(base_short,base_long,height) - Find area of trapezoid
trapezoid_height(base_short,base_long,area) - Find height of trapezoid
trapezoid_surface_are(base_short,base_long,height) - Find surface are of trapezoid
pythagoras_a(b,c) - Solve for a in equation a²+b²=c²
pythagoras_b(a,c) - Solve for b in equation a²+b²=c²
pythagoras_c(a,b) - Solve for c in equation a²+b²=c²
energy_evq(potential_difference,charge) - Find energy using potential difference and charge
potential_dif_evq(energy,charge) - Find potential difference using energy and charge
charge_evq(energy,potential_difference) - Find charge using energy and potential difference
power_piv(current, potential_difference) - Find power using current and potential difference
current_piv(power, potential_difference) - Find current using power and potential difference
potential_dif_piv(power, current) - Find potential difference using power and current

Usage:
tiquations.example_xyz(5,72)
tiquations.quadratic(1,2,-3)

          ''')
    
    #Built-in variables
    print('''
Built-in varaibles:
earth_g - Earth's gravitational pull strength in m/s² = 9.807
moon_g - The moon's gravitational pull strength in m/s² = 1.62
mars_g - Mars' gravitational pull strength in m/s² = 3.711
jupiter_g - Jupiter's gravitational pull strength in m/s² = 24.79
neptune_g - Neptune's gravitational pull strength in m/s² = 11.15
mercury_g - Mercury's gravitational pull strength in m/s² = 3.7
saturn_g - Saturn's gravitational pull strength in m/s² = 10.44
uranus_g - Uranus' gravitational pull strength in m/s² = 8.87
venus_g - Venus' gravitational pull strength in m/s² = 8.87
pluto_g - Pluto's gravitational pull strength in m/s² = 0.62
pi - First 16 numbers of pi = 3.141592653589793

Usage:
tiquations.example(pi,67)
tiquations.weight_wmg(52, earth_g)

Type constants.variables() to see a full list with attached values
        ''')
