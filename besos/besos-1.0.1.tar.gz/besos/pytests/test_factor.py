import pytest
import pandas as pd
from pandas import DataFrame as DF
import numpy as np

from sklearn import svm, pipeline, linear_model
from sklearn.preprocessing import StandardScaler

import eppy_funcs as ef
from evaluator import EvaluatorEP, EvaluatorSR
from parameters import RangeParameter, CategoryParameter, Parameter, FieldSelector
from problem import EPProblem
import sampling

def test_factor():
    building = ef.get_building()

    parameters = [
                Parameter(FieldSelector('Lights', '*', 'Watts per Zone Floor Area'),
                    value_descriptor=CategoryParameter([1,2,3,4,5,6,7,8,9,10]),
                    name='Lights Watts/Area', mode='Add')]
    objectives = ['Electricity:Facility']
    problem = EPProblem(parameters, objectives)
    evaluator = EvaluatorEP(problem, building, multi = False)

    parameter2 = Parameter(FieldSelector('Lights', '*', 'Watts per Zone Floor Area'),
                    value_descriptor=RangeParameter(.5,2),
                    name='Lights Watts/Area', mode='Multiply')
    parameters2 = [parameter2]
    objectives2 = ['Electricity:Facility']
    problem2 = EPProblem(parameters2, objectives2)
    evaluator2 = EvaluatorEP(problem2, building, multi = False)

    samples = sampling.dist_sampler(sampling.seeded_sampler, problem, 20)
    samples2 = sampling.dist_sampler(sampling.seeded_sampler, problem2, 20)

    outputs = evaluator.df_apply(samples, keep_input = True, processes = 4)
    outputs2 = evaluator2.df_apply(samples2, keep_input = True, processes = 4)

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    print()
    print()
    print(outputs)
    print(problem.names('inputs'))
    print(problem.inputs[0].mode)
    print(type(problem.inputs))
    print()
    print()
    print(outputs2)
    #change this to 0 to see stdout and stderr
    assert 1
