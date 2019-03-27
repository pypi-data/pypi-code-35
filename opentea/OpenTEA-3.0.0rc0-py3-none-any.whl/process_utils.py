"""Utilities for opentea additionnal porcessing in tabs"""
import sys
import yaml


def template_aditional_process(nob_in):
    """Template of an additionnal process.

    Parameter :
    -----------
    nob_in : nested object containing the initial data

    Output :
    -----------
    nob_out : a nested object containing the altered data
    """
    nob_out = nob_in.copy()

    # Your actions here to change the content of nob_out
    # nob_out["foobar"] = 2 * nob_in["foobar"]
    # (...)

    return nob_out


def process_tab(func_to_call):
    """Execute the function of an external process.external.

    func_to_call : see above for a typical function 
    to be called by openTea GUIS
    """
    with open(sys.argv[1], "r") as fin:
        data = yaml.load(fin)
    data_out = func_to_call(data)
    with open("dataset_to_gui.yml", "w") as fout:
        yaml.dump(data_out, fout, default_flow_style=False)
