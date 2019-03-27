"""Generate a Tk from upon a Gui schema.

A GUI schema is a JSON-Schema dictionnary,
with tags require and existifs added to declare explicit cyclic depenencies
"""
from tkinter import Tk
from opentea.gui_tree.root_tree import OTRoot


def main_otinker(schema):
    """Startup the gui generation.

    Inputs :
    --------
    schema : dictionary compatible with json-schema

    Outputs :
    ---------
    a tkinter GUI
    """
    tksession = Tk()

    OTRoot(schema, tksession)
