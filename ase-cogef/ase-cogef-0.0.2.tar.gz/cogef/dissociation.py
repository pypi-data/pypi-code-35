# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Module for calculating rupture forces based on the dissociation
rates.

"""

import os
import sys
from copy import deepcopy
from numpy import exp, arange, log, array

from ase.vibrations import Vibrations
from ase.vibrations.infrared import Infrared
from ase.thermochemistry import IdealGasThermo
from ase.parallel import world, rank
from ase.units import J, m, kB, _hplanck, _e

from cogef import rupture_force_from_dpdf
from cogef import rupture_force_and_uncertainty_from_dpdf
from cogef import SpringVib, SpringInf


# eV / (nN * A)
force_factor = m / J * 1e9


def do_nothing_vib(image, dirname):
    """Explanation of the initialization function needed for the vibrational
    analysis in class *Dissociation*.

    This function can be used to set a cell and a calculator.

    Parameters
    ----------
    image: Atoms object
        Configuration used.
    dirname: str
        Path of the directory where output files of the vibrational analysis
        will be saved.

    """
    pass


class Dissociation(object):
    """Class for calculating energy barriers, dissociation rates
    and the resulting rupture force at a given temperature and pressure.

    Parameters
    ----------
    cogef: COGEF object
        The cogef path.
    initialize: function
        Initialization function which is executed before each vibrational
        analysis. See function *do_nothing_vib*.
    dirname: str
        The general directory name for files of the
        vibrational analysis. Image indices will be added automatically.
    imagemin: int
        Image number of first image used from the cogef path.
    imagemax: int
        Image number of last image used from the cogef path.
        Negative values can be used to count from the other direction.
    modulo: int
        Set it to a larger value that less images are used from the cogef
        path, e.g. *modulo=2* means that every second image is used.
        This can be used for numerical tests.
    gibbs_method: str
        The method used to obtain extrema in the Gibbs energy surface.
    vib_method: str
        The method used to obtain vibrational frequencies, see class
        *Vibrations*.
    vib_indices: list of int
        List of indices of atoms to vibrate. Default behavior is
        to vibrate all atoms.
    vib_delta: float
        Magnitude of displacements for vibrational analysis.
    vib_nfree: int
        Number of displacements per atom and cartesian coordinate, 2 and 4 are
        supported. Default is 2 which will displace each atom +delta and
        -delta for each cartesian coordinate.
    vib_class: str
        The name of the class used. Possible classes are
        *Vibrations* and *Infrared*.
    geometry: 'linear', or 'nonlinear'
        Geometry of the molecule used for the calculation of Gibbs energies,
        see class *IdealGasThermo*.
    symmetrynumber: int
        Symmetry number of the molecule. See, for example, Table 10.1 and
        Appendix B of C. Cramer "Essentials of Computational Chemistry",
        2nd Ed.
    spin: float
        The total electronic spin. (0 for molecules in which all electrons
        are paired, 0.5 for a free radical with a single unpaired electron,
        1.0 for a triplet with two unpaired electrons, such as O_2.)
    force_unit: str
        If it is set to 'nN' than every force value which is set or
        returned in one of the following methods is in nN and the loading
        rate has unit nN/s. The loading rate has unit eV/(A*s) if it
        is set to 'eV/A', where A stands for Angstrom.
    allow_max_at_upper_limit: bool
        By default an error message will arise in method
        *electronic_extreme_values* if the energy maximum associated to the
        energy barrier lies at the end of the
        considered image interval because it indicates that the real maximum
        lies outside the interval. If you are sure that the maximum of the
        energy barrier lies within or at the end of the interval, you can use
        *allow_max_at_upper_limit=True* to suppress this error message.
    spring_on_atom1: bool
        Defines the connection point of the spring if there is a spring.
        *True*: self.cogef.atom1, *False*: self.cogef.atom2.
    average_rate: bool
        When spring constant is not zero and *average_rate* is
        *True*, the rate constants are obtained as average over both spring
        positions (atom1/atom2). If it is *False*, the connection is defined
        by *spring_on_atom1*.

    """
    def __init__(self, cogef, initialize=None, dirname='image',
                 imagemin=0, imagemax=-1, modulo=1, gibbs_method='canonical',
                 vib_method='standard', vib_indices=None, vib_delta=0.01,
                 vib_nfree=2, vib_class='Vibrations', geometry='nonlinear',
                 symmetrynumber=1, spin=0, force_unit='eV/A',
                 allow_max_at_upper_limit=False,
                 spring_on_atom1=True, average_rate=True):
        assert force_unit in ['eV/A', 'nN']
        assert vib_class in ['Vibrations', 'Infrared']
        self.cogef = cogef
        self.initialize = initialize
        self.dirname = dirname
        self.imagemin = imagemin
        self.imagemax = imagemax
        self.modulo = modulo
        self.gibbs_method = gibbs_method
        self.vib_method = vib_method
        self.vib_indices = vib_indices
        self.vib_delta = vib_delta
        self.vib_nfree = vib_nfree
        self.vib_class = vib_class
        assert geometry in ['nonlinear', 'linear']
        self.geometry = geometry
        self.symmetrynumber = symmetrynumber
        self.spin = spin
        self.force_unit = force_unit
        self.spring_constant = 0.
        self.spring_ref = 0.
        self.spring_on_atom1 = spring_on_atom1
        self.average_rate = average_rate
        self.allow_max_at_upper_limit = allow_max_at_upper_limit
        self.energy_tolerance = 0
        self.error = None

    def set_energy_tolerance(self, energy_tolerance):
        """Use *energy_tolerance* to allow jumps over small energy barriers
        with *'dE' < energy_tolerance* during the search for the energy
        minimum.

        Parameters
        ----------
        energy_tolerance: float

        """
        self.energy_tolerance = energy_tolerance

    def set_force_unit(self, force_unit='eV/A'):
        """Change the unit of forces and loading rates.

        Parameters
        ----------
        force_unit: str
            If it is set to 'nN' than every force value which is set or
            returned in one of the following methods is in nN and the loading
            rate has unit nN/s. The loading rate has unit eV/(A*s) if
            it is set to 'eV/A', where A stands for Angstrom.

        """
        self.force_unit = force_unit

    def set_spring_constant(self, spring_constant, T, force_min=0.,
                            spring_ref=None):
        """Set the spring constant of the cantilever which stretches the
        molecule.

        The unit of the spring constant is eV/A^2 if *self.force_unit* is
        'eV/A' or nN/A if *self.force_unit* is 'nN'.

        Parameters
        ----------
        spring_constant: float
            The new spring constant.
        T: float
            Temperature.
        force_min: float
            Initial external force.
        spring_ref: float (optional)
            Define the reference value for the calculation of the elongation
            if it should not be the initial stretching distance. This can be
            used for transitions starting from instable intermediate states.

        Returns
        -------
        result: float
            The initial stretching distance of the molecule in equilibrium
            associated to the initial external force and temperature.
            This value can be used as a reference value.

        """
        if spring_ref is None:
            self.spring_constant = 0.
            self.spring_ref = self.get_mean_distance(force_min, T)
        else:
            self.spring_ref = spring_ref
        if self.force_unit == 'nN':
            self.spring_constant = spring_constant / force_factor
        else:
            self.spring_constant = spring_constant
        return self.spring_ref

    def modified_energies(self, f_ext, shift=True,
                          only_intact_bond_images=False):
        """Add the influence of a constant external force (and a spring)
        on the electronic energy along the cogef path.

        Parameters
        ----------
        f_ext: float
            External force.
        shift: bool
            *True* means that the energies are shifted such that the global
            energy minimum gets zero.
        only_intact_bond_images: bool
            *True* means that the given number of the last intact bond image
            defines the upper limit of used images.

        Returns
        -------
        result: list of floats
            Force-tilted energies in the order of the image numbers.

        """
        if self.force_unit == 'nN':
            f_ext /= force_factor
        energies, distances = self.cogef.get_energy_curve(
            self.imagemin, self.imagemax, only_intact_bond_images,
            modulo=self.modulo)
        if self.spring_constant == 0.:
            for i in range(len(energies)):
                energies[i] -= f_ext * distances[i]
        else:
            for i in range(len(energies)):
                delta_d = distances[i] - self.spring_ref
                energies[i] += (self.spring_constant * delta_d / 2. -
                                f_ext) * delta_d
        if shift:
            energies -= min(energies)
        return energies

    def electronic_energy_barrier(self, f_ext):
        """Return the electronic activation energy/barrier height.

        Parameters
        ----------
        f_ext: float
            External force.

        Returns
        -------
        result: float

        """
        pmax, pmin = self.electronic_extreme_values(f_ext)
        return pmax[1] - pmin[1]

    def electronic_extreme_values(self, f_ext, shift=True,
                                  only_minimum=False):
        """Return the maximum and minimum defining the electronic energy
        barrier.

        Parameters
        ----------
        f_ext: float
            External force.
        shift: bool
            *True* means that the energies are shifted. The shift depends on
            the limits of the image interval and the external force.
        only_minimum: bool
            Set it to *True* in order to get only the energy minimum.

        Returns
        -------
        result1: tuple of two floats (optional)
            Image number and energy of the energy maximum.
        result2: tuple of two floats
            Image number and energy of the energy minimum.

        """
        self.error = None
        energies = self.modified_energies(f_ext, shift,
                                          only_intact_bond_images=True)
        energies_copy = deepcopy(energies)
        # Find minimum
        min_at_the_end = True
        while min_at_the_end:
            emin = None
            imin = None
            before_barrier = True
            imin_test = None
            for i, energy in enumerate(energies):
                if (emin is None) or (emin >= energy):
                    emin = energy
                    imin = i
                    min_at_the_end = True
                else:
                    min_at_the_end = False
                if (before_barrier) and \
                   (energy > emin + self.energy_tolerance):
                    before_barrier = False
                    imin_test = imin
            if imin_test is None:
                imin_test = imin
            if min_at_the_end:
                if imin == self.cogef.last_intact_bond_image:
                    break
                # Minimum of energy curve must not be placed at the upper
                # limit of the interval. Upper limit of the interval will
                # be reduced.
                energies = energies[:-1]
                if len(energies) <= 1:
                    self.error = 1
                    raise ValueError('Cannot find a local minimum which ' +
                                     'is not placed at the upper limit ' +
                                     'of the interval. f_ext is too ' +
                                     'large or the range of the ' +
                                     'interval is too small.')
        assert imin_test == imin, 'It seems as if the found minimum is ' + \
                                  'behind the barrier but it should be ' + \
                                  'before. To get rid of this error, ' + \
                                  "set 'last_intact_bond_image' of the " + \
                                  'COGEF object if it is known. Or you ' + \
                                  "could increase 'energy_tolerance' " + \
                                  'of this Dissociation object slightly.'
        if only_minimum:
            return (imin * self.modulo, emin)
        # Find maximum
        emax = None
        imax = None
        max_at_the_end = True
        # use *energies_copy* which contains all energies
        for i, energy in enumerate(energies_copy):
            if i <= imin:
                continue
            if (emax is None) or (emax <= energy):
                emax = energy
                imax = i
                max_at_the_end = True
            else:
                max_at_the_end = False
        if (imax is None) and (imin == self.cogef.last_intact_bond_image):
            # Minimum and maximum are merged together
            emax = emin
            imax = imin
        else:
            if (max_at_the_end) and not(self.allow_max_at_upper_limit) and \
               (imax < self.cogef.last_intact_bond_image):
                self.error = 2
                raise ValueError('Local maxima of the energy curve must ' +
                                 'not be placed at the upper limit of the ' +
                                 'interval. f_ext or imagemax is too ' +
                                 'small. It may help to ' +
                                 "set 'last_intact_bond_image' of the " +
                                 'COGEF object if it is known.')
        return (imax * self.modulo, emax), (imin * self.modulo, emin)

    def set_imagemin(self, imagemin=0):
        """Change first image number used from the cogef path.

        Parameters
        ----------
        imagemin: int
            Image number.

        """
        self.imagemin = imagemin

    def set_imagemax(self, imagemax=-1):
        """Change last image number used from the cogef path.

        Parameters
        ----------
        imagemax: int
            Image number.
            Negative values can be used to count from the other direction.

        """
        self.imagemax = imagemax

    def gibbs_energy_barrier(self, f_ext, T, P, verbose=True):
        """Return the Gibbs activation energy/barrier height at given
        temperature and pressure.

        Parameters
        ----------
        f_ext: float
            External force.
        T: float
            Temperature.
        P: float
            Pressure.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        verbose = (verbose) and (rank == 0)
        method = self.gibbs_method
        assert method in ['canonical']
        if method == 'canonical':
            # Canonical Transition-state theory:
            # Use Gibbs energies from the configurations of the
            # electronic maximum (Transition-state structure) and minimum.
            # This is an approximation.
            pmax, pmin = self.electronic_extreme_values(f_ext)
            emax = pmax[1]
            emin = pmin[1]
            imax = pmax[0]
            imin = pmin[0]
            # Gibbs energy at the minimum and maximum
            for is_maximum, i in [(False, imin), (True, imax)]:
                if verbose:
                    if is_maximum:
                        sys.stdout.write('\n' + 'Maximum:')
                    else:
                        sys.stdout.write('\n' + 'Minimum:')
                self.calculate_vibrations(i)
                if is_maximum:
                    potentialenergy = emax
                else:
                    potentialenergy = emin
                gibbs = self.get_gibbs_energy(i, T, P, potentialenergy,
                                              is_maximum, verbose)
                if is_maximum:
                    gibbs_max = gibbs
                else:
                    gibbs_min = gibbs
            return gibbs_max - gibbs_min

    def calculate_vibrations(self, imageindex):
        """Use the class *Vibrations* or *Infrared* to get the files needed
        for the calculation of the Gibbs energy.

        Parameters
        ----------
        imageindex: int
            Image index.

        """
        if self.initialize is None:
            return
        image = self.cogef.images[imageindex].copy()
        image.set_calculator(
            deepcopy(self.cogef.images[imageindex].get_calculator()))
        # No constraints should be set during the calculation of
        # the forces which are needed for the vibrational modes. Even the
        # FixBondLength constraint of the COGEF procedure must be removed.
        image.set_constraint()
        dirname = self.dirname + str(imageindex)
        if (rank == 0) and not(os.path.isdir(dirname)):
            os.mkdir(dirname)
        world.barrier()
        if self.vib_class == 'Vibrations':
            try:
                # Check first whether calculation is finished (no calculator)
                if not(os.path.isfile(os.path.join(dirname, 'vib.eq.pckl'))) \
                   and (os.path.isfile(os.path.join(
                       dirname,
                       'vib-d{:.3f}.eq.pckl'.format(self.vib_delta)))):
                    # Old name
                    vib = Vibrations(image,
                                     name=os.path.join(
                                         dirname,
                                         'vib-d{:.3f}'
                                         .format(self.vib_delta)),
                                     delta=self.vib_delta,
                                     nfree=self.vib_nfree)
                else:
                    vib = Vibrations(image,
                                     name=os.path.join(dirname, 'vib'),
                                     delta=self.vib_delta,
                                     nfree=self.vib_nfree)
                vib.clean(empty_files=True)
                vib.run()
            except RuntimeError:
                # It's not finished: set box and calculator
                self.initialize(image, dirname)
                world.barrier()
                vib = Vibrations(image,
                                 name=os.path.join(dirname, 'vib'),
                                 delta=self.vib_delta,
                                 nfree=self.vib_nfree)
                vib.clean(empty_files=True)
                vib.run()
        elif self.vib_class == 'Infrared':
            try:
                # Check first whether calculation is finished (no calculator)
                if not(os.path.isfile(os.path.join(dirname, 'ir.eq.pckl'))) \
                   and (os.path.isfile(os.path.join(
                       dirname,
                       'ir-d{:.3f}.eq.pckl'.format(self.vib_delta)))):
                    # Old name
                    infra = Infrared(image,
                                     name=os.path.join(
                                         dirname,
                                         'ir-d{:.3f}'.format(self.vib_delta)),
                                     delta=self.vib_delta,
                                     nfree=self.vib_nfree)
                else:
                    infra = Infrared(image,
                                     name=os.path.join(dirname, 'ir'),
                                     delta=self.vib_delta,
                                     nfree=self.vib_nfree)
                infra.clean(empty_files=True)
                infra.run()
            except RuntimeError:
                # It's not finished: set box and calculator
                self.initialize(image, dirname)
                world.barrier()
                infra = Infrared(image,
                                 name=os.path.join(dirname, 'ir'),
                                 delta=self.vib_delta,
                                 nfree=self.vib_nfree)
                infra.clean(empty_files=True)
                infra.run()
        world.barrier()

    def get_gibbs_energy(self, imageindex, T, P, potentialenergy, is_maximum,
                         verbose):
        """Return the Gibbs energy.

        Parameters
        ----------
        imageindex: int
            Image index.
        T: float
            Temperature.
        P: float
            Pressure.
        potentialenergy: float
            Electronic energy.
        is_maximum: bool
            *True* means that the image corresponds to an energy maximum and
            not minimum.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        image = self.cogef.images[imageindex].copy()
        image.set_constraint()
        if self.vib_class == 'Vibrations':
            name = 'vib'
            if self.spring_constant == 0.:
                vib_class = Vibrations
            else:
                vib_class = SpringVib
        elif self.vib_class == 'Infrared':
            name = 'ir'
            if self.spring_constant == 0.:
                vib_class = Infrared
            else:
                vib_class = SpringInf
        dirname = self.dirname + str(imageindex)
        filename = os.path.join(dirname, name)
        if not(os.path.isfile(filename + '.eq.pckl')):
            # Old name
            filename += '-d{:.3f}'.format(self.vib_delta)
        if self.spring_constant == 0.:
            vib = vib_class(image, indices=self.vib_indices,
                            name=filename,
                            delta=self.vib_delta, nfree=self.vib_nfree)
        else:
            vib = vib_class(image, indices=self.vib_indices,
                            name=filename,
                            delta=self.vib_delta, nfree=self.vib_nfree,
                            spring_constant=self.spring_constant,
                            atom1=self.cogef.atom1, atom2=self.cogef.atom2,
                            spring_on_atom1=self.spring_on_atom1)
        if verbose:
            vib.summary(method=self.vib_method)
        vib_energies = vib.get_energies(method=self.vib_method)
        vib_energies = self.vib_energy_correction(
            vib_energies, image, is_maximum, T, P)
        thermo = IdealGasThermo(vib_energies=vib_energies,
                                potentialenergy=potentialenergy,
                                atoms=image,
                                geometry=self.geometry,
                                symmetrynumber=self.symmetrynumber,
                                spin=self.spin)
        return thermo.get_gibbs_energy(T, P, verbose=verbose)

    def vib_energy_correction(self, vib_energies, image, is_maximum, T, P):
        """This method can be used to correct vibrational frequencies.

        Parameters
        ----------
        vib_energies: numpy array of complex
            Vibrational energies.
        image: Atoms object
            The configuration.
        is_maximum: bool
            *True* means that the image corresponds to an energy maximum and
            not minimum.
        T: float
            Temperature.
        P: float
            Pressure.

        Returns
        -------
        result: numpy array of complex
            Corrected vibrational energies.

        """
        if is_maximum:
            # At the Transition-state (Maximum):
            # Do not use the imaginary frequency along the transition path
            natoms = len(image)
            if self.geometry == 'nonlinear':
                vib_energies = vib_energies[-(3 * natoms - 7):]
            elif self.geometry == 'linear':
                vib_energies = vib_energies[-(3 * natoms - 6):]
        return vib_energies

    def get_rate(self, f_ext, T, P, method='Gibbs', verbose=True):
        """Return dissociation rate constant from the Eyring equation
        at given temperature and pressure.

        Parameters
        ----------
        f_ext: float
            External force.
        T: float
            Temperature.
        P: float
            Pressure.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        assert method in ['electronic', 'Gibbs']
        if method == 'electronic':
            barrier = self.electronic_energy_barrier(f_ext)
        if method == 'Gibbs':
            barrier = self.gibbs_energy_barrier(f_ext, T, P, verbose=verbose)
        # h in units eV * s
        h = _hplanck / _e
        prefactor = kB * T / h
        exponent = -barrier / (kB * T)
        rate_constant = prefactor * exp(exponent)
        if (self.spring_constant != 0) and (self.average_rate) \
           and (method == 'Gibbs'):
            # The spring position only has an influence on the vibrational
            # frequencies
            try:
                self.spring_on_atom1 = not(self.spring_on_atom1)
                self.average_rate = False
                rate_constant = (rate_constant +
                                 self.get_rate(f_ext, T, P, method,
                                               verbose)) / 2.
            finally:
                self.spring_on_atom1 = not(self.spring_on_atom1)
                self.average_rate = True
        return rate_constant

    def get_rate_constants(self, T, P, force_max, force_min=0.,
                           force_step=0.01, method='Gibbs', verbose=False):
        """Return dissociation rate constants.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result1: list of floats
            Rate constants.
        result2: list of floats
            External forces.

        """
        rates = []
        forces = []
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            rates.append(self.get_rate(f_ext, T, P, method, verbose))
            forces.append(f_ext)
        return rates, forces

    def save_rate_constants(self, T, P, force_max, force_min=0.,
                            force_step=0.01, method='Gibbs',
                            fileout='rates.dat'):
        """Save dissociation rate constants to a file.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        fileout: str
            Filename.

        """
        rates, forces = self.get_rate_constants(T, P, force_max, force_min,
                                                force_step, method)
        fd = open(fileout, 'w')
        if self.spring_constant == 0.:
            fd.write('Force\t' + 'Rate constant\n')
            space = '\t'
        else:
            fd.write('Loading rate * time\t' + 'Rate constant\n')
            space = '\t\t\t'
        for i in range(len(rates)):
            fd.write(str(round(forces[i], 10)) + space + str(rates[i]) + '\n')
        fd.close()

    def probability_density(self, T, P, loading_rate, force_max,
                            force_min=0., force_step=0.01, method='Gibbs',
                            verbose=False, probability_break_value=0.):
        """Return a list of dp/df-values within a given force interval.

        p is the bond-breaking probability and f is the external force.
        The maximum of the dp/df-values corresponds to the most probable
        rupture force.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval. It is assumed that
            *force_min* is the external force at time 0.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.
        probability_break_value: float
            The calculation is canceled when the probability that the bond is
            not broken drops below this value.

        Returns
        -------
        result1: numpy array of float
            dp/df-values.
        result2: numpy array of float
            External forces.

        """
        integration = 0.
        dpdf = []
        forces = []
        start = True
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            last_rate = self.get_rate(f_ext, T, P, method, verbose=verbose)
            if start:
                start = False
                # In the first round only one half step
            else:
                # Half step
                integration += last_rate * force_step / 2.
            prob = exp(-integration / loading_rate)
            dpdf.append(last_rate / loading_rate * prob)
            forces.append(f_ext)
            if prob <= probability_break_value:
                break
            # Half step
            integration += last_rate * force_step / 2.
        return array(dpdf), array(forces)

    def external_force(self, T, force_max, force_min=0., force_step=0.01):
        """Return a list of external force values.

        The external force is not equal to
        f_ext = 'spring constant' * 'velocity'  * 'time' + force_min
        due to the spring and the elongation of the molecule.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of *f_ext* interval.
        force_min: float
            Lower limit of *f_ext* interval.
        force_step: float
            Step size of *f_ext*.

        Returns
        -------
        result 1: List of float
            External forces.
        result 2: List of float
            *f_ext* values.

        """
        if self.spring_ref is None:
            raise ValueError('You have to set the spring constant first.')
        spring_constant = self.spring_constant
        if self.force_unit == 'nN':
            spring_constant *= force_factor
        fs_tot = []
        forces = []
        # 'f_ext' has the meaning of [loading rate * time + force_min]
        # which is the external force for zero spring constant or unchanged
        # molecule length
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            d = self.get_mean_distance(f_ext, T)
            delta_d = d - self.spring_ref
            fs_tot.append(f_ext - spring_constant * delta_d)
            forces.append(f_ext)
        return fs_tot, forces

    def save_external_forces(self, T, force_max, force_min=0.,
                             force_step=0.01, fileout='force.dat'):
        """Save external forces. See method *external_force*.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of *f_ext* interval.
        force_min: float
            Lower limit of *f_ext* interval.
        force_step: float
            Step size of *f_ext*.
        fileout: str
            Filename.

        """
        fs_tot, forces = self.external_force(T, force_max, force_min,
                                             force_step)
        fd = open(fileout, 'w')
        fd.write('Loading rate * time\t' + 'External force\n')
        for i in range(len(fs_tot)):
            fd.write(str(round(forces[i], 10)) + '\t\t\t' + str(fs_tot[i]) +
                     '\n')
        fd.close()

    def rupture_force(self, T, P, loading_rate, force_max, force_min=0.,
                      force_step=0.01, method='Gibbs', verbose=False):
        """Calculate the average rupture force for a given loading rate
        by numerical integration.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_max: float
            Upper limit of the force interval. It should be set as
            large as possible and as necessary for a good result.
        force_min: float
            Lower limit of the force interval. It is assumed that
            *force_min* is the external force at time 0.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result: float

        """
        dpdf, forces = self.probability_density(T, P, loading_rate,
                                                force_max, force_min,
                                                force_step, method, verbose)
        if self.spring_constant == 0.:
            return rupture_force_from_dpdf(dpdf, forces)
        else:
            force_step = forces[1] - forces[0]
            fs_tot, forces = self.external_force(T, force_max, force_min,
                                                 force_step)
            return rupture_force_from_dpdf(dpdf, fs_tot, force_step)

    def rupture_force_and_uncertainty(self, T, P, loading_rate, force_max,
                                      force_min=0., force_step=0.01,
                                      method='Gibbs', verbose=False):
        """Calculate the average rupture force and its uncertainty for a
        given loading rate.

        The uncertainty is defined as the range
        around the average rupture force which contains all forces with a
        total probability of 68.3% (one standard deviation).

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_max: float
            Upper limit of the force interval. It should be set as
            large as possible and as necessary for a good result.
        force_min: float
            Lower limit of the force interval. It is assumed that
            *force_min* is the external force at time 0.
        force_step: float
            Force step size used.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result 1: float
            Rupture force.
        result 2: float
            Standard deviation.

        """
        dpdf, forces = self.probability_density(T, P, loading_rate,
                                                force_max, force_min,
                                                force_step, method, verbose)
        if self.spring_constant == 0.:
            return rupture_force_and_uncertainty_from_dpdf(dpdf, forces)
        else:
            force_step = forces[1] - forces[0]
            fs_tot, forces = self.external_force(T, force_max, force_min,
                                                 force_step)
            return rupture_force_and_uncertainty_from_dpdf(dpdf, fs_tot,
                                                           force_step)

    def most_probable_force_is_larger(self, f_ext, T, P, loading_rate,
                                      force_step=0.01):
        """Return *True* if the most probable force is larger than *f_ext*.

        The method is 'electronic'. The forces are only considered in the
        interval in which the rates can be calculated.

        Parameters
        ----------
        f_ext: float
            External force.
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_step: float
            Force step size used.

        Returns
        -------
        result: bool

        """
        try:
            dpdf, forces = self.probability_density(
                T, P, loading_rate, force_max=f_ext + force_step,
                force_min=f_ext, force_step=force_step, method='electronic')
        except ValueError:
            assert self.error in [1, 2]
            if self.error == 1:
                # *f_ext* or *f_ext + force_step* are too large for the
                # calculation of the rate
                return False
            elif self.error == 2:
                # *f_ext* or *f_ext + force_step* are too small for the
                # calculation of the rate
                return True
        if dpdf[0] < 1e-30:
            # If the *dpdf* values are near to zero than only because of
            # very small or very large rates
            rate = self.get_rate(f_ext, T, P, 'electronic', verbose=False)
            return rate / loading_rate < 1e-20
        # The ratio between two *dpdf* values are independent of *force_min*
        # and can be used to find the maximum
        return dpdf[1] / dpdf[0] > 1

    def get_force_limits(self, T, P, loading_rate, factor=10,
                         force_step=0.01, method='Gibbs'):
        """Determine good force limits for the calculation of the rupture
        force.

        The initial external force is assumed to be zero.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        factor: float
            The probability density at the limits of the interval will be
            smaller than the maximum of the probability distribution divided
            by *factor*.
        force_step: float
            Force step size used. The limits are multiples of *force_step*.
        method: 'electronic' or 'Gibbs'
            Defines whether electronic or Gibbs activation energies are used.

        Returns
        -------
        result 1: float
            Lower limit.
        result 2: float
            Upper limit.

        """
        assert method in ['electronic', 'Gibbs']
        self.error = None
        force_min = 0.
        if method == 'electronic':
            # Search most probable force
            n = -1
            f_ext = 0.
            while self.most_probable_force_is_larger(f_ext, T, P,
                                                     loading_rate,
                                                     force_step=force_step):
                n += 1
                f_ext = force_step * 2 ** n
            n -= 2
            if n < 0:
                self.error = 3
                raise ValueError('force_step is not small enough or the ' +
                                 'COGEF-trajectory was not calculated ' +
                                 'far enough.')
            f_ext -= force_step * 2 ** n
            while n >= 0:
                n -= 1
                if self.most_probable_force_is_larger(f_ext, T, P,
                                                      loading_rate,
                                                      force_step=force_step):
                    if n >= 0:
                        f_ext += force_step * 2 ** n
                    else:
                        f_ext += force_step
                else:
                    if n >= 0:
                        f_ext -= force_step * 2 ** n
            # Increase interval range around the most probable force in
            # dependence of *factor*
            force_max = f_ext
            ratio = 1.
            while ratio >= 1. / factor:
                try:
                    dpdf, forces = self.probability_density(
                        T, P, loading_rate, force_max + force_step,
                        force_max, force_step, method='electronic')
                except ValueError:
                    assert self.error in [1, 2]
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                if dpdf[0] < 1e-30:
                    self.error = 3
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                ratio *= dpdf[1] / dpdf[0]
                force_max += force_step

            force_min = f_ext
            ratio = 1.
            while ratio >= 1. / factor:
                try:
                    dpdf, forces = self.probability_density(
                        T, P, loading_rate, force_min, force_min - force_step,
                        force_step, method='electronic')
                except ValueError:
                    assert self.error in [1, 2]
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                if dpdf[0] < 1e-30:
                    self.error = 3
                    raise ValueError('force_step is not small enough or ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough.')
                ratio *= dpdf[0] / dpdf[1]
                force_min -= force_step
            return force_min, force_max
        elif method == 'Gibbs':
            # Calculate limits for method='electronic'
            force_min, force_max = self.get_force_limits(T, P, loading_rate,
                                                         factor,
                                                         force_step,
                                                         method='electronic')
            return self.get_force_limits_gibbs(T, P, loading_rate, force_min,
                                               force_max, factor, force_step)

    def get_force_limits_gibbs(self, T, P, loading_rate, force_min, force_max,
                               factor=10, force_step=0.01):
        """Determine good force limits for the calculation of the rupture
        force with method='Gibbs'.

        Parameters
        ----------
        T: float
            Temperature.
        P: float
            Pressure.
        loading_rate: float
            The force is assumed to inceases uniformly by this loading rate.
        force_min: float
            Lower limit for method='electronic'.
        force_max: float
            Upper limit for method='electronic'.
        factor: float
            The probability density at the limits of the interval will be
            smaller than the maximum of the probability distribution divided
            by *factor*.
        force_step: float
            Force step size used. The limits are multiples of *force_step*.

        Returns
        -------
        result 1: float
            Lower limit.
        result 2: float
            Upper limit.

        """
        # Estimate shift if method is changed from 'electronic' to 'Gibbs'
        rate_el_max = self.get_rate(force_max, T, P, 'electronic',
                                    verbose=False)
        f_ext = force_min
        rate_gibbs = self.get_rate(f_ext, T, P, 'Gibbs', verbose=False)
        while rate_gibbs > rate_el_max:
            f_ext -= force_step
            try:
                rate_gibbs = self.get_rate(f_ext, T, P, 'Gibbs',
                                           verbose=False)
            except ValueError:
                self.error = 3
                raise ValueError('COGEF-trajectory was not ' +
                                 'calculated far enough.')
        while rate_gibbs < rate_el_max:
            f_ext += force_step
            try:
                rate_gibbs = self.get_rate(f_ext, T, P, 'Gibbs',
                                           verbose=False)
            except ValueError:
                self.error = 3
                raise ValueError('COGEF-trajectory was not ' +
                                 'calculated far enough.')
        df = f_ext - force_max
        force_max += df
        force_min += df
        try:
            dpdf, forces = self.probability_density(T, P, loading_rate,
                                                    force_max, force_min,
                                                    force_step,
                                                    method='Gibbs')
        except ValueError:
            self.error = 3
            raise ValueError('COGEF-trajectory was not ' +
                             'calculated far enough.')
        imax = list(dpdf).index(max(dpdf))
        # Most probable force
        f_ext = forces[imax]
        # Increase the range of the interval in dependence of 'factor'
        force_max = f_ext
        ratio = 1.
        while ratio >= 1. / factor:
            try:
                dpdf, forces = self.probability_density(
                    T, P, loading_rate, force_max + force_step,
                    force_max, force_step, method='Gibbs')
            except ValueError:
                assert self.error in [1, 2]
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            if dpdf[0] < 1e-30:
                self.error = 3
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            ratio *= dpdf[1] / dpdf[0]
            force_max += force_step

        force_min = f_ext
        ratio = 1.
        while ratio >= 1. / factor:
            try:
                dpdf, forces = self.probability_density(
                    T, P, loading_rate, force_min, force_min - force_step,
                    force_step, method='Gibbs')
            except ValueError:
                assert self.error in [1, 2]
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            if dpdf[0] < 1e-30:
                self.error = 3
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')
            ratio *= dpdf[0] / dpdf[1]
            force_min -= force_step
        return force_min, force_max

    def get_minimum_distances(self):
        """Return the distances from the cogef images with intact bond.

        Returns
        -------
        result: list of floats

        """
        energies, distances = self.cogef.get_energy_curve(
            self.imagemin, self.imagemax, only_intact_bond_images=True,
            modulo=self.modulo)
        return distances

    def get_mean_distance(self, f_ext, T, check=True):
        """Return the mean distance from the cogef images.

        It is assumed that the molecule structure is always one image of the
        calculated minimum trajectory and Boltzmann distributed associated
        to their electronic energies.

        Parameters
        ----------
        f_ext: float
            External force.
        T: float
            Temperature.
        check: bool
            Set it to *True* in order to check whether the number of the
            last intact bond minimum is set. This is recommended.

        Returns
        -------
        result: float

        """
        distances = self.get_minimum_distances()
        energies = self.modified_energies(f_ext, only_intact_bond_images=True)
        assert len(distances) == len(energies)
        if (check) and (self.cogef.last_intact_bond_image >= len(energies)):
            raise ValueError("You have to set 'last_intact_bond_image' of " +
                             'the COGEF object.')
        sum_dist = 0.
        sum_weight = 0.
        for i, energy in enumerate(energies):
            dist = distances[i]
            weight = exp(-energy / (kB * T))
            sum_dist += dist * weight
            sum_weight += weight
        return sum_dist / sum_weight

    def get_mean_distances(self, T, force_max, force_min=0., force_step=0.01,
                           use_spring_ref=False):
        """Return mean distances. See method *get_mean_distance*.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        use_spring_ref: bool
            *True* means that distances are obtained relative to the
            equilibrium distance. This is possible if a spring constant
            is set.

        Returns
        -------
        result 1: list of float
            Mean distances.
        result 2: list of float
            External forces.

        """
        dists = []
        forces = []
        if use_spring_ref:
            assert self.spring_ref is not None
            dist0 = self.spring_ref
        else:
            dist0 = 0.
        for f_ext in arange(force_min, force_max + force_step / 2.,
                            force_step):
            dists.append(self.get_mean_distance(f_ext, T) - dist0)
            forces.append(f_ext)
        return dists, forces

    def save_mean_distances(self, T, force_max, force_min=0., force_step=0.01,
                            fileout='dists.dat', use_spring_ref=False):
        """Save mean distances to a file. See method *get_mean_distances*.

        Parameters
        ----------
        T: float
            Temperature.
        force_max: float
            Upper limit of the force interval.
        force_min: float
            Lower limit of the force interval.
        force_step: float
            Force step size used.
        fileout: str
            Filename.
        use_spring_ref: bool
            *True* means that distances are obtained relative to the
            equilibrium distance. This is possible if a spring constant
            is set.

        """
        dists, forces = self.get_mean_distances(T, force_max, force_min,
                                                force_step, use_spring_ref)
        if use_spring_ref:
            distance = 'delta d'
        else:
            distance = 'distance'
        fd = open(fileout, 'w')
        if self.spring_constant == 0.:
            fd.write('Force\t' + 'Mean ' + distance + '\n')
            space = '\t'
        else:
            fd.write('Loading rate * time\t' + 'Mean ' + distance + '\n')
            space = '\t\t\t'
        for i in range(len(dists)):
            fd.write(str(round(forces[i], 10)) + space + str(dists[i]) + '\n')
        fd.close()

    def get_d_parameter(self, T, P, loading_rate, dpdf, forces,
                        method='Gibbs'):
        """Get the d-parameter.

        The parameter d can be used to describe the dependence of the
        rupture force on loading rate and temperature using the function
        *estimate_force_change*.

        Parameters
        ----------
        T: float
            Temperature used for dpdf.
        P: float
            Pressure used for dpdf.
        loading_rate: float
            Loading rate used for dpdf.
        dpdf: numpy array of float
            dpdf-values from method *probability_density*.
        forces: numpy array of float
            External forces from method *probability_density* associated to
            dpdf.
        method: 'electronic' or 'Gibbs'
            Method used for dpdf.

        Returns
        -------
        result: float
            The d-parameter in Angstrom.

        """
        if self.force_unit == 'nN':
            loading_rate /= force_factor
        index = list(dpdf).index(max(dpdf))
        # Most probable rupture force
        fmp = forces[index]
        rate = self.get_rate(fmp, T, P, method, verbose=False)
        return kB * T / loading_rate * rate


def estimate_force_change(d, T, T_new, loading_rate, loading_rate_new,
                          force_unit='eV/A'):
    """Estimate change of the rupture force.

    The rupture force change can be estimated for small changes of
    temperature and loading rate with the help of the d-parameter from
    method *get_d_parameter* in class *Dissociation*.

    Parameters
    ----------
    d: float
        d-parameter.
    T: float
        Temperature associated to the d-parameter.
    T_new: float
        Temperature of the estimated rupture force.
    loading_rate: float
        Loading rate associated to the d-parameter.
    loading_rate_new: float
        Loading rate of the estimated rupture force.
    force_unit: str
        If it is set to 'nN' than the force value which is returned is in
        nN and the loading rates have unit nN/s. The loading rate has unit
        eV/(A*s) if force_unit is set to 'eV/A', where A stands for Angstrom.

    """
    factor = 1.
    if force_unit == 'nN':
        factor = force_factor
        loading_rate /= factor
        loading_rate_new /= factor
    # h in units eV * s
    h = _hplanck / _e
    part1 = T * log(loading_rate * d * h / (kB * T)**2)
    part2 = T_new * log(loading_rate_new * d * h / (kB * T_new)**2)
    return kB / d * (part2 - part1) * factor
