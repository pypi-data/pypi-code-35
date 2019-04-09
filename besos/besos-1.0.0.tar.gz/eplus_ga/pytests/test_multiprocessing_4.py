import pytest

import eppy_funcs as ef
from evaluator import EvaluatorEP, EvaluatorSR
from parameters import RangeParameter, CategoryParameter, Parameter, FieldSelector
from problem import EPProblem, Problem
import sampling


@pytest.fixture
def building():
    return ef.get_building()


@pytest.fixture
def parameters():
    parameters = [
        Parameter(FieldSelector(object_name='NonRes Fixed Assembly Window',
                field_name='Solar Heat Gain Coefficient'),
                value_descriptor=RangeParameter(0.01,0.99)),
        Parameter(FieldSelector('Lights', '*', 'Watts per Zone Floor Area'),
                value_descriptor=RangeParameter(8, 12),
                name='Lights Watts/Area')]
    return parameters


@pytest.fixture
def problem(parameters):
    objectives = ['Electricity:Facility']
    problem = EPProblem(parameters, objectives)
    return problem


def test_eval(building, problem):
    evaluator = EvaluatorEP(problem, building, multi = True)
    samples = sampling.dist_sampler(sampling.seeded_sampler, problem, 100)

    evaluator.estimate_time(samples)
    outputs = evaluator.df_apply(samples, keep_input = True, processes = 4)
    print()
    print(outputs)
    evaluator.estimate_time(samples)
    assert 1
