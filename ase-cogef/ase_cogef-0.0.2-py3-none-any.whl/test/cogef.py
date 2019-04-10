# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Tests for ase/cogef.py and ase/dissociation.py.

"""
from os import remove

from ase import Atoms
from ase.optimize import FIRE
from ase.units import m, J
from ase.calculators.emt import EMT

from cogef import COGEF, Dissociation


# Class COGEF
fmax = 0.05

atom1 = 0
atom2 = 1
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
        return 'cogef' + str(imagenum) + '.traj'
    image.set_calculator(EMT())

cogef = COGEF(images, atom1, atom2, optimizer=FIRE, fmax=fmax)
cogef.pull(stepsize, steps, initialize, 'cogef.traj')

# Pull further
cogef = COGEF('cogef.traj', atom1, atom2, optimizer=FIRE, fmax=fmax)
cogef.pull(stepsize, steps, initialize, 'cogef.traj')
force1 = cogef.get_maximum_force()

# Reload the value
cogef = COGEF('cogef.traj', atom1, atom2)
force2 = cogef.get_maximum_force()

assert force1 == force2

print('Maximum force (electronic part):')
print(str(cogef.get_maximum_force(method='use_energies') * m / J * 1e9) +
      'nN')
print(str(cogef.get_maximum_force(method='use_forces') * m / J * 1e9) + 'nN')


# Class Dissociation
T = 298
P = 101325.
loading_rate = 10.
force_ext = 6.5
force_min = 6.5
force_max = 7.
force_step = 0.02


def initialize_diss(image, dirname):
    """initialize the image"""
    image.set_calculator(EMT())

diss = Dissociation(cogef, initialize_diss, vib_method='frederiksen',
                    force_unit='nN')

pmax, pmin = diss.electronic_extreme_values(force_ext)
energies = diss.modified_energies(force_ext)
assert pmax[1] == energies[pmax[0]]
assert pmin[1] == energies[pmin[0]]
# Really a local maximum?
assert pmax[1] >= energies[pmax[0] + 1]
assert pmax[1] >= energies[pmax[0] - 1]
# Really a local minimum?
assert pmin[1] <= energies[pmin[0] + 1]
assert pmin[1] <= energies[pmin[0] - 1]

# in eV/Angstrom
diss.set_force_unit('eV/A')
f_ext = force_ext / (m / J * 1e9)
rate1 = diss.get_rate(f_ext, T, P, method='electronic', verbose=False)

# in nN
diss.set_force_unit('nN')
f_ext = force_ext
rate2 = diss.get_rate(f_ext, T, P, method='electronic', verbose=False)
assert rate1 == rate2
print('Rate for f_ext=' + str(f_ext) + 'nN:')
print(str(rate1) + '/s')

f_rup, f_err = diss.rupture_force_and_uncertainty(T, P, loading_rate,
                                                  force_max, force_min,
                                                  force_step)
print('Rupture force:')
print(str(f_rup) + 'nN')
print('Uncertainty:')
print(str(f_err) + 'nN')

# Search limits automatically
factor = 10
force_min, force_max = diss.get_force_limits(T, P, loading_rate,
                                             force_step=force_step,
                                             method='Gibbs',
                                             factor=factor)
dpdf, forces = diss.probability_density(T, P, loading_rate, force_max,
                                        force_min, force_step, method='Gibbs')
assert dpdf[0] < max(dpdf) / factor
assert dpdf[-1] < max(dpdf) / factor
f_rup2 = diss.rupture_force(T, P, loading_rate, force_max, force_min,
                            force_step, method='Gibbs')
assert round(f_rup, 1) == round(f_rup2, 1)

# Remove the files
for i in range(1, 2 * steps + 1):
    remove('cogef' + str(i) + '.traj')
remove('cogef.traj')
