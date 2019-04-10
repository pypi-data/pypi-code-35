# -*- coding: utf-8 -*-

# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Similar to class COGEF in module cogef.py but considering two dimensions
of the Born-Oppenheimer surface.

"""

import os
import sys

from ase.constraints import FixBondLengths, ExternalForce
from ase.optimize import FIRE
from ase.parallel import world, rank
from ase.io.trajectory import Trajectory

from cogef import COGEF, do_nothing


def do_nothing2d(image, directory, imagenum, new_opt, get_filename):
    """Explanation of the initialization function needed for method
    *calc_maximum_curve* in class *COGEF2D*.

    This function can be used to set a cell, to set a calculator and to
    return the name of the trajectory file for the optimization.

    Parameters
    ----------
    image: Atoms object
        Configuration which has to be optimized.
    directory: str
        Path of the directory where output files of the optimization should
        be saved.
    imagenum: int
        Image number that can be added to the name of the trajectory file.
    new_opt: bool
        Is *True* if it is a new optimization and not the restart of a
        canceled optimization. For instance, the cell need only to be set if
        *new_opt* is *True*.
    get_filename: bool
        Just return trajectory name if *get_filename* is *True*.

    Returns
    -------
    result: str or None
        Return the name of the trajectory file only if *get_filename* is
        *True*. Add 'new forces:' in front of the file name for
        recalculating forces even if an optimization file already exists and
        seems to be converged. This can be
        useful after the change of some parameters of the calculator.
        Return 'Finished' to cancel the calculation of the COGEF path.

    """
    return None


def get_first_maximum(values, tolerance):
    """ Find the first maximum.

    Return first value from list *values* for which the next values
    decrease by more than *tolerance* or return None when no maximum can be
    identified. Restart searching after a value which is None.

    Parameters
    ----------
    values: list of float
    tolerance: float

    Returns
    -------
    result: float or None

    """
    valuemax = None
    for value in values:
        if value is None:
            valuemax = None
            continue
        if (valuemax is None) or (value > valuemax):
            valuemax = value
        else:
            if valuemax > value + tolerance:
                return valuemax
    return None


def get_first_minimum(values, tolerance):
    """Find the first minimum.

    Return first value from list *values* for which the next values
    increase by more than *tolerance* or return None when no maximum can be
    identified. Restart searching after a value which is None.

    Parameters
    ----------
    values: list of float
    tolerance: float

    Returns
    -------
    result: float or None

    """
    valuemin = None
    for value in values:
        if value is None:
            valuemin = None
            continue
        if (valuemin is None) or (value < valuemin):
            valuemin = value
        else:
            if valuemin < value - tolerance:
                return valuemin
    return None


class COGEF2D(COGEF):
    """COnstraint GEometry to simulate Forces (COGEF) in two dimensions.

    This class can be used to calculate 3S-COGEF paths as explained here:
    O. Brügner, M. Walter, Phys. Rev. Materials 2018, 2, 113603

    Pull two atoms apart or press two atoms together. In addition to class
    COGEF (1S-COGEF), these methods from here can be used to simulate the
    influence of the thermal motion on a given bond (3S-COGEF).
    The first segment of the 3S-COGEF path obtained here (reactant curve)
    is the 1S-COGEF path which can also be obtained from
    class COGEF and contains reactant states in dependence of the external
    force. The second segment of the 3S-COGEF path (maximum curve)
    belongs to the energy curve associated to the transition states of the
    bond breaking reaction in dependence of the force.
    The third segment (product minimum curve) contains product (and
    transition) states in dependence of the force. In general, searching
    transition states on the 3S-COGEF path is more accurate compared to the
    1S-COGEF path as two dimensions of the BO-surface are considered in the
    former. 3S-COGEF also allows to address different bonds for the bond
    breaking reaction in order to compare their acivation energies
    (see class Dissociation2d). Product states which can be obtained here
    (in contrast to class COGEF) can be used to get activation energies for
    the back reaction.

    Parameters
    ----------
    pullatompair: tuple of two ints
        Two atom indices where force acts on.
    breakatompair: tuple of two ints
        Two atom indices associated to the breaking bond.
    images: str or list of Atoms objects
        Initial trajectory of the reactant (minimum) curve or its filename
        (minima with intact bond).
    maximum_images: str or list of Atoms objects (optional)
        Initial trajectory of the (transition) maximum curve or its filename.
    minimum_images: str or list of Atoms objects (optional)
        Initial trajectory of the product minimum curve or its filename
        (minima with broken bond).
    optimizer: Optimizer object
        Used optimizer.
    fmax: float
        Maximum force for optimization.
    optimizer_logfile: file object or str
        If *optimizer_logfile* is a string, a file with that name will be
        opened. Use '-' for stdout.
    Atoms_alternative: class
        Alternative to class Atoms which should be used.
    max_image_number: int
        Maximum number of images for variation of the breaking bond length
    fix_force_for_max_curve: bool
        Defines the additional constraint during variation of the breaking
        bond length. Use *True* to fix the external force, use *False* to
        fix the distance between the atoms where force acts on. These are two
        different procedures in order to find the maximum curve (and the
        product minimum curve).
    placeholdernumber: int
        The number of the reactant image used as placeholder, see property
        *placeholder*.

    """
    def __init__(self, pullatompair, breakatompair, images,
                 maximum_images=None, minimum_images=None,
                 optimizer=FIRE, fmax=0.1, optimizer_logfile='-',
                 Atoms_alternative=None, max_image_number=20,
                 fix_force_for_max_curve=True, placeholdernumber=0):
        COGEF.__init__(self, images, pullatompair[0], pullatompair[1],
                       optimizer, fmax, optimizer_logfile, Atoms_alternative)
        self.pullatompair = pullatompair
        self.breakatompair = breakatompair
        self.Atoms_alternative = Atoms_alternative
        self.initialize2d = None
        self.directory = None
        self.placeholdernumber = placeholdernumber
        self.maximum_images = [None] * len(self.images)
        if maximum_images:
            cogef = COGEF(maximum_images, 0, 1,
                          Atoms_alternative=Atoms_alternative)
            for i, max_image in enumerate(cogef.images):
                # Don't consider placeholder
                if max_image != self.placeholder:
                    self.maximum_images[i] = max_image
        self.minimum_images = [None] * len(self.images)
        if minimum_images:
            cogef = COGEF(minimum_images, 0, 1,
                          Atoms_alternative=Atoms_alternative)
            for i, min_image in enumerate(cogef.images):
                # Don't consider placeholder
                if min_image != self.placeholder:
                    self.minimum_images[i] = min_image
        self.max_image_number = max_image_number
        self.fix_force_for_max_curve = fix_force_for_max_curve
        self.f_ext = None
        self.last_broken_bond_image = float("inf")

    @property
    def placeholder(self):
        """Return a configuration standing for an empty image in all
        trajectories except of the reactant curve.

        It may be an image of the reactant curve.

        Returns
        -------
        result: Atoms object

        """
        return self.images[self.placeholdernumber]

    def set_last_broken_bond_image(self, last_broken_bond_image):
        """ Set the index of the last product (broken bond) image.

        From a certain image on, the product minimum trajectory can contain
        images which do not belong anymore to the product of the current but to
        the product of a new transition indicated by energy release.
        In this case, you must set
        the last image number which still belongs to the current
        transition to prevent wrong results.

        Parameters
        ----------
        last_broken_bond_image: int

        """
        self.last_broken_bond_image = last_broken_bond_image

    def pull(self, stepsize, steps, initialize=do_nothing,
             trajectory='pull.traj'):
        """Obtain the reactant curve. See class COGEF.

        """
        COGEF.pull(self, stepsize, steps, initialize, trajectory)
        self.maximum_images += [None] * steps
        self.minimum_images += [None] * steps

    def initialize(self, image, imagenum, new_opt, get_filename):
        """Initialization function for variation of the breaking bond length.

        This function adds the external force constraint if
        *self.fix_force_for_max_curve* is *True* and transfers all information
        plus the directory name to self.initialize2d, see function
        *do_nothing2d*.

        Parameters and returns
        ----------     -------
        See explanation of the initialization function in cogef.py.

        """
        if get_filename:
            return self.initialize2d(image, self.directory, imagenum, new_opt,
                                     get_filename)
        if self.fix_force_for_max_curve:
            if new_opt:
                con1 = ExternalForce(self.pullatompair[0],
                                     self.pullatompair[1], self.f_ext)
                con2 = image.constraints[0]
                assert isinstance(con2, FixBondLengths)
                image.set_constraint([con1, con2])
            else:
                assert str(image.constraints[0].__class__) == \
                    'ase.constraints.ExternalForce'
                assert isinstance(image.constraints[1], FixBondLengths)
        return self.initialize2d(image, self.directory, imagenum, new_opt,
                                 get_filename)

    def initialize_bbm(self, image, imagenum, new_opt, get_filename):
        """Initialization function for reoptimization of a product/
        broken-bond minimum (bbm) without fixing of the breaking bond length.

        This is similar to method *initialize*. The trajectory will be saved
        in directory 'bbm'.

        Parameters and returns
        ----------     -------
        See explanation of the initialization function in cogef.py.

        """
        directory = os.path.join(self.directory, 'bbm')
        if get_filename:
            return self.initialize2d(image, directory, imagenum,
                                     new_opt=False, get_filename=get_filename)
        if self.fix_force_for_max_curve:
            if new_opt:
                con = ExternalForce(self.pullatompair[0],
                                    self.pullatompair[1], self.f_ext)
                image.set_constraint(con)
            else:
                assert str(image.constraints[0].__class__) == \
                    'ase.constraints.ExternalForce'
        # 'new_opt' is set to false to reduce calculation time
        # because otherwise the cell would be renewed
        return self.initialize2d(image, directory, imagenum, new_opt=False,
                                 get_filename=get_filename)

    def get_break_cogef(self, images):
        """Get the cogef object for pulling the atoms with indices
        *self.breakatompair* apart.

        Parameters
        ----------
        images: str or list of Atoms objects
            Initial trajectory or its filename.

        Returns
        -------
        result: COGEF object

        """
        return COGEF(images, self.breakatompair[0], self.breakatompair[1],
                     optimizer=self.optimizer, fmax=self.fmax,
                     Atoms_alternative=self.Atoms_alternative)

    def optimize_bbm(self, image, imagenum):
        """Optimize product/broken-bond minimum.

        Parameters
        ----------
        images: Atoms object
            Initial configuration for optimization.
        imagenum: int
            Image number.

        Returns
        -------
        result: Atoms object
            Optimized configuration.

        """
        directory = os.path.join(self.directory, 'bbm')
        if (rank == 0) and not(os.path.isdir(directory)):
            os.mkdir(directory)
        world.barrier()
        cogef = self.get_break_cogef([image] * imagenum)
        if not(self.fix_force_for_max_curve):
            cogef.set_fixed_atom_pairs([self.pullatompair])
        cogef.pull(None, 1, self.initialize_bbm, trajectory=None)
        return cogef.images[imagenum]

    def calc_maximum_curve(self, imageindices, stepsize,
                           energy_tolerance=0.01, initialize2d=do_nothing2d,
                           max_trajectory='pull_max.traj',
                           breakdirectory='pull', breaktrajectory='pull.traj',
                           and_minimum_curve=False,
                           min_trajectory='pull_min.traj', use_image=None,
                           only_minimum_curve=False):
        """Calculate maximum curve and/or product minimum curve by variation
        of the breaking bond length.

        The bond lengths are varied until all requested extrema are found or
        the maximum number *self.max_image_number* is reached. Problems in
        finding extrema lead to error messages.

        imageindices: list of int
            The variation of the breaking bond is started at the reactant
            minima with indices *imageindices*.
        stepsize: float
            Step size of bond length steps.
        energy_tolerance: float
            This tolerance must be exceeded that an extremum in energy is
            identified.
        initialize2d: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing2d*.
        max_trajectory: str
            Name of the trajectory file where the images of the maximum curve
            will be saved in the order of the reactant image numbers.
            *self.placeholder* will be used as placeholder if
            not all maximum images are calculated.
        breakdirectory: str
            A directory with name *breakdirectory + _ + 'image index'* will
            be created for each of the indices in *imageindices*.
        breaktrajectory: str
            Name of the trajectory file for the variation of the breaking
            bond length. This file is save into the corresponding directory,
            see *breakdirectory*.
        and_minimum_curve: bool
            Product minimum curve will also be obtained if it is *True*.
        min_trajectory: str
            Name of the trajectory file where the images of the product
            minimum curve will be saved in the order of the reactant image
            numbers. *self.placeholder* will be used as
            placeholder if not all product minimum images are calculated.
        use_image: bool
            Set *use_image* to an image number for which
            the maximum image was already calculated if you want that this
            maximum image should be used as initial structure for the search
            process of the new maximum images. This can reduce the computing
            time. But it could lead to gaps in *breaktrajectory*.
            *self.placeholder* will be used as placeholder then.
        only_minimum_curve: bool
            No maximum curve will be obtained if it is *True*.

        """
        if only_minimum_curve:
            and_minimum_curve = True
        if (use_image is None) and (only_minimum_curve):
            raise ValueError('If use_image is not set, ' +
                             'only_minimum_curve must be set to False ' +
                             'because maximum must be calculated ' +
                             'first and the minimum later.')
        self.initialize2d = initialize2d
        for i in imageindices:
            assert i >= 0, \
                'Only image numbers larger or equal to zero are allowed.'
            if rank == 0:
                sys.stdout.write('\n' + 'Get image ' + str(i))
                if not(only_minimum_curve):
                    sys.stdout.write(' maximum')
                    if and_minimum_curve:
                        sys.stdout.write(' and')
                if and_minimum_curve:
                    sys.stdout.write(' product minimum')
                sys.stdout.write('\n\n')
            if self.fix_force_for_max_curve:
                self.f_ext = self.constraint_force(i)
                self.directory = breakdirectory + '_' + str(i)
            else:
                self.directory = breakdirectory + '_d_' + str(i)
            if (rank == 0) and not(os.path.isdir(self.directory)):
                os.mkdir(self.directory)
            world.barrier()
            if breaktrajectory is None:
                breaktraj = None
                atoms = self.images[i]
                cogef = self.get_break_cogef([atoms])
            else:
                breaktraj = os.path.join(self.directory, breaktrajectory)
                try:
                    cogef = self.get_break_cogef(breaktraj)
                except IOError:
                    atoms = self.images[i]
                    cogef = self.get_break_cogef([atoms])
            is_maxs = []
            if not(only_minimum_curve):
                # Get maximum
                is_maxs.append(True)
            if and_minimum_curve:
                # Get product/broken-bond minimum
                is_maxs.append(False)
            for is_maximum in is_maxs:
                if use_image:
                    cogef, found_min = self._use_image(cogef, use_image, i,
                                                       stepsize,
                                                       energy_tolerance,
                                                       maximum=is_maximum)
                else:
                    found_min = False
                if not(self.fix_force_for_max_curve):
                    cogef.set_fixed_atom_pairs([self.pullatompair])
                for img in cogef.images:
                    if self.fix_force_for_max_curve:
                        con = ExternalForce(self.pullatompair[0],
                                            self.pullatompair[1], self.f_ext)
                    else:
                        con = None
                    img.set_constraint(con)
                engs = [img.get_potential_energy() for img in cogef.images]
                for j, img in enumerate(cogef.images):
                    if img == self.placeholder:
                        # Placeholder
                        engs[j] = None
                engs, emax, emin = self.check_energies(
                    engs, energy_tolerance, i, is_maximum, found_min)
                for j in range(len(cogef.images), self.max_image_number):
                    if (is_maximum) and (emax is not None) or \
                       not(is_maximum) and (emin is not None):
                        break
                    if cogef.pull(stepsize, 1, self.initialize,
                                  breaktraj) == 'Canceled':
                        break
                    engs.append(cogef.images[-1].get_potential_energy())
                    if is_maximum:
                        emax = get_first_maximum(engs, energy_tolerance)
                    else:
                        emin = get_first_minimum(engs, energy_tolerance)
                else:
                    if (is_maximum) and (emax is None):
                        if breaktraj is None:
                            raise ValueError('Cannot find energy maximum. ' +
                                             'Maximum image number is too ' +
                                             'small or energy_tolerance ' +
                                             'is too small.')
                        else:
                            raise ValueError('Cannot find energy maximum. ' +
                                             'Maximum image number is too ' +
                                             'small or energy_tolerance ' +
                                             'is too large or too small. ' +
                                             'If you want to ' +
                                             'increase energy_tolerance, ' +
                                             'remove ' + breaktraj +
                                             ' first.')
                    if not(is_maximum) and (emin is None):
                        raise ValueError('Cannot find energy minimum. ' +
                                         'Maximum image number is too small.')
                if is_maximum:
                    self.maximum_images[i] = cogef.images[engs.index(emax)]
                else:
                    engs = [img.get_potential_energy()
                            for img in cogef.images]
                    imagenum = engs.index(emin)
                    if imagenum == 0:
                        image = cogef.images[0]
                    else:
                        image = self.optimize_bbm(cogef.images[imagenum],
                                                  imagenum)
                        if self.maximum_images[i] is not None:
                            self.check_broken_bond_images(i, image, stepsize)
                    self.minimum_images[i] = image
            # Save trajectories
            imgtraj = []
            if not(only_minimum_curve):
                imgtraj.append((self.maximum_images, max_trajectory))
            if and_minimum_curve:
                imgtraj.append((self.minimum_images, min_trajectory))
            for images, trajectory in imgtraj:
                if trajectory is None:
                    continue
                # Trajectory cannot save different constraints for
                # different images, therefore remove the constraint
                images[i].set_constraint()
                traj = Trajectory(trajectory, 'w')
                for img in images:
                    if img:
                        traj.write(img)
                    else:
                        traj.write(self.placeholder)  # Placeholder
                traj.close()
            # Output
            if rank == 0:
                sys.stdout.write('\n' + 'Image ' + str(i) + ':\n')
                if not(only_minimum_curve):
                    sys.stdout.write('Emax = ' +
                                     str(self.maximum_images[i].
                                         get_potential_energy()) +
                                     ' eV')
                    if self.fix_force_for_max_curve:
                        sys.stdout.write(', Emax-F*d = ' + str(emax) + ' eV')
                    sys.stdout.write('\n')
                if and_minimum_curve:
                    sys.stdout.write('Emin = ' +
                                     str(self.minimum_images[i].
                                         get_potential_energy()) +
                                     ' eV')
                    if self.fix_force_for_max_curve:
                        sys.stdout.write(', Emin-F*d = ' + str(emin) + ' eV')
                    sys.stdout.write('\n')
                sys.stdout.write('\n')

    def check_energies(self, engs, energy_tolerance, i, is_maximum,
                       found_min):
        """Check energies of the existing images and check used parameters.

        Search for energy maximum or minimum in 'engs' and check, if
        necessary, whether 'engs' is suitable in order to find the minimum by
        calculating further energy values.


        Parameters
        ----------
        engs: list of float and None
            Energies of exisiting images. Contains None for gaps.
        energy_tolerance: float
            This tolerance must be exceeded that an extremum in energy is
            identified.
        i: int
            Image number of the corresponding reactant image.
        is_maximum: bool
            Maximum must be found if it is *True*, otherwise a minimum must be
            found.
        found_min: bool
            There is a known minimum at larger bond lengths if it is *True*.

        Returns
        -------
        engs: list of float and None
            Initial energies for finding the extrema.
        emax: float or None
            Energy of the maximum if already identified.
        emin: float or None
            Energy of the product minimum if already identified.

        """
        emax = get_first_maximum(engs, energy_tolerance)
        emin = None
        if not(is_maximum):
            if emax is None:
                if i <= self.last_intact_bond_image:
                    if (len(engs) == 1) or \
                       (get_first_maximum(engs, 0.) is not None) and \
                       not(found_min):
                        raise ValueError(
                            'Cannot identify broken-bond ' +
                            'minimum. energy_tolerance is ' +
                            'too large or image ' + str(i) +
                            ' is not in the range in ' +
                            'which a barrier can be ' +
                            'found. Perhaps you can ' +
                            'prevent this error message ' +
                            'if you use the function ' +
                            "'set_last_intact_bond_image'.")
                    if not(found_min):
                        raise RuntimeError(
                            'Cannot identify broken-bond ' +
                            'minimum of image ' + str(i) +
                            '. The maximum of this image ' +
                            'must be searched first.')
            else:
                engs = engs[engs.index(emax):]
            if (len(engs) > 1) and (found_min):
                # To prevent errors if only the
                # product/broken-bond minimum shall be calculated
                engs = engs[-1:]
            emin = get_first_minimum(engs, energy_tolerance)
            if emin is not None:
                j = engs.index(emin)
                if (len(engs) > j + 1) and (engs[j + 1] is None):
                    raise RuntimeError('Something wrong with the ' +
                                       'found minimum.')
        return engs, emax, emin

    def check_broken_bond_images(self, i, broken_bond_image, stepsize):
        """Check whether product/broken-bond minimum image is ok.

        Parameters
        ----------
        i: int
            Image number of the corresponding reactant image.
        broken_bond_image: Atoms object
            The product image under investigation.
        stepsize: float
            Defines the tolerance. Product image is not ok if the breaking
            bond length is smaller than that of the corresponging maximum
            image minus this tolerance.

        """
        maximum_image = self.maximum_images[i]
        if self.get_break_distance(broken_bond_image) < \
           self.get_break_distance(maximum_image) - stepsize:
            raise RuntimeError(
                'Found wrong product/broken-bond image (' + str(i) +
                '). Bond length is smaller than that of the ' +
                'maximum image.')

    def get_break_distance(self, atoms):
        """Get the distance between the atoms of the breaking bond.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: float

        """
        return atoms.get_distance(self.breakatompair[0],
                                  self.breakatompair[1])

    def get_break_atoms(self):
        """Get atoms which are involved in the calculation of the
        break-coordinate.

        This method can be modified for classes which inherite by COGEF2D.

        Returns
        -------
        result: list of tuple of two ints
            If there are more than two atoms, write it like this:
            >>> return [(1, 2), (3, 4), (5, 6)]
            if atom indices 1 to 6 are involved.

        """
        return [self.breakatompair]

    def get_break_imagenum(self, dist, dist0, stepsize):
        """Get the next image number associated to a given breaking bond
        length by variation of this bond length.

        Parameters
        ----------
        dist: float
            Bond length for which image number is needed.
        dist0: float
            Bond length from the corresponding reactant configuration.
        stepsize: float
            Step size defining the image numbers.

        Returns
        -------
        result: int

        """
        imagenum = int(round((dist - dist0) / stepsize + 0.5))
        if imagenum < 0:
            imagenum = 0
        return imagenum

    def shift_pull_atoms(self, use_atoms, shift_d):
        """Fix the breaking bond length and pull the atoms apart where
        force acts on.

        Parameters
        ----------
        use_atoms: Atoms object
            The configuration under modification.
        shift_d: float
            Total increase of distance.

        """
        cogef = COGEF([], self.pullatompair[0], self.pullatompair[1],
                      fixed_atom_pairs=self.get_break_atoms())
        cogef.shift_atoms(use_atoms, shift_d)

    def _use_image(self, cogef, use_image_num, get_image_num, stepsize,
                   energy_tolerance, maximum=True):
        """Search ideal start position for finding a certain extremum
        somewhere in the COGEF path for variation of the breaking bond.

        The configuration of this start position is obtained from another
        configuration with different distance between the atoms where the
        force acts on.

        Parameters
        ----------
        cogef: COGEF object
            COGEF path for variation of the breaking bond.
        use_image_num: int
            Image number with respect to the corresponding reactant image
            of the other configuration used in order to obtain the start
            position.
        get_image_num: int
            Image number with respect to the corresponding reactant image
            of the wanted configuration.
        stepsize: float
            Step size of bond length steps.
        energy_tolerance: float
            This tolerance must be exceeded that an extremum in energy is
            identified.
        maximum: bool
            Maximum must be found if it is *True*, otherwise a minimum must be
            found.

        Returns
        -------
        result 1: COGEF object
            Initialized COGEF path for variation of the breaking bond and
            for finding the extremum.
        result 2: bool
            Is *True* if and only if the extremum was already found.

        """
        if not(self.fix_force_for_max_curve):
            assert abs(use_image_num - get_image_num) == 1
        atoms = self.images[get_image_num]
        dist = self.get_break_distance(atoms)
        pull_dist = self.get_distance(atoms)
        if maximum:
            use_atoms = self.maximum_images[use_image_num].copy()
        else:
            use_atoms = self.minimum_images[use_image_num].copy()
        if use_atoms is None:
            if maximum:
                raise ValueError('Cannot find maximum image with number ' +
                                 str(use_image_num) + '.')
            else:
                raise ValueError('Cannot find minimum image with number ' +
                                 str(use_image_num) + '.')
        use_atoms_dist = self.get_break_distance(use_atoms)
        use_atoms_pull_dist = self.get_distance(use_atoms)
        imagenum = self.get_break_imagenum(use_atoms_dist, dist, stepsize)
        use_dist = dist + imagenum * stepsize
        emaxmin = None
        if (len(cogef.images) <= imagenum) or \
           (cogef.images[imagenum] == self.placeholder):
            # Add *use_atoms* with shifted bond length or add earlier image
            shift = use_dist - use_atoms_dist
            if self.fix_force_for_max_curve:
                con = ExternalForce(self.pullatompair[0],
                                    self.pullatompair[1], self.f_ext)
            else:
                shift_d = pull_dist - use_atoms_pull_dist
                self.shift_pull_atoms(use_atoms, shift_d)
                con = None
            use_atoms.set_constraint(con)
            engs = []
            while emaxmin is None:
                if imagenum == 0:
                    if maximum:
                        # Cut all images *i >= 1* to prevent starting
                        # maximum-search behind the minimum
                        cogef = self.get_break_cogef([cogef.images[0]])
                    return cogef, emaxmin is not None
                cogef2 = self.get_break_cogef([use_atoms] * imagenum)
                if not(self.fix_force_for_max_curve):
                    cogef2.set_fixed_atom_pairs([self.pullatompair])
                cogef2.pull(shift, 1, self.initialize, trajectory=None)
                use_atoms = cogef2.images[imagenum]
                engs.append(use_atoms.get_potential_energy())
                if maximum:
                    emaxmin = get_first_maximum(engs, energy_tolerance)
                else:
                    emaxmin = get_first_minimum(engs, energy_tolerance)
                shift = -stepsize
                imagenum -= 1
            imagenum += 1
            cogef.images[0].set_constraint(con)
            cogef2.images[imagenum].set_constraint(con)
            engs = [cogef.images[0].get_potential_energy(),
                    cogef2.images[imagenum].get_potential_energy()]
            emax = get_first_maximum(engs, energy_tolerance)
            if (maximum) and (emax is not None) and (engs.index(emax) == 0):
                # Set image 0 to a placeholder image to get no problems
                # when searching for the maximum
                images_ini = [self.placeholder] + cogef.images[1:imagenum]
            else:
                images_ini = cogef.images[:imagenum]
            images = images_ini + [self.placeholder] * \
                (imagenum - len(images_ini)) + [cogef2.images[imagenum]]
            cogef = self.get_break_cogef(images)
        else:
            # Image already exists
            if maximum:
                # Cut all images *i > imagenum* to prevent starting
                # maximum-search behind the minimum
                images = cogef.images[:imagenum + 1]
                cogef = self.get_break_cogef(images)
        return cogef, emaxmin is not None

    def get_maximum_energy_curve(self, imagemin=0, imagemax=-1, modulo=1):
        """Return the energy values and associated distances of the
        maximum curve.

        Parameters
        ----------
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        modulo: int
            Set it to a larger value that less images are used, e.g.
            *modulo=2* means that every second image is used.

        Returns
        -------
        result: two list of floats
            Energies and associated distances in the order of the image
            numbers.

        """
        if imagemax < 0:
            imagemax += len(self.images)
        energies = []
        distances = []
        for i in range(imagemin, imagemax + 1):
            if i % modulo != 0:
                continue
            image = self.maximum_images[i]
            if not(image):
                continue
            energies.append(image.get_potential_energy())
            distances.append(self.get_distance(image))
        return energies, distances

    def get_minimum_energy_curve(self, imagemin=0, imagemax=-1,
                                 only_broken_bond_images=False, modulo=1):
        """Return the energy values and associated distances of the
        product minimum curve. Use method *get_energy_curve* to get the
        reactant minimum curve associated to the intact bond.

        Parameters
        ----------
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        only_broken_bond_images: bool
            *True* means that the given number of the last
            product/broken-bond image defines the upper limit of used images.
        modulo: int
            Set it to a larger value that less images are used, e.g.
            *modulo=2* means that every second image is used.

        Returns
        -------
        result: two list of floats
            Energies and associated distances in the order of the image
            numbers.

        """
        if imagemax < 0:
            imagemax += len(self.images)
        if only_broken_bond_images:
            imagemax = min(imagemax, self.last_broken_bond_image)
        energies = []
        distances = []
        for i in range(imagemin, imagemax + 1):
            if i % modulo != 0:
                continue
            image = self.minimum_images[i]
            if not(image):
                continue
            energies.append(image.get_potential_energy())
            distances.append(self.get_distance(image))
        return energies, distances
