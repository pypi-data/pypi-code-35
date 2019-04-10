# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Module for calculating vibrational frequencies when the molecule is
stetched by a spring. Spring forces which acts on two atoms influence the
vibrational modes.

"""

import pickle
from math import sqrt
import numpy as np

from ase.vibrations import Vibrations
from ase.vibrations.infrared import Infrared
import ase.units as units


class SpringVib(Vibrations):
    """Class like Vibrations for a system influenced by an external
    spring force.

    One side of the configuration is fixed and the other side is connected to
    a spring which is fixed on the other side.

    Parameters
    ----------
    atoms: Atoms object
        The atoms to work on.
    indices: list of int
        List of indices of atoms to vibrate.  Default behavior is
        to vibrate all atoms.
    name: str
        Name to use for files.
    delta: float
        Magnitude of displacements.
    nfree: int
        Number of displacements per atom and cartesian coordinate, 2 and 4 are
        supported. Default is 2 which will displace each atom +delta and
        -delta for each cartesian coordinate.
    spring_constant: float
        Spring constant with unit eV/A^2.
    atom1: int
        Index of first atom where forces acts on.
    atom2: int
        Index of second atom where forces acts on.
    spring_on_atom1: bool
        Define the connection point of the spring.
        *True*: atom1, *False*: atom2.
    spring_direction: numpy array of three floats (optional)
        Define spring direction, otherwise it is obtained from atom positions.

    """
    def __init__(self, atoms, indices=None, name='vib', delta=0.01, nfree=2,
                 spring_constant=0., atom1=None, atom2=None,
                 spring_on_atom1=True, spring_direction=None):
        Vibrations.__init__(self, atoms, indices, name, delta, nfree)
        self.spring_constant = spring_constant
        assert atom1 != atom2
        self.atom1 = atom1
        self.atom2 = atom2
        self.spring_on_atom1 = spring_on_atom1
        self.spring_direction = spring_direction

    def read(self, method='standard', direction='central'):
        # TODO: The following code should be optimized
        Vibrations.read(self, method, direction)
        if self.spring_direction is None:
            dist = self.atoms[self.atom2].position - \
                self.atoms[self.atom1].position
        else:
            dist = self.spring_direction
        if self.spring_on_atom1:
            atom = self.atom1
        else:
            atom = self.atom2
        for i in range(3):
            for j in range(3):
                self.H[3 * atom + i, 3 * atom + j] += \
                    self.spring_constant * dist[i] * dist[j] / dist.dot(dist)
        m = self.atoms.get_masses()
        self.im = np.repeat(m[self.indices]**-0.5, 3)
        omega2, modes = np.linalg.eigh(self.im[:, None] * self.H * self.im)
        self.modes = modes.T.copy()
        # Conversion factor:
        s = units._hbar * 1e10 / sqrt(units._e * units._amu)
        self.hnu = s * omega2.astype(complex)**0.5


class SpringInf(Infrared):
    """Class like Infrared for a system influenced by an external
    spring force.

    One side of the configuration is fixed and the other side is connected to
    a spring which is fixed on the other side.

    Parameters
    ----------
    atoms: Atoms object
        The atoms to work on.
    indices: list of int
        List of indices of atoms to vibrate.  Default behavior is
        to vibrate all atoms.
    name: str
        Name to use for files.
    delta: float
        Magnitude of displacements.
    nfree: int
        Number of displacements per degree of freedom, 2 or 4 are
        supported. Default is 2 which will displace each atom +delta
        and -delta in each cartesian direction.
    directions: list of int
        Cartesian coordinates to calculate the gradient
        of the dipole moment in.
        For example directions = 2 only dipole moment in the z-direction will
        be considered, whereas for directions = [0, 1] only the dipole
        moment in the xy-plane will be considered. Default behavior is to
        use the dipole moment in all directions.
    spring_constant: float
        Spring constant with unit eV/A^2.
    atom1: int
        Index of first atom where forces acts on.
    atom2: int
        Index of second atom where forces acts on.
    spring_on_atom1: bool
        Define the connection point of the spring.
        *True*: atom1, *False*: atom2.
    spring_direction: numpy array of three floats (optional)
        Define spring direction, otherwise it is obtained from atom positions.

    """
    def __init__(self, atoms, indices=None, name='ir', delta=0.01,
                 nfree=2, directions=None, spring_constant=0., atom1=None,
                 atom2=None, spring_on_atom1=True, spring_direction=None):
        Infrared.__init__(self, atoms, indices, name, delta, nfree,
                          directions)
        self.spring_constant = spring_constant
        assert atom1 != atom2
        self.atom1 = atom1
        self.atom2 = atom2
        self.spring_on_atom1 = spring_on_atom1
        self.spring_direction = spring_direction

    def read(self, method='standard', direction='central'):
        self.method = method.lower()
        self.direction = direction.lower()
        assert self.method in ['standard', 'frederiksen']

        def load(fname, combined_data=None):
            if combined_data is not None:
                return combined_data[fname]
            return pickleload(open(fname, 'rb'))

        if direction != 'central':
            raise NotImplementedError(
                'Only central difference is implemented at the moment.')

        if op.isfile(self.name + '.all.pckl'):
            # Open the combined pickle-file
            combined_data = load(self.name + '.all.pckl')
        else:
            combined_data = None
        # Get "static" dipole moment and forces
        name = '%s.eq.pckl' % self.name
        [forces_zero, dipole_zero] = load(name, combined_data)
        self.dipole_zero = (sum(dipole_zero**2)**0.5) / units.Debye
        self.force_zero = max([sum((forces_zero[j])**2)**0.5
                               for j in self.indices])

        ndof = 3 * len(self.indices)
        H = np.empty((ndof, ndof))
        dpdx = np.empty((ndof, 3))
        r = 0
        for a in self.indices:
            for i in 'xyz':
                name = '%s.%d%s' % (self.name, a, i)
                [fminus, dminus] = load(name + '-.pckl', combined_data)
                [fplus, dplus] = load(name + '+.pckl', combined_data)
                if self.nfree == 4:
                    [fminusminus, dminusminus] = load(
                        name + '--.pckl', combined_data)
                    [fplusplus, dplusplus] = load(
                        name + '++.pckl', combined_data)
                if self.method == 'frederiksen':
                    fminus[a] += -fminus.sum(0)
                    fplus[a] += -fplus.sum(0)
                    if self.nfree == 4:
                        fminusminus[a] += -fminus.sum(0)
                        fplusplus[a] += -fplus.sum(0)
                if self.nfree == 2:
                    H[r] = (fminus - fplus)[self.indices].ravel() / 2.0
                    dpdx[r] = (dminus - dplus)
                if self.nfree == 4:
                    H[r] = (-fminusminus + 8 * fminus - 8 * fplus +
                            fplusplus)[self.indices].ravel() / 12.0
                    dpdx[r] = (-dplusplus + 8 * dplus - 8 * dminus +
                               dminusminus) / 6.0
                H[r] /= 2 * self.delta
                dpdx[r] /= 2 * self.delta
                for n in range(3):
                    if n not in self.directions:
                        dpdx[r][n] = 0
                        dpdx[r][n] = 0
                r += 1
        H += H.copy().T
        if self.spring_direction is None:
            dist = self.atoms[self.atom2].position - \
                self.atoms[self.atom1].position
        else:
            dist = self.spring_direction
        if self.spring_on_atom1:
            atom = self.atom1
        else:
            atom = self.atom2
        for i in range(3):
            for j in range(3):
                H[3 * atom + i, 3 * atom + j] += \
                    self.spring_constant * dist[i] * dist[j] / dist.dot(dist)
        self.H = H
        # Calculate eigenfrequencies and eigenvectors
        m = self.atoms.get_masses()
        self.im = np.repeat(m[self.indices]**-0.5, 3)
        omega2, modes = np.linalg.eigh(self.im[:, None] * H * self.im)
        self.modes = modes.T.copy()

        # Calculate intensities
        dpdq = np.array([dpdx[j] / sqrt(m[self.indices[j // 3]] *
                                        units._amu / units._me)
                         for j in range(ndof)])
        dpdQ = np.dot(dpdq.T, modes)
        dpdQ = dpdQ.T
        intensities = np.array([sum(dpdQ[j]**2) for j in range(ndof)])
        # Conversion factor:
        s = units._hbar * 1e10 / sqrt(units._e * units._amu)
        self.hnu = s * omega2.astype(complex)**0.5
        # Conversion factor from atomic units to (D/Angstrom)^2/amu.
        conv = (1.0 / units.Debye)**2 * units._amu / units._me
        self.intensities = intensities * conv
