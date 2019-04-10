# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Tests for cogef/cogef2d.py.

"""

import shutil
from os import mkdir, remove
from os.path import join, isdir

from ase import Atoms
from ase.optimize import FIRE
from ase.parallel import rank
from ase.calculators.emt import EMT

from cogef import COGEF2D

# Class COGEF2D
fmax = 0.05

pull_atoms = [0, 1]
break_atoms = [0, 2]
steps = 10
stepsize = 0.25

image = Atoms('H3', positions=[(0, 0, 0), (0.751, 0, 0), (0, 1., 0)])
image.set_calculator(EMT())
opt = FIRE(image)
opt.run(fmax=fmax)

images = [image]


def initialize(image, imagenum, new_opt, get_filename):
    """Initialize the image and return the trajectory name.

    """
    if get_filename:
        return join('pull', 'cogef' + str(imagenum) + '.traj')
    image.set_calculator(EMT())


def initialize2d(image, directory, imagenum, new_opt, get_filename):
    """Initialize the image or return the trajectory name.

    """
    molout_pull = join(directory, 'cogef')
    if initialize(image, -1, new_opt, get_filename) == 'Finished':
        return 'Finished'
    if get_filename:
        return molout_pull + str(imagenum) + '.traj'


if (rank == 0) and not(isdir('pull')):
    mkdir('pull')
cogef = COGEF2D(pull_atoms, break_atoms, images, optimizer=FIRE, fmax=fmax)
cogef.pull(stepsize, steps, initialize, 'cogef.traj')

# Searching-minimum-tests

# Test 1
energy_tolerance = 0.5
i = 10
cogef.last_intact_bond_image = 20
is_maximum = False
found_min = True
engs = [1, None, None, 4]
engs2, emax, emin = cogef.check_energies(
    engs, energy_tolerance, i, is_maximum, found_min)
assert [engs2, emin] == [engs[-1:], None]

# Test 2
engs = [1]
try:
    engs2, emax, emin = cogef.check_energies(
        engs, energy_tolerance, i, is_maximum, found_min)
except ValueError:
    pass  # Energy tolerance is too small
else:
    raise RuntimeError('Missing error message.')

# Test 3
i = 30
engs = [1]
engs2, emax, emin = cogef.check_energies(
    engs, energy_tolerance, i, is_maximum, found_min)
assert [engs2, emin] == [engs, None]

# Test 4
i = 10
found_min = False
engs = [1, 2, 3, 2.9, 4, 5]
try:
    engs2, emax, emin = cogef.check_energies(
        engs, energy_tolerance, i, is_maximum, found_min)
except ValueError:
    pass  # Energy tolerance is too small
else:
    raise RuntimeError('Missing error message.')

# Test 5
engs = [1, None, None, 3, 2.9, 4, 5]
try:
    engs2, emax, emin = cogef.check_energies(
        engs, energy_tolerance, i, is_maximum, found_min)
except ValueError:
    pass  # Energy tolerance is too small
else:
    raise RuntimeError('Missing error message.')

# Test 6
found_min = True
engs = [1, None, None, 4, 5]
engs2, emax, emin = cogef.check_energies(
    engs, energy_tolerance, i, is_maximum, found_min)
assert [engs2, emin] == [engs[-1:], None]

# Test 7
found_min = False
engs = [1, 2, 3, 4, 5]
try:
    engs2, emax, emin = cogef.check_energies(
        engs, energy_tolerance, i, is_maximum, found_min)
except RuntimeError:
    pass  # Maximum must be obtained first
else:
    raise RuntimeError('Missing error message.')

# Test 8
found_min = True
engs = [1, 2, 3, 2.9, 4, 5]
engs2, emax, emin = cogef.check_energies(
    engs, energy_tolerance, i, is_maximum, found_min)
assert [engs2, emin] == [engs[-1:], None]

# Remove the files
shutil.rmtree('pull')
remove('cogef.traj')
