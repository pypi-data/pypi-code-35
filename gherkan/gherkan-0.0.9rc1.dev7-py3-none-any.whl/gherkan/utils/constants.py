import os

PROJECT_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir)
DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "data")

AND = "AND"
OR = "OR"
NOT = "NOT"
EQUALITY = "EQUALITY"
INEQUALITY = "INEQUALITY"
BOOL = "BOOL"
EDGE = "EDGE"
FORCE = "FORCE"
UNFORCE = "UNFORCE"

LBRACKET = "LBRACKET"
RBRACKET = "RBRACKET"
SKIP = "SKIP"
MISMATCH =  "MISMATCH"

LANG_CZ = "cs"
LANG_EN = "en"