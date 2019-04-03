import os
import pathlib
import json

_ENDPOINTS_V3_FILE_PATH = pathlib.Path(os.path.dirname(__file__) + "/endpoints_v3.json")
with open(_ENDPOINTS_V3_FILE_PATH, "r") as fp:
    v3 = json.load(fp)

_ENDPOINTS_V4_FILE_PATH = pathlib.Path(os.path.dirname(__file__) + "/endpoints_v4.json")
with open(_ENDPOINTS_V4_FILE_PATH, "r") as fp:
    v4 = json.load(fp)