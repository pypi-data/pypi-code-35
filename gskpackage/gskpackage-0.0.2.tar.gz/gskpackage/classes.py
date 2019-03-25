"""
__count ------ private variable
_count  ----  protected
count  ---- public
"""

class Employee:
    """ Document string for Employee class"""
    static_value = 0

    def __init__(self):
        print("constructor")
        self.salary = 0

    def __new__(self):
        print("new")
        return object.__new__(Employee)

    def __del__(self): #destructor
        print("destructor")

    def cal_salary(self,salary):
        ''' Document string for cal_salary method'''
        self.salary = salary
        return self.salary

    @staticmethod
    def f1():
        return "static method"

e = Employee()
print(e.cal_salary(56))
print(e.__doc__)
print(e.cal_salary.__doc__)
print(Employee.f1())

"""
Inheritance
Data hiding

"""

"""
class simplest:
    pass

s=simplest()
s.rate = 10 #attaches an attribute rate to the instance s
"""