from .__version__ import __version__
from .maps import all_maps
from .ode import all_ode

all_problems = {}
for typ, dct in zip(["map", "ode"], [all_maps, all_ode]):
    for k, v in dct.items():
        all_problems[k] = v
        all_problems[k]["type"] = typ

del all_maps
del all_ode
