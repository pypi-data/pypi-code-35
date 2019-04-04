from .lib.learners import *
from .lib.table_processing import *
from .lib.scores import *
from .lib.clustering import *


def cforange_multiple_cross_validation(input_dict):
    import orange, orngTest, orngStat
    learners = input_dict['learners']
    data = input_dict['dataset']
    folds = int(input_dict['folds'])
    results = orngTest.crossValidation(learners, data, folds=folds)
    output_dict = {}
    output_dict['results']=results
    return output_dict

def cforange_proportion_test(input_dict):
    import orange, orngTest, orngStat
    learners = input_dict['learners']
    data = input_dict['dataset']
    learnProp = float(input_dict['learnProp'])
    times = int(input_dict['times'])
    results = orngTest.proportionTest(learners, data, learnProp, times=times)
    output_dict = {}
    output_dict['results']=results
    return output_dict  

def cforange_leave_one_out(input_dict):
    import orange, orngTest, orngStat
    learners = input_dict['learners']
    data = input_dict['dataset']
    results = orngTest.leaveOneOut(learners, data)
    output_dict = {}
    output_dict['results']=results
    return output_dict       

def cforange_cross_validation(input_dict):
    import orange, orngTest, orngStat
    learners = [input_dict['learner']]
    data = input_dict['dataset']
    folds = int(input_dict['folds'])
    results = orngTest.crossValidation(learners, data, folds=folds)
    output_dict = {}
    output_dict['results']=results
    return output_dict

