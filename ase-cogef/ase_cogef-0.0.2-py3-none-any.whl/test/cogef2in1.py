# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Tests for cogef/cogef2in1.py.

"""

import shutil
from os import remove
from os.path import join

from ase.build import molecule
from ase.optimize import FIRE
from ase.calculators.emt import EMT

from cogef import COGEF2IN1

# Class COGEF2IN1
fmax = 0.05

pull_atoms = [9, 6]
break_atoms = [2, 3]
break_distance = 2.5
steps = 10
stepsize = 0.25

image = molecule('cyclobutene')
image.set_calculator(EMT())
opt = FIRE(image)
opt.run(fmax=fmax)

images = [image]


def initialize(image, curve_type, imagenum, new_opt, get_filename):
    """Initialize the image and return the trajectory name.

    """
    if curve_type == 'reactant':
        dir_pull = 'pull'
    elif curve_type == 'transition':
        dir_pull = 'pull_max'
    else:
        assert curve_type == 'product'
        dir_pull = 'pull_min'
    if get_filename:
        return join(dir_pull, 'cogef' + str(imagenum) + '.traj')
    image.set_calculator(EMT())


cogef = COGEF2IN1(pull_atoms, break_atoms, break_distance, images,
                  optimizer=FIRE, fmax=fmax)
cogef.calc_all(stepsize, initialize,
               reactant_trajectory='pull/cogef.traj',
               transition_trajectory1='pull_max/cogef.traj',
               transition_trajectory2='breakmax.traj',
               product_trajectory1='pull_min/cogef.traj',
               product_trajectory2='breakmin.traj')

# Remove the files
shutil.rmtree('pull')
shutil.rmtree('pull_max')
shutil.rmtree('pull_min')
remove('breakmax.traj')
remove('breakmin.traj')
