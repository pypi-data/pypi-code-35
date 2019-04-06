from .integrate import generate_ode_data
from .not_so_simple_ode import *
from .simple_ode import *
from .simple_ode import all_loaders as simple_ode_loaders

all_loaders = {**simple_ode_loaders}
