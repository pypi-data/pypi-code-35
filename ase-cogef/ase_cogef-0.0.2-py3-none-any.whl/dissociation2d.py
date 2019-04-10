# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Similar to module class *Dissociation* in cogef.py but considering
two dimensions of the Born-Oppenheimer surface.

"""

import sys
from numpy import exp, arange, multiply, array
from copy import deepcopy
from warnings import warn

from ase.parallel import rank
from ase.units import kB
from ase.thermochemistry import IdealGasThermo

from cogef import Dissociation, rupture_force_from_dpdf
from cogef import rupture_force_and_uncertainty_from_dpdf


class Dissociation2d(Dissociation):
    """This class is conceived for analysing the trajectories from COGEF2D.

    Class for calculating energy barriers, dissociation rates
    and the resulting rupture force at a given temperature and pressure.

    Parameters
    ----------
    cogef2d: COGEF object
        The 3s-cogef path.
    initialize: function
        Initialization function which is executed before each vibrational
        analysis. See function *do_nothing_vib* in module dissociation.py.
    minimum_dirname: str
        The general directory name for files of the
        vibrational analysis of images from the reactant minimum curve.
        Image indices will be added automatically.
    maximum_dirname: str
        The general directory name for files of the
        vibrational analysis of images from the transition maximum curve.
        Image indices will be added automatically.
    broken_bond_minimum_dirname: str
        The general directory name for files of the
        vibrational analysis of images from the product minimum curve.
        Image indices will be added automatically.
    imagemin: int
        Image number of first image used from the 3s-cogef path.
    imagemax: int
        Image number of last image used from the 3s-cogef path.
        Negative values can be used to count from the other direction.
    modulo: int
        Set it to a larger value that less images are used from the 3s-cogef
        paths, e.g. *modulo=2* means that every second image is used.
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
    allow_max_at_lower_limit: bool
        To suppress error messages when the energy extremum is found at the
        beginning of the maximum curve.
    allow_max_at_upper_limit: bool
        To suppress error messages when the energy extremum is found at the
        end of the maximum curve.
    allow_min_at_lower_limit: bool
        To suppress error messages when the energy extremum is found at the
        beginning of the product minimum curve.
    allow_min_at_upper_limit: bool
        To suppress error messages when the energy extremum is found at the
        end of the product minimum curve.
    mode2d: bool
        Switch between 1s- (*False*) and 3s-COGEF (*True*).
    intact_bond_minimum: bool
        Some methods need the specification which minimum should be used,
        the reactant minimum with intact bond (*True*) or the product minimum
        with broken bond (*False*). For instance you can use it to define
        whether the rate constant for the forward or backward reaction
        should be calculated.
    consider_back_reaction: bool
        When the back reaction is considered, product states must be obtained
        to get the corresponding rate constants. It influences also the
        probability density dp/df.
    image_range: int
        Global extrema on the maximum and product minimum curves are assumed
        to be identified when *image_range* images are obtained on both
        sides of the extremum image.
    gapimages: list of int
        There are sometimes image numbers for which no point of the maximum
        and product minimum curves can be found although they are
        surrounded by two images for which these points can be found.
        The origin of this problem can be the finit step size. To get
        no problems in finding the maximum or product minimum in this
        case, one should add these image numbers into *gapimages*.
    transition_into_two_fragments: bool (optional but recommended)
        Defines whether the molecule splits into two fragments during the
        considered reaction (dissociation in contrast to ring-opening
        reaction).
    spring_on_atom1: bool
        Defines the connection point of the spring if there is a spring.
        *True*: self.cogef.atom1, *False*: self.cogef.atom2.
    average_rate: bool
        When spring constant is not zero and *average_rate* is
        *True*, the rate constants are obtained as average over both spring
        positions (atom1/atom2). If it is *False*, the connection is defined
        by *spring_on_atom1*.
    infinit_entropy: float or tuple of two floats (optional)
        Product states at large distances could have too many imaginary
        frequencies. *infinit_entropy* can be set to the total entropy
        of the two fragments at infinit distance for the used spring
        constant. *infinit_extra_trans_rot* must also be set in this case.
        Then the associated frequencies of each image are corrected.
        *infinit_entropy* can also be a tuple of two floats where
        *infinit_entropy[spring_on_atom1]* defines the respective
        value in dependence of the connection point of the spring.
    infinit_extra_trans_rot (optional):
        The number of additional translational and rotational degrees of
        freedom arising from splitting (e.g. *infinit_extra_trans_rot=6*).

    """
    def __init__(self, cogef2d, initialize=None, minimum_dirname='image',
                 maximum_dirname='max_image',
                 broken_bond_minimum_dirname='min_image', imagemin=0,
                 imagemax=-1, modulo=1, gibbs_method='canonical',
                 vib_method='standard', vib_indices=None, vib_delta=0.01,
                 vib_nfree=2, vib_class='Vibrations', geometry='nonlinear',
                 symmetrynumber=1, spin=0, force_unit='eV/A',
                 allow_max_at_lower_limit=False,
                 allow_max_at_upper_limit=False,
                 allow_min_at_lower_limit=False,
                 allow_min_at_upper_limit=False, mode2d=True,
                 intact_bond_minimum=True, consider_back_reaction=False,
                 image_range=3, gapimages=None,
                 transition_into_two_fragments=None, spring_on_atom1=True,
                 average_rate=True, infinit_entropy=None,
                 infinit_extra_trans_rot=None):
        Dissociation.__init__(self, deepcopy(cogef2d), initialize,
                              minimum_dirname, imagemin, imagemax, modulo,
                              gibbs_method, vib_method, vib_indices,
                              vib_delta, vib_nfree, vib_class, geometry,
                              symmetrynumber, spin, force_unit,
                              allow_max_at_upper_limit, spring_on_atom1,
                              average_rate)
        self.allow_max_at_lower_limit = allow_max_at_lower_limit
        self.allow_min_at_upper_limit = allow_min_at_upper_limit
        self.allow_min_at_lower_limit = allow_min_at_lower_limit
        self.mode2d = mode2d
        self.cogef2d = cogef2d
        self.minimum_dirname = minimum_dirname
        self.maximum_dirname = maximum_dirname
        self.broken_bond_minimum_dirname = broken_bond_minimum_dirname
        self.intact_bond_minimum = intact_bond_minimum
        self.consider_back_reaction = consider_back_reaction
        # If the calculation of the energy barrier produces an error due to
        # missing images of the maximum or the product minimum curve, the
        # associated image number will be filled in *self.needed_max_images*
        # or *self.needed_min_images*
        self.needed_max_images = []
        self.needed_min_images = []
        self.image_range = image_range
        if gapimages is None:
            gapimages = []
        self.gapimages = gapimages
        self.transition_into_two_fragments = transition_into_two_fragments
        if transition_into_two_fragments is None:
            warn("If transition_into_two_fragments is not set to 'True' or " +
                 "'False', it tries to find it out automatically. But this " +
                 'is not save.')
        self.infinit_entropy = infinit_entropy  # eV / K
        self.infinit_extra_trans_rot = infinit_extra_trans_rot

    def set_spring_constant(self, spring_constant, T, force_min=0.,
                            spring_ref=None):
        """Set the spring constant of the cantilever which stretches the
        molecule. See class *Dissociation*.

        """
        intact_bond_minimum = self.intact_bond_minimum
        try:
            self.intact_bond_minimum = True
            Dissociation.set_spring_constant(self, spring_constant, T,
                                             force_min, spring_ref)
        finally:
            self.intact_bond_minimum = intact_bond_minimum
        return self.spring_ref

    def clean_needed_images_list(self):
        """Clean the lists *self.needed_max_images* and
        *self.needed_min_images*.

        """
        self.needed_max_images = []
        self.needed_min_images = []

    def modified_energies(self, f_ext, shift=True, minimum=True,
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
        minimum: bool
            Defines the segment of the 3s-cogef path: maximum curve (*False*)
            or one of the minimum curves (*True*). Reactant and product
            minimum curves are selected by *self.intact_bond_minimum*.
        only_intact_bond_images: bool
            *True* means that the given number of the last intact bond image
            defines the upper limit of used images if *minimum* and
            *self.intact_bond_minimum* is *True*.

        Returns
        -------
        result: list of floats
            Force-tilted energies in the order of the image numbers.

        """
        if (minimum) and (self.intact_bond_minimum):
            # Reactant/Intact-bond minimum
            self.cogef.images = self.cogef2d.images
            result = Dissociation.modified_energies(self, f_ext, shift,
                                                    only_intact_bond_images)
        else:
            # Maximum or product/broken-bond minimum
            self._fill_cogef_with_images(minimum)
            imagemin = self.imagemin
            imagemax = self.imagemax
            modulo = self.modulo
            try:
                self.imagemin = 0
                self.imagemax = -1
                self.modulo = 1
                result = Dissociation.modified_energies(self, f_ext, shift)
            finally:
                self.imagemin = imagemin
                self.imagemax = imagemax
                self.modulo = modulo
        self.cogef.images = self.cogef2d.images
        return result

    def _fill_cogef_with_images(self, minimum):
        """Fill images into *self.cogef*.

        First take images from the range *[self.imagemin, self.imagemax]*
        and remove later empty images which have not yet been calculated.

        Parameters
        ----------
        minimum: bool
            Defines the segment of the 3s-cogef path: maximum curve (*False*)
            or product minimum curves (*True*).

        """
        if minimum:
            images = self.cogef2d.minimum_images
        else:
            images = self.cogef2d.maximum_images
        imagemax = self.imagemax
        imagemin = self.imagemin
        if imagemax < 0:
            imagemax += len(images)
        if minimum:
            imagemax = min(imagemax, self.cogef2d.last_broken_bond_image)
        self.cogef.images = []
        for i in range(imagemin, imagemax + 1):
            if i % self.modulo != 0:
                continue
            image = images[i]
            if not(image):
                continue
            self.cogef.images.append(image)

    def electronic_extreme_values(self, f_ext, shift=True,
                                  only_minimum=False):
        """Return the maximum and minimum defining the electronic energy
        barrier. See class *Dissociation*.

        """
        self.error = None
        if not(self.mode2d):
            self.cogef.images = self.cogef2d.images
            return Dissociation.electronic_extreme_values(self, f_ext, shift,
                                                          only_minimum)
        # mode2d
        # *shift* must be False, here
        self.cogef.images = self.cogef2d.images
        intact_bond_minimum = self.intact_bond_minimum
        try:
            self.intact_bond_minimum = True
            pmin = Dissociation.electronic_extreme_values(self, f_ext,
                                                          shift=False,
                                                          only_minimum=True)
        finally:
            self.intact_bond_minimum = intact_bond_minimum
        imgmin = []
        if not(self.intact_bond_minimum):
            # Minimum is product/broken-bond minimum
            imgmin.append((self.cogef2d.minimum_images, True, True))
        if not(only_minimum):
            imgmin.append((self.cogef2d.maximum_images, False, True))
            if not(self.cogef2d.fix_force_for_max_curve):
                # Search the transition state not only on the
                # maximum curve but also on the product/broken-bond minimum
                # curve
                imgmin.append((self.cogef2d.minimum_images, True, False))
        for images, is_minimum, search_minimum in imgmin:
            # *search_minimum* is only used in fixed-d-method
            if self.cogef2d.fix_force_for_max_curve:
                # Fixed-force-method
                imagemin = self.imagemin
                imagemax = self.imagemax
                try:
                    self.imagemin = 0
                    self.imagemax = -1
                    self.cogef.images = [images[pmin[0]]]
                    if self.cogef.images[0]:
                        energies = Dissociation.modified_energies(self, f_ext,
                                                                  shift=False)
                        if is_minimum:
                            pmin = (pmin[0], energies[0])
                        else:
                            pmax = (pmin[0], energies[0])
                    else:
                        if is_minimum:
                            self.needed_min_images.append(pmin[0])
                            self.error = 1
                            raise ValueError('Cannot find suitable image ' +
                                             'of the product minimum ' +
                                             'energy curve (image' +
                                             str(pmin[0]) +
                                             '). If you have started ' +
                                             'the calculation of this ' +
                                             'minimum energy curve at ' +
                                             'the smallest image number ' +
                                             'without a gap, f_ext is ' +
                                             'too large or this minimum ' +
                                             'energy curve was not ' +
                                             'calculated far enough.')
                        else:
                            self.needed_max_images.append(pmin[0])
                            self.error = 2
                            raise ValueError('Cannot find suitable image ' +
                                             'of the maximum ' +
                                             'energy curve (image ' +
                                             str(pmin[0]) +
                                             '). If you have started ' +
                                             'the calculation of the ' +
                                             'maximum energy curve at ' +
                                             'the largest image number ' +
                                             'without a gap, f_ext is ' +
                                             'too small or the maximum ' +
                                             'energy curve was not ' +
                                             'calculated far enough ' +
                                             'in the direction of ' +
                                             'smaller image numbers.')
                finally:
                    self.imagemin = imagemin
                    self.imagemax = imagemax
                    self.cogef.images = self.cogef2d.images
            else:
                # Fixed-d-method
                intact_bond_minimum = self.intact_bond_minimum
                imagemin = self.imagemin
                imagemax = self.imagemax
                try:
                    if not(search_minimum):
                        self.intact_bond_minimum = False
                        if self.transition_into_two_fragments is True:
                            imin = 0
                        else:
                            energies = self.modified_energies(
                                f_ext, shift=False, minimum=is_minimum)
                            emin = min(energies)
                            imin = energies.index(emin)
                        if imin > 0:
                            self.imagemin = pmax[0] + 1
                            energies = self.modified_energies(
                                f_ext, shift=False, minimum=is_minimum)
                            self.imagemin = imagemin
                        if (imin == 0) or (emin in energies):
                            # Search maximum at larger distances than
                            # minimum of maximum curve
                            self.imagemin = pmax[0]
                        else:
                            # Search maximum at smaller distances than
                            # minimum of maximum curve
                            self.imagemax = pmax[0]
                    i_start = self.imagemin - imagemin
                    if i_start % self.modulo != 0:
                        i_start += self.modulo - i_start % self.modulo
                    search_start = 0
                    energies = self.modified_energies(f_ext, shift=False,
                                                      minimum=is_minimum)
                    if not(search_minimum):
                        if len(energies) == 0:
                            if self.imagemin == pmax[0]:
                                for j in range(pmax[0] - 1, -1, -1):
                                    if self.cogef.minimum_images[j] \
                                       is not None:
                                        self.error = 1
                                        self.needed_min_images.append(j + 1)
                                        raise ValueError(
                                            'The minimum energy curve was ' +
                                            'not calculated far enough.')
                        if self.transition_into_two_fragments is True:
                            i = 0
                        else:
                            # If minimum on product/broken-bond minimum
                            # curve can be
                            # found (means: minimum is not the left or right
                            # limit of the calculated images), then search
                            # maximum only on the left hand side of the
                            # minimum
                            i = energies.index(min(energies))
                        if self.imagemin == pmax[0]:
                            if (self.transition_into_two_fragments is None) \
                               and (i > 0) and (i < len(energies) - 1) or \
                               (self.transition_into_two_fragments is False):
                                # Minimum not on the left or right limit
                                # could mean that it does not dissociate
                                energies = energies[:i + 1]
                        else:
                            search_start = i
                finally:
                    self.intact_bond_minimum = intact_bond_minimum
                    self.imagemin = imagemin
                    self.imagemax = imagemax
                if len(energies) == 0:
                    if is_minimum:
                        raise RuntimeError('This minimum energy curve ' +
                                           'has no points, yet, or it ' +
                                           'has too less points for the ' +
                                           'used modulo value.')
                    else:
                        raise RuntimeError('The maximum energy curve ' +
                                           'has no points, yet, or it ' +
                                           'has too less points for the ' +
                                           'used modulo value.')
                if search_minimum:
                    eminmax = min(energies)
                else:
                    eminmax = max(energies[search_start:])
                i = energies.index(eminmax)
                # Index number must be corrected due to empty images
                # and modulo value
                iminmax = i_start - self.modulo
                while i >= 0:
                    iminmax += self.modulo
                    if images[iminmax] is not None:
                        i -= 1
                if search_minimum:
                    if is_minimum:
                        pmin = (iminmax, eminmax)
                    else:
                        pmax = (iminmax, eminmax)
                else:
                    if not(self.allow_min_at_lower_limit):
                        # In order to find the maximum at smaller or larger
                        # distance values than the minimum (both in
                        # product/broken-bond (bbm) minimum curve),
                        # the bbm curve must be
                        # completely known for smaller or larger distances
                        # down or up to the distance of the minimum of the
                        # maximum curve
                        if iminmax >= pmax[0]:
                            step = -1
                        else:
                            step = 1
                        for i in range(iminmax + step, pmax[0] + step, step):
                            if not(images[i]) and (i not in self.gapimages):
                                self.error = 1
                                self.needed_min_images.append(i)
                                raise ValueError('f_ext is ' +
                                                 'too large or the ' +
                                                 'maximum energy curve ' +
                                                 'was not calculated ' +
                                                 'far enough.')
                    if eminmax > pmax[1]:
                        if not(self.intact_bond_minimum):
                            # Check if barrier was found on the correct side
                            assert (pmin[0] >= pmax[0]) == \
                                (iminmax >= pmax[0])
                        # Transition state is maximum of product/broken-bond
                        # minimum curve, indicated by a negative image number
                        pmax = (-iminmax, eminmax)
                        # Indication doesn't work if image number is zero
                        assert iminmax > 0
                    else:
                        # No change: Transition state is minimum of maximum
                        # curve
                        continue
                for n in range(1, self.image_range + 1):
                    i = iminmax + n * self.modulo
                    if ((i >= len(images)) or (images[i] is None)) and \
                       (i not in self.gapimages):
                        if is_minimum:
                            if not(self.allow_min_at_upper_limit) and \
                               (i <= self.cogef2d.last_broken_bond_image):
                                self.error = 1
                                self.needed_min_images.append(i)
                                raise ValueError('f_ext is ' +
                                                 'too large or this ' +
                                                 'minimum energy curve ' +
                                                 'was not calculated ' +
                                                 'far enough. gapimages ' +
                                                 'could also help.')
                        else:
                            if not(self.allow_max_at_upper_limit) and \
                               (i <= self.cogef2d.last_intact_bond_image):
                                self.error = 1
                                self.needed_max_images.append(i)
                                raise ValueError('f_ext is ' +
                                                 'too large or the ' +
                                                 'maximum energy curve ' +
                                                 'was not calculated ' +
                                                 'far enough. gapimages ' +
                                                 'could also help.')
                    i = iminmax - n * self.modulo
                    if ((i < 0) or (images[i] is None)) and \
                       (i not in self.gapimages):
                        if is_minimum:
                            if not(self.allow_min_at_lower_limit):
                                self.error = 2
                                self.needed_min_images.append(i)
                                raise ValueError('f_ext is ' +
                                                 'too small or this ' +
                                                 'minimum energy curve ' +
                                                 'was not calculated ' +
                                                 'far enough. gapimages ' +
                                                 'could also help.')
                        else:
                            if not(self.allow_max_at_lower_limit):
                                self.error = 2
                                self.needed_max_images.append(i)
                                raise ValueError('f_ext is ' +
                                                 'too small or the ' +
                                                 'maximum energy curve was ' +
                                                 'not calculated far ' +
                                                 'enough. gapimages ' +
                                                 'could also help.')
        if only_minimum:
            return pmin
        else:
            return pmax, pmin

    def gibbs_energy_barrier(self, f_ext, T, P, verbose=True):
        """Return the Gibbs activation energy/energy barrier height at given
        temperature and pressure. See class *Dissociation*.

        """
        if not(self.mode2d):
            self.dirname = self.minimum_dirname
            return Dissociation.gibbs_energy_barrier(self, f_ext, T, P,
                                                     verbose)
        verbose = (verbose) and (rank == 0)
        method = self.gibbs_method
        assert method in ['canonical']
        if method == 'canonical':
            # Canonical Transition-state theory
            # Use Gibbs energies from the configurations of the
            # electronic maximum (Transition-state structure) and minimum.
            # This is an approximation.
            pmax, pmin = self.electronic_extreme_values(f_ext)
            emax = pmax[1]
            emin = pmin[1]
            imax = pmax[0]
            imin = pmin[0]
            if self.cogef2d.fix_force_for_max_curve:
                assert imax == imin  # By definition
            # Gibbs energy at the minimum and maximum
            for is_maximum, i in [(False, imin), (True, imax)]:
                if not(self.cogef2d.fix_force_for_max_curve) and \
                   (is_maximum) and (i < 0):
                    # Negative index number indicates that transition state
                    # is sitting on product/broken-bond minimum (bbm)
                    # curve instead of maximum curve
                    bbm_curve_anyway = True
                    i *= -1
                else:
                    bbm_curve_anyway = False
                if verbose:
                    if is_maximum:
                        sys.stdout.write('\n' + 'Maximum:')
                    else:
                        sys.stdout.write('\n' + 'Minimum:')
                if is_maximum:
                    if bbm_curve_anyway:
                        self.cogef.images = self.cogef2d.minimum_images
                        self.dirname = self.broken_bond_minimum_dirname
                    else:
                        self.cogef.images = self.cogef2d.maximum_images
                        self.dirname = self.maximum_dirname
                    potentialenergy = emax
                else:
                    if self.intact_bond_minimum:
                        self.cogef.images = self.cogef2d.images
                        self.dirname = self.minimum_dirname
                    else:
                        self.cogef.images = self.cogef2d.minimum_images
                        self.dirname = self.broken_bond_minimum_dirname
                    potentialenergy = emin
                self.calculate_vibrations(i)
                gibbs = self.get_gibbs_energy(i, T, P, potentialenergy,
                                              is_maximum, verbose)
                if is_maximum:
                    gibbs_max = gibbs
                else:
                    gibbs_min = gibbs
            self.cogef.images = self.cogef2d.images
            self.dirname = self.minimum_dirname
            return gibbs_max - gibbs_min

    def vib_energy_correction(self, vib_energies, image, is_maximum, T, P):
        """This method can be used to correct vibrational frequencies.

        See class *Dissociation*.

        """
        if self.infinit_entropy is not None:
            # Frequency correction
            if type(self.infinit_entropy) in [list, tuple]:
                infinit_entropy = self.infinit_entropy[self.spring_on_atom1]
            else:
                infinit_entropy = self.infinit_entropy
            extradofs = self.infinit_extra_trans_rot
            assert extradofs > 0
            natoms = len(image)
            if self.geometry == 'nonlinear':
                removedofs = 6 + extradofs
            elif self.geometry == 'linear':
                removedofs = 5 + extradofs
            less_vib_energies = vib_energies[-(3 * natoms - removedofs):]
            thermo = IdealGasThermo(vib_energies=less_vib_energies,
                                    potentialenergy=0,
                                    atoms=image,
                                    geometry=self.geometry,
                                    symmetrynumber=self.symmetrynumber,
                                    spin=self.spin)
            delta_entropy = infinit_entropy - \
                thermo.get_entropy(T, P, verbose=False)
            freq_min = kB * T * exp(1 - delta_entropy / (kB * extradofs))
            for i in range(removedofs - extradofs, removedofs):
                if (vib_energies[i]**2).real < freq_min**2:
                    vib_energies[i] = freq_min
        vib_energies = Dissociation.vib_energy_correction(
            self, vib_energies, image, is_maximum, T, P)
        return vib_energies

    def get_all_rate_constants(self, T, P, force_max, force_min=0.,
                               force_step=0.01, method='Gibbs',
                               neglect_small_backward_rates=False,
                               neglect_factor=100., verbose=False):
        """Return dissociation rate constants for forward and backward
        reaction.

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
        neglect_small_backward_rates: bool
            When the backward rate constants are much smaller than
            the forward rate constants, they are simply set to zero in the
            following such that less product/broken-bond minima must be
            calculated. This is enabled if *neglect_small_backward_rates*
            is set to *True*.
        neglect_factor: float
            Small backward rate constants are only neglected when they are
            smaller than the forward rate constants divided by
            *neglect_factor*.
        verbose: bool
            Set it to *True* to get more informations.

        Returns
        -------
        result1: list of floats
            Rate constants for forward reaction.
        result2: list of floats
            Rate constants for backward reaction.
        result3: list of floats
            External forces.

        """
        if not(self.consider_back_reaction):
            # There is only a forward reaction
            assert self.intact_bond_minimum
            return self.get_rate_constants(T, P, force_max, force_min,
                                           force_step, method, verbose)
        intact_bond_minimum = self.intact_bond_minimum
        neglect_backward_reaction = False
        try:
            self.intact_bond_minimum = True
            rates, forces = self.get_rate_constants(T, P, force_max,
                                                    force_min, force_step,
                                                    method, verbose)
            self.intact_bond_minimum = False
            back_rates = []
            for i, f_ext in enumerate(arange(force_min,
                                             force_max + force_step / 2.,
                                             force_step)):
                if neglect_backward_reaction:
                    rate = 0.
                else:
                    self.intact_bond_minimum = False
                    rate = self.get_rate(f_ext, T, P, method, verbose)
                    if (neglect_small_backward_rates) and \
                       (rates[i] > rate * neglect_factor):
                        neglect_backward_reaction = True
                back_rates.append(rate)
        finally:
            self.intact_bond_minimum = intact_bond_minimum
        return rates, back_rates, forces

    def save_all_rate_constants(self, T, P, force_max, force_min=0.,
                                force_step=0.01, method='Gibbs',
                                fileout='rates.dat',
                                neglect_small_backward_rates=False,
                                neglect_factor=100.):
        """Save dissociation rate constants for forward and backward
        reaction to a file.

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
        neglect_small_backward_rates: bool
            When the backward rate constants are much smaller than
            the forward rate constants, they are simply set to zero in the
            following such that less product/broken-bond minima must be
            calculated. This is enabled if *neglect_small_backward_rates*
            is set to *True*.
        neglect_factor: float
            Small backward rate constants are only neglected when they are
            smaller than the forward rate constants divided by
            *neglect_factor*.

        """
        if not(self.consider_back_reaction):
            # There is only a forward reaction
            assert self.intact_bond_minimum
            return self.save_rate_constants(T, P, force_max, force_min,
                                            force_step, method, fileout)
        rates, back_rates, forces = self.get_all_rate_constants(
            T, P, force_max, force_min, force_step, method,
            neglect_small_backward_rates, neglect_factor)
        fd = open(fileout, 'w')
        if self.spring_constant == 0.:
            fd.write('Force\t' + 'Forward rate constant\t' +
                     'Backward rate constant\n')
            space = '\t'
        else:
            fd.write('Loading rate * time\t' + 'Forward rate constant\t' +
                     'Backward rate constant\n')
            space = '\t\t\t'
        for i in range(len(rates)):
            fd.write(str(round(forces[i], 10)) + space + str(rates[i]) +
                     '\t\t' + str(back_rates[i]) + '\n')
        fd.close()

    def probability_density(self, T, P, loading_rate, force_max,
                            force_min=0., force_step=0.01, method='Gibbs',
                            verbose=False, probability_break_value=0.,
                            return_probs=False):
        """Return a list of dp/df-values within a given force interval.
        See class *Dissociation*.

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
        return_probs: bool
            Probabilities are also returned if it is *True*.

        Returns
        -------
        result1: list of float or tuple of two lists of float
            dp/df-values and optional p-values.
        result2: list of float
            External forces.

        """
        if not(self.consider_back_reaction):
            assert self.intact_bond_minimum
            return Dissociation.probability_density(self, T, P, loading_rate,
                                                    force_max, force_min,
                                                    force_step, method,
                                                    verbose,
                                                    probability_break_value)
        prob_old = 1.
        prob = 1.
        dpdf = []
        if return_probs:
            probs = []
        forces = []
        intact_bond_minimum = self.intact_bond_minimum
        neglect_backward_reaction = False
        try:
            start = True
            for f_ext in arange(force_min, force_max + force_step / 2.,
                                force_step):
                # Rate constant in forward direction
                self.intact_bond_minimum = True
                last_rate1 = self.get_rate(f_ext, T, P, method,
                                           verbose=verbose)
                # Rate constant in backward direction
                if neglect_backward_reaction:
                    last_rate2 = 0.
                else:
                    self.intact_bond_minimum = False
                    last_rate2 = self.get_rate(f_ext, T, P, method,
                                               verbose=verbose)
                    if last_rate1 > last_rate2 * 100.:
                        neglect_backward_reaction = True
                ratio = last_rate2 / (last_rate1 + last_rate2)
                expo = -(last_rate1 + last_rate2) / loading_rate
                step = force_step / 2.
                if start:
                    start = False
                    # In the first round only one half step
                else:
                    # Half step
                    prob = (prob - ratio) * exp(expo * force_step / 2.) + \
                        ratio
                    step += force_step / 2.
                if prob <= probability_break_value:
                    break
                # Half step
                prob = (prob - ratio) * exp(expo * force_step / 2.) + ratio
                dpdf.append(-(prob - prob_old) / step)
                if return_probs:
                    probs.append(prob)
                forces.append(f_ext)
                prob_old = prob
        finally:
            self.intact_bond_minimum = intact_bond_minimum
        if return_probs:
            return (dpdf, probs), forces
        else:
            return dpdf, forces

    def external_force(self, T, force_max, force_min=0., force_step=0.01,
                       probs_intact_bond=None):
        """Return a list of external force values. See class *Dissociation*.

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
        probs_intact_bond: List of float
            When back reaction is considered, probabilities of intact bond
            must be set in order to get the total average forces.
            You can use the method *probability_density* with
            *return_probs=True* and the same force range and force step
            in order to get these probabilities. If *probs_intact_bond* is
            *None*, the total average forces cannot be calculated yet,
            and average forces of both the reactant/intact-bond minimum
            curve and the product/broken-bond minimum curve are returned.

        Returns
        -------
        result 1: List of float or tuple of two lists of float
            Average external forces or external force associated to the
            reactant and product states.
        result 2: List of float
            *f_ext* values.

        """
        if not(self.consider_back_reaction):
            assert self.intact_bond_minimum
            return Dissociation.external_force(
                self, T, force_max, force_min, force_step)
        intact_bond_minimum = self.intact_bond_minimum
        try:
            self.intact_bond_minimum = True
            fs_tot_intact, forces = Dissociation.external_force(
                self, T, force_max, force_min, force_step)
            self.intact_bond_minimum = False
            fs_tot_broken, forces = Dissociation.external_force(
                self, T, force_max, force_min, force_step)
            if probs_intact_bond is not None:
                probs_intact_bond = array(probs_intact_bond)
                fs_tot_intact = multiply(fs_tot_intact, probs_intact_bond)
                fs_tot_broken = multiply(fs_tot_broken,
                                         1. - probs_intact_bond)
                fs_tot = fs_tot_intact + fs_tot_broken
        finally:
            self.intact_bond_minimum = intact_bond_minimum
        if probs_intact_bond is None:
            return (fs_tot_intact, fs_tot_broken), forces
        else:
            return fs_tot, forces

    def save_all_external_forces(self, T, force_max, force_min=0.,
                                 force_step=0.01, fileout='force.dat'):
        """Save external forces for both the reactant/intact-bond minimum
        curve and the product/broken-bond minimum curve.

        See method *save_external_forces* in class *Dissociation*.

        """
        if not(self.consider_back_reaction):
            assert self.intact_bond_minimum
            return self.save_external_forces(T, force_max, force_min,
                                             force_step, fileout)
        result, forces = self.external_force(T, force_max, force_min,
                                             force_step)
        fs_tot_intact, fs_tot_broken = result[0], result[1]
        fd = open(fileout, 'w')
        fd.write('Loading rate * time\t' + 'Intact external force\t' +
                 'Broken external force\n')
        for i in range(len(fs_tot_intact)):
            fd.write(str(round(forces[i], 10)) + '\t\t\t' +
                     str(fs_tot_intact[i]) + '\t\t' + str(fs_tot_broken[i]) +
                     '\n')
        fd.close()

    def rupture_force(self, T, P, loading_rate, force_max, force_min=0.,
                      force_step=0.01, method='Gibbs', verbose=False):
        """Calculate the average rupture force for a given loading rate
        by numerical integration. See class *Dissociation*.

        """
        if not(self.consider_back_reaction):
            assert self.intact_bond_minimum
            return Dissociation.rupture_force(
                self, T, P, loading_rate, force_max, force_min, force_step,
                method, verbose)
        if self.spring_constant == 0.:
            dpdf, forces = self.probability_density(
                T, P, loading_rate, force_max, force_min, force_step, method,
                verbose)
            return rupture_force_from_dpdf(dpdf, forces)
        else:
            result, forces = self.probability_density(
                T, P, loading_rate, force_max, force_min, force_step, method,
                verbose, return_probs=True)
            dpdf, probs = result[0], result[1]
            force_step = forces[1] - forces[0]
            fs_tot, forces = self.external_force(T, force_max, force_min,
                                                 force_step, probs)
            return rupture_force_from_dpdf(dpdf, fs_tot, force_step)

    def rupture_force_and_uncertainty(self, T, P, loading_rate, force_max,
                                      force_min=0., force_step=0.01,
                                      method='Gibbs', verbose=False):
        """Calculate the average rupture force and its uncertainty for a
        given loading rate. See class *Dissociation*.

        """
        if not(self.consider_back_reaction):
            assert self.intact_bond_minimum
            return Dissociation.rupture_force_and_uncertainty(
                self, T, P, loading_rate, force_max, force_min, force_step,
                method, verbose)
        if self.spring_constant == 0.:
            dpdf, forces = self.probability_density(
                T, P, loading_rate, force_max, force_min, force_step, method,
                verbose)
            return rupture_force_and_uncertainty_from_dpdf(dpdf, forces)
        else:
            result, forces = self.probability_density(
                T, P, loading_rate, force_max, force_min, force_step, method,
                verbose, return_probs=True)
            dpdf, probs = result[0], result[1]
            force_step = forces[1] - forces[0]
            fs_tot, forces = self.external_force(T, force_max, force_min,
                                                 force_step, probs)
            return rupture_force_and_uncertainty_from_dpdf(dpdf, fs_tot,
                                                           force_step)

    def get_force_limits(self, T, P, loading_rate, factor=10,
                         force_step=0.01, method='Gibbs'):
        """Determine good force limits for the calculation of the rupture
        force. See class *Dissociation*.

        """
        if self.consider_back_reaction:
            raise AttributeError('get_force_limits has not been tested ' +
                                 'with consider_back_reaction=True.')
        try:
            return Dissociation.get_force_limits(self, T, P, loading_rate,
                                                 factor, force_step, method)
        except ValueError:
            assert self.error in [1, 2, 3]
            if self.mode2d:
                if self.error == 2:
                    raise ValueError('force_step is not small enough or ' +
                                     'the maximum energy curve was not ' +
                                     'calculated far enough in the ' +
                                     'direction of smaller image numbers.')
                elif (self.error == 1) or (self.error == 3):
                    raise ValueError('force_step is not small enough, ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough or the ' +
                                     'maximum energy curve was not ' +
                                     'calculated far enough in the ' +
                                     'direction of smaller image numbers.')
            else:
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')

    def get_force_limits_gibbs(self, T, P, loading_rate, force_min, force_max,
                               factor=10, force_step=0.01):
        """Determine good force limits for the calculation of the rupture
        force with method='Gibbs'. See class *Dissociation*.

        """
        if self.consider_back_reaction:
            raise AttributeError('get_force_limits_gibbs has not ' +
                                 'been tested with ' +
                                 'consider_back_reaction=True.')
        try:
            return Dissociation.get_force_limits_gibbs(self, T, P,
                                                       loading_rate,
                                                       force_min, force_max,
                                                       factor, force_step)
        except ValueError:
            assert self.error in [1, 2, 3]
            if self.mode2d:
                if self.error == 2:
                    raise ValueError('force_step is not small enough or ' +
                                     'the maximum energy curve was not ' +
                                     'calculated far enough in the ' +
                                     'direction of smaller image numbers.')
                elif (self.error == 1) or (self.error == 3):
                    raise ValueError('force_step is not small enough, ' +
                                     'the COGEF-trajectory was not ' +
                                     'calculated far enough or the ' +
                                     'maximum energy curve was not ' +
                                     'calculated far enough in the ' +
                                     'direction of smaller image numbers.')
            else:
                raise ValueError('force_step is not small enough or ' +
                                 'the COGEF-trajectory was not ' +
                                 'calculated far enough.')

    def get_minimum_distances(self):
        """See class *Dissociation*.

        """
        if self.intact_bond_minimum:
            energies, distances = self.cogef2d.get_energy_curve(
                self.imagemin, self.imagemax, only_intact_bond_images=True,
                modulo=self.modulo)
        else:
            energies, distances = self.cogef2d.get_minimum_energy_curve(
                self.imagemin, self.imagemax, only_broken_bond_images=True,
                modulo=self.modulo)
        return distances

    def get_mean_distance(self, f_ext, T, check=True):
        """See class *Dissociation*.

        """
        if (check) and not(self.intact_bond_minimum) and \
           (self.cogef2d.last_broken_bond_image >= len(self.cogef2d.images)):
            raise ValueError("You have to set 'last_broken_bond_image' of " +
                             'the COGEF object.')
        return Dissociation.get_mean_distance(self, f_ext, T,
                                              check=self.intact_bond_minimum)

    def save_mean_distances(self, T, force_max, force_min=0., force_step=0.01,
                            fileout='dists.dat', use_spring_ref=False):
        """Save mean distances for reactant/intact-bond state and
        product/broken-bond state to a file. See class *Dissociation*.

        """
        if not(self.consider_back_reaction):
            assert self.intact_bond_minimum
            return Dissociation.save_mean_distances(self, T, force_max,
                                                    force_min, force_step,
                                                    fileout, use_spring_ref)
        intact_bond_minimum = self.intact_bond_minimum
        try:
            self.intact_bond_minimum = True
            dists_i, forces = self.get_mean_distances(
                T, force_max, force_min, force_step, use_spring_ref)
            self.intact_bond_minimum = False
            dists_b, forces = self.get_mean_distances(
                T, force_max, force_min, force_step, use_spring_ref)
            if use_spring_ref:
                distance = 'delta d'
            else:
                distance = 'distance'
            fd = open(fileout, 'w')
            if self.spring_constant == 0.:
                fd.write('Force\t' + 'Mean ' + distance + ' (intact)\t' +
                         'Mean ' + distance + ' (broken)\n')
                space = '\t'
            else:
                fd.write('Loading rate * time\t' +
                         'Mean ' + distance + ' (intact)\t' +
                         'Mean ' + distance + ' (broken)\n')
                space = '\t\t\t'
            for i in range(len(dists_i)):
                fd.write(str(round(forces[i], 10)) + space +
                         str(dists_i[i]) + '\t\t' + str(dists_b[i]) + '\n')
            fd.close()
        finally:
            self.intact_bond_minimum = intact_bond_minimum
