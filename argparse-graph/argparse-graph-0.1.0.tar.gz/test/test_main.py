import pytest
import os, sys
from argparse import Namespace

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from argparseGraph.argparseGraph import argparseGraph as agg

# argparse object
argparse_obj_1 = Namespace(**dict({'argv1': 1, 'argv2': [1, 2], 'argv3': 'test3', 'argv4': False, 'argv5': 'ok', 'argv6': True, 'argv7': ['Hello', 'World']}))
argparse_obj_2 = Namespace(**dict({'argv1': 1, 'argv2': [1, 2], 'argv3': 'test3', 'argv4': False, 'argv5': None, 'argv6': None, 'argv7': None}))
argparse_obj_3 = Namespace(**dict({'argv1': None, 'argv2': None, 'argv3': 'test3', 'argv4': 'True', 'argv5': None, 'argv6': True, 'argv7': ['Test']}))
argparse_obj_4 = Namespace(**dict({'argv1': None, 'argv2': None, 'argv3': 'test3', 'argv4': False, 'argv5': None, 'argv6': None, 'argv7': None}))

def test_all_str():
    """
    option: "all"
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples.yml", argparse_obj_1)
    assert res.get_one() == 'senario_1'

def test_all_int():
    """
    option: "all"
    return get_one: 1
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_digit.yml", argparse_obj_1)
    assert res.get_one() == 1

def test_all_args():
    """
    option: "all"
    return get_one: senario_1
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_args.yml", argparse_obj_1)
    assert res.get_one() == "senario_1"

def test_all_list():
    """
    option:
    - argv1
    - argv2
    - argv3
    - argv4
    - argv5
    - argv6
    - argv7
    return get_one: "senario_1"
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_list.yml", argparse_obj_1)
    assert res.get_one() == "senario_1"

def test_two_args_str():
    """
    option:  argv3, argv4
    return get_one: senario_2
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples.yml", argparse_obj_4)
    assert res.get_one() == "senario_2"

def test_two_args_int():
    """
    option:  argv3, argv4
    return get_one: 2
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_digit.yml", argparse_obj_4)
    assert res.get_one() == 2

def test_two_args_args():
    """
    option:  argv3, argv4
    return get_one: 2
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_args.yml", argparse_obj_4)
    assert res.get_one() == "senario_2"

def test_two_args_list():
    """
    option:
        - argv3
        - argv4
    return get_one: 2
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_list.yml", argparse_obj_4)
    assert res.get_one() == "senario_2"

def test_args_str():
    """
    option:  argv1, argv2, argv3, argv4
    return get_one: senario_2
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples.yml", argparse_obj_2)
    assert res.get_one() == "senario_3"

def test_args_int():
    """
    option:  argv1, argv2, argv3, argv4
    return get_one: 3
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_digit.yml", argparse_obj_2)
    assert res.get_one() == 3

def test_args_args():
    """
    option: argv1, argv2, argv3, argv4
    return get_one: senario_3
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_args.yml", argparse_obj_2)
    assert res.get_one() == "senario_3"

def test_args_list():
    """
    options:
        - argv1
        - argv2
        - argv3
        - argv4
    return get_one: senario_3
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_list.yml", argparse_obj_2)
    assert res.get_one() == "senario_3"

def test_args_str():
    """
    option:  argv3, argv4, argv6, argv7
    return get_one: senario_4
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples.yml", argparse_obj_3)
    assert res.get_one() == "senario_4"

def test_args_int():
    """
    option:  argv3, argv4, argv6, argv7
    return get_one: 4
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_digit.yml", argparse_obj_3)
    assert res.get_one() == 4

def test_args_args():
    """
    option: [argv3, argv4, argv6, argv7]
    return get_one: senario_4
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_args.yml", argparse_obj_3)
    assert res.get_one() == "senario_4"

def test_args_list():
    """
    options:
        - argv3
        - argv4
        - argv6
        - argv7
    return get_one: senario_4
    """
    res = agg(CURRENT_DIR + "/yaml/senarios_examples_list.yml", argparse_obj_3)
    assert res.get_one() == "senario_4"

def test_bad_file():
    """
    Fail bad file
    """
    with pytest.raises(OSError) as e:
        res = agg(CURRENT_DIR + "/bad/path.yml", argparse_obj_1)
    assert e.typename == 'OSError'
