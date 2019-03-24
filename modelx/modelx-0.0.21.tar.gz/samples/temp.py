import modelx as mx

def parent_param(x):

    if x == 0:
        bases = [Base1]
    else:
        bases = [Base2]

    return {'bases': bases}


def child_param(y):
    return {'bases': [ChildBase1, ChildBase2]}


def cells1(i):
    return 100 * i


def cells2(i):
    return 200 * i


def cells3(i):
    return 300 * x * y * i


def cells4(i):
    return 400 * x * y * i


model = mx.new_model(name='sample_dynamic_model')

base1 = model.new_space(name='Base1')
base2 = model.new_space(name='Base2')

base1.new_cells(formula=cells1)
base2.new_cells(formula=cells2)

parent = model.new_space(name='Parent', formula=parent_param)
child = base2.new_space(name='Child', formula=child_param)

child.new_space(name='ChildBase1').new_cells(formula=cells3)
child.new_space(name='ChildBase2').new_cells(formula=cells4)

parent.Base1 = base1
parent.Base2 = base2


c = parent[1].Child


impl = c._impl
