from os.path import join, expanduser, isdir
from os import makedirs

MODELS_PATH = join(expanduser("~"), "text_classifikation","models")
DATA_PATH = join(expanduser("~"), "text_classifikation", "data")

if not isdir(MODELS_PATH):
    makedirs(MODELS_PATH)

if not isdir(DATA_PATH):
    makedirs(DATA_PATH)

