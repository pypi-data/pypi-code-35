# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 08:19:47 2018

@author: a.teffal
"""

import Effectifs as eff
import pandas as pd
import time
import Actuariat as act

#%%

#Define some laws
def law_ret1(age, year_emp):
    if year_emp < 2002:
        if age+1 >= 55:
            return True
        else:
            return False
    if year_emp >= 2002:
        if age+1 >= 60:
            return True
        else:
            return False
        
        
def law_ret2(age):
    if age+1 >= 55:
        return True
    else:
        return False
    

def law_ret3(age, sexe):
    if sexe == 'female':
        if age+1 >= 55:
            return True
        else:
            return False
    if sexe == 'male':
        if age+1 >= 60:
            return True
        else:
            return False 



def law_resignation_1(age, sexe):

    if age+1 >= 50 :
        return 0
    if sexe == 'female':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01
    if sexe == 'male':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01
    



def law_mar1(age, sexe, typeAgent):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """
    if sexe == 'male':
        if typeAgent=='active':
            if age >= 25 and age <= 54:
                return 0.095
            else :
                return 0
        else:
            return 0
    
    if sexe == 'female':
        if typeAgent=='active':
            if age >= 25 and age <= 54:
                return 0.15
            else :
                return 0
        else:
            return 0
    
    
def law_replacement1(departures_, year_):
    
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : sex, age, number and group
        
    '''
    new_employees = []

    for g in departures_:
        temp = {'sex':'male', 'age' : 30, 'number':departures_[g],'group':g}
        new_employees.append(temp)
    
    return new_employees


    

# Path for input data
path ="./data/"

# Start Time 
t1 = time.time()

# Number of years to project
MAX_ANNEES = 50

# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

# Summary informations about input data
print("employees : ", len(employees))
print(employees.head(5))
print("spouses : ", len(spouses))
print(spouses.head(5))
print("children : ", len(children))
print(children.head(5))


# Projection of population
numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, (law_ret1, ['age', 'Year_employment']), 
                    (law_resignation_1, ['age', 'sex']), (law_mar1, ['age', 'sex','type']), law_replacement_ = None)

# Global numbers
Effectifs = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

Effectifs.to_csv('Effectifs_python.csv', sep = ';', index=False, decimal=',')

#Number of actives leaving population : deaths, resignations, and new retired
Leaving = eff.leavingNumbers(numbers_[0], numbers_[4], MAX_ANNEES)

Leaving.to_csv('Sortants_python.csv', sep = ';', index=False, decimal=',')


#export projected employees
pd.DataFrame.from_dict(numbers_[0]).to_csv('employees_proj.csv', sep = ';', index=False, decimal=',')

#export projected spouses
pd.DataFrame.from_dict(numbers_[1]).to_csv('spouses_proj.csv', sep = ';', index=False, decimal=',')

#export projected children
pd.DataFrame.from_dict(numbers_[2]).to_csv('children_proj.csv', sep = ';', index=False, decimal=',')

# End time
t2 = time.time()

#Print start time, end time and duration
print("Début :", time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(t1)))
print("Fin :", time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(t2)))
print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%




