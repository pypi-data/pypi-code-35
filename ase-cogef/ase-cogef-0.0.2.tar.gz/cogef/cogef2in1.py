# -*- coding: utf-8 -*-

# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Similar to class COGEF2D in module cogef2d.py, thus considering two
dimensions of the Born-Oppenheimer surface but calculating the three-segments
COGEF (3S-COGEF) path directly (reactant minimum curve, transition maxium
curve and product minimum curve).

"""

import os

from ase.constraints import FixBondLengths, MirrorForce
from ase.optimize import FIRE
from ase.parallel import rank, world
from ase.io.trajectory import Trajectory

from cogef import COGEF, do_nothing


def do_nothing2in1(image, curve_type, imagenum, new_opt, get_filename):
    """Explanation of the initialization function needed for the calculation
    of the images from the 3S-COGEF path in class *COGEF2IN1*.

    This function can be used to set a cell, to set a calculator and to
    return the name of the trajectory file for the optimization.

    Parameters
    ----------
    image: Atoms object
        Configuration which has to be optimized.
    curve_type: str
        The name of the curve segment, that is 'reactant', 'transition' or
        'product'.
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


class COGEF2IN1(COGEF):
    """Efficient calculation of the 3S-COGEF path. An alternative to COGEF2D.

    O. Brügner, M. Walter, Phys. Rev. Materials 2018, 2, 113603

    Parameters
    ----------
    pullatompair: tuple of two ints
        Two atom indices where force acts on.
    breakatompair: tuple of two ints
        Two atom indices associated to the breaking bond.
    break_distance: float
        Bond is assumed to be broken when bond length reaches this value.
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
    collision_distance: float
        Bond is assumed to be imploded when bond length reaches this value.
    transition_image_shift: int
        Defines the first image of the transition maximum curve relative to
        the last image of the reactant curve (in negative direction).
    product_image_shift: int
        Defines the first image of the product minimum curve relative to the
        last image of the transition maximum curve.
    always_increase: bool
        Defines whether the bond length is increased before each optimization
        during the calculation of the transition maximum curve and product
        minimum curve. *False* means that it is increased only for the first
        image.
    placeholdernumber: int
        The number of the reactant image used as placeholder, see property
        *placeholder*.

    """
    def __init__(self, pullatompair, breakatompair, break_distance, images,
                 maximum_images=None, minimum_images=None,
                 optimizer=FIRE, fmax=0.1, optimizer_logfile='-',
                 Atoms_alternative=None, collision_distance=1.,
                 transition_image_shift=0, product_image_shift=0,
                 always_increase=False, placeholdernumber=0):
        COGEF.__init__(self, images, pullatompair[0], pullatompair[1],
                       optimizer, fmax, optimizer_logfile, Atoms_alternative)
        self.pullatompair = pullatompair
        self.breakatompair = breakatompair
        self.Atoms_alternative = Atoms_alternative
        self.initialize = None
        self.stepsize = None
        self.start = None
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
        # Always fixed d, never fixed force here
        self.fix_force_for_max_curve = False
        self.last_broken_bond_image = float("inf")
        self.break_distance = break_distance
        self.collision_distance = collision_distance
        self.transition_image_shift = transition_image_shift
        self.min_product_distance = None
        self.product_image_shift = product_image_shift
        self.distance_type = 'Bond'
        self.always_increase = always_increase

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
        Method *calc_reactant_curve* should be used here instead.

        """
        COGEF.pull(self, stepsize, steps, initialize, trajectory)
        self.maximum_images += [None] * steps
        self.minimum_images += [None] * steps

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

    def initialize_reactant(self, image, imagenum, new_opt, get_filename):
        """Initialization function for images of the reactant curve.

        This function transfers all information plus the name of the curve
        type to self.initialize, see function *do_nothing2in1*.

        Parameters and returns
        ----------     -------
        See explanation of the initialization function in cogef.py.

        """
        return self.initialize(image, 'reactant', imagenum, new_opt,
                               get_filename)

    def initialize_transition(self, image, imagenum, new_opt, get_filename):
        """Initialization function for images of the transition maximum curve.

        This function adds the MirrorForce constraint, increases the bond
        length in the first cogef step to ensure that the correct maximum
        will be found and transfers all information plus the name of the curve
        type to self.initialize, see function *do_nothing2in1*.

        Parameters and returns
        ----------     -------
        See explanation of the initialization function in cogef.py.

        """
        if get_filename:
            return self.initialize(image, 'transition', imagenum, new_opt,
                                   get_filename)
        if new_opt:
            if (self.start) or (self.always_increase):
                image_copy = image.copy()
                cogef = COGEF([], self.breakatompair[0],
                              self.breakatompair[1],
                              fixed_atom_pairs=[self.pullatompair])
                cogef.shift_atoms(image_copy, self.stepsize)
                image.positions = image_copy.positions
            con2 = image.constraints[0]
        else:
            assert str(image.constraints[0].__class__) == \
                'ase.constraints.MirrorForce'
            con2 = image.constraints[1]
        con1 = MirrorForce(self.breakatompair[0], self.breakatompair[1],
                           self.break_distance, self.collision_distance,
                           fmax=self.fmax)
        assert isinstance(con2, FixBondLengths)
        image.set_constraint([con1, con2])
        return self.initialize(image, 'transition', imagenum, new_opt,
                               get_filename)

    def initialize_product(self, image, imagenum, new_opt, get_filename):
        """Initialization function for images of the product minimum curve.

        This function increases the bond length in the first cogef step to
        ensure that the correct minimum will be found and transfers all
        information plus the name of the curve type to self.initialize,
        see function *do_nothing2in1*.

        Parameters and returns
        ----------     -------
        See explanation of the initialization function in cogef.py.

        """
        if get_filename:
            return self.initialize(image, 'product', imagenum, new_opt,
                                   get_filename)
        if new_opt:
            if (self.start) or (self.always_increase):
                image_copy = image.copy()
                cogef = COGEF([], self.breakatompair[0],
                              self.breakatompair[1],
                              fixed_atom_pairs=[self.pullatompair])
                cogef.shift_atoms(image_copy, self.stepsize)
                image.positions = image_copy.positions
        return self.initialize(image, 'product', imagenum, new_opt,
                               get_filename)

    def calc_reactant_curve(self, stepsize, initialize=do_nothing2in1,
                            trajectory='pull/pull.traj'):
        """Obtain the reactant curve up to bond breaking.

        The pulling process can be limitated by *self.last_intact_bond_image*.

        Parameters
        ----------
        stepsize: float
            Step size used.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing2in1*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.

        """
        dirname = os.path.dirname(trajectory)
        if (rank == 0) and not(os.path.isdir(dirname)):
            os.mkdir(dirname)
        self.initialize = initialize
        while (self.get_break_distance(self.images[-1]) <
               self.break_distance) and \
              (len(self.images) <= self.last_intact_bond_image + 1):
            self.pull(stepsize, 1, self.initialize_reactant, trajectory)

    def calc_transition_curve(self, stepsize, initialize=do_nothing2in1,
                              trajectory1='pull_max/press.traj',
                              trajectory2='pull_max.traj'):
        """Obtain the transition maximum curve.

        Starting from the reactant curve just before bond
        breaking and calculating the transition maximum curve by decreasing
        the distance and mirroring the forces along the bond.

        Parameters
        ----------
        stepsize: float
            Step size used.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing2in1*.
        trajectory1: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.
        trajectory2: str
            Name of the trajectory file where the images of the COGEF path
            will be saved in the order of the reactant image numbers.
            *self.placeholder* will be used as placeholder if
            not all maximum images are calculated.

        """
        dirname = os.path.dirname(trajectory1)
        if (rank == 0) and not(os.path.isdir(dirname)):
            os.mkdir(dirname)
        self.initialize = initialize
        self.stepsize = stepsize
        last_index = None
        for i in range(len(self.images))[::-1]:
            if self.get_break_distance(self.images[i]) < self.break_distance:
                last_index = i
                break
        if last_index < self.last_intact_bond_image:
            self.set_last_intact_bond_image(last_index)
        else:
            last_index = self.last_intact_bond_image
        last_index -= self.transition_image_shift
        if os.path.isfile(trajectory1):
            images = trajectory1
        else:
            assert (self.get_break_distance(self.images[-1]) >=
                    self.break_distance) or \
                   (len(self.images) > self.last_intact_bond_image + 1), \
                'Reactant curve must be calculated first.'
            # Go to last intact-bond image
            i = last_index
            assert self.get_break_distance(self.images[i]) < \
                self.break_distance
            images = [self.images[i]]
        cogef = COGEF(images, self.pullatompair[0], self.pullatompair[1],
                      optimizer=self.optimizer, fmax=self.fmax,
                      Atoms_alternative=self.Atoms_alternative)
        world.barrier()
        self.maximum_images = [None] * len(self.maximum_images)
        for j in range(self.transition_image_shift):
            i = last_index + j + 1
            self.maximum_images[i] = self.images[i]
        for j, img in enumerate(cogef.images):
            i = last_index - j
            if self.get_break_distance(img) < self.break_distance:
                if i < 0:
                    if trajectory2 is not None:
                        self.save_maximum_curve(trajectory2)
                    raise RuntimeError('Negative transition state image ' +
                                       'number reached. Image numbers of ' +
                                       'reactant curve must be shifted.')
                self.maximum_images[i] = img
        if trajectory2 is not None:
            self.save_maximum_curve(trajectory2)
        while self.get_break_distance(cogef.images[-1]) < self.break_distance:
            assert self.get_break_distance(cogef.images[-1]) > \
                self.collision_distance, \
                self.distance_type + ' is too small. Cannot find ' + \
                'transition curve. It may help to increase ' + \
                "'transition_image_shift' but you must remove " + \
                'or rename the old transition curve data first.'
            self.start = (len(cogef.images) == 1)
            cogef.pull(-stepsize, 1, self.initialize_transition, trajectory1)
            if self.get_break_distance(cogef.images[-1]) < \
               self.break_distance:
                i = last_index - len(cogef.images) + 1
                if i < 0:
                    if trajectory2 is not None:
                        self.save_maximum_curve(trajectory2)
                    raise RuntimeError('Negative transition state image ' +
                                       'number reached. Image numbers of ' +
                                       'reactant curve must be shifted.')
                self.maximum_images[i] = cogef.images[-1]
                if trajectory2 is not None:
                    self.save_maximum_curve(trajectory2)

    def calc_product_curve(self, stepsize, initialize=do_nothing2in1,
                           trajectory1='pull_min/pull.traj',
                           trajectory2='pull_min.traj',
                           uptoimgnum=None,
                           reactant_trajectory='pull/pull.traj'):
        """Obtain the product minimum curve.

        Starting from the transition maximum curve just before bond breaks
        completely and calculating the product minimum curve by increasing the
        distance again.

        Parameters
        ----------
        stepsize: float
            Step size used.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing2in1*.
        trajectory1: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.
        trajectory2: str
            Name of the trajectory file where the images of the COGEF path
            will be saved in the order of the reactant image numbers.
            *self.placeholder* will be used as placeholder if
            not all product minimum images are calculated.
        uptoimgnum: int (optional)
            The product minimum curve is calculated up to image
            number *uptoimgnum* or up to the maximum image number of the
            reactant curve if it is *None*.
        reactant_trajectory: str
            Name of the trajectory file where the images of the reactant
            curve will be saved. This must be set if *uptoimgnum* is not
            *None*.

        """
        dirname = os.path.dirname(trajectory1)
        if (rank == 0) and not(os.path.isdir(dirname)):
            os.mkdir(dirname)
        self.initialize = initialize
        self.stepsize = stepsize
        max_dists = [self.get_break_distance(image)
                     for image in self.maximum_images if image is not None]
        self.min_product_distance = max(max_dists[self.product_image_shift:])
        first_index = None
        first_image = None
        for i, img in enumerate(self.maximum_images):
            if img is not None:
                first_index = i
                first_image = img
                break
        first_index += self.product_image_shift
        if os.path.isfile(trajectory1):
            images = trajectory1
        else:
            assert first_image is not None, \
                'Reactant and transition curve must be calculated first.'
            # Go to last almost-intact-bond image
            i = first_index
            assert self.get_break_distance(self.maximum_images[i]) < \
                self.break_distance
            images = [self.maximum_images[i]]
        cogef = COGEF(images, self.pullatompair[0], self.pullatompair[1],
                      optimizer=self.optimizer, fmax=self.fmax,
                      Atoms_alternative=self.Atoms_alternative)
        world.barrier()
        self.minimum_images = [None] * len(self.minimum_images)
        for j in range(self.product_image_shift):
            i = first_index - j - 1
            self.minimum_images[i] = self.maximum_images[i]
        for j, img in enumerate(cogef.images):
            i = first_index + j
            self.check_product_distance(img)
            self.minimum_images[i] = img
        if trajectory2 is not None:
            self.save_minimum_curve(trajectory2)
        if uptoimgnum is None:
            uptoimgnum = len(self.images) - 1
        while first_index + len(cogef.images) <= uptoimgnum:
            self.start = (len(cogef.images) == 1)
            cogef.pull(stepsize, 1, self.initialize_product, trajectory1)
            self.check_product_distance(cogef.images[-1])
            i = first_index + len(cogef.images) - 1
            if i >= len(self.images):
                # Reactant trajectory should contain the complete image range
                self.images += [cogef.images[-1]]
                self.maximum_images += [None]
                self.minimum_images += [None]
                self.save_reactant_curve(reactant_trajectory)
            self.minimum_images[i] = cogef.images[-1]
            if trajectory2 is not None:
                self.save_minimum_curve(trajectory2)

    def check_product_distance(self, image):
        """Check whether product minimum image is ok.

        If the bond length is too small, it cannot be a product state.

        Parameters
        ----------
        image: Atoms object
            The product image under investigation.

        """
        if self.get_break_distance(image) < self.min_product_distance:
            raise RuntimeError('Bond length is too small. Cannot find ' +
                               'product curve. It may help to increase ' +
                               "'product_image_shift' but you must remove " +
                               'or rename the old product curve data first.')

    def save_reactant_curve(self, trajectory):
        """Save reactant curve.

        Parameters
        ----------
        trajectory: str
            Filename of the trajectory.

        """
        traj = Trajectory(trajectory, 'w')
        for img in self.images:
            img.set_constraint()
            traj.write(img)
        traj.close()
        world.barrier()

    def save_maximum_curve(self, trajectory):
        """Save maximum curve in the same order as the reactant curve.

        Parameters
        ----------
        trajectory: str
            Filename of the trajectory.

        """
        traj = Trajectory(trajectory, 'w')
        for img in self.maximum_images:
            if img is not None:
                img.set_constraint()
                traj.write(img)
            else:
                traj.write(self.placeholder)  # Placeholder
        traj.close()
        world.barrier()

    def save_minimum_curve(self, trajectory):
        """Save product minimum curve in the same order as the reactant curve.

        Parameters
        ----------
        trajectory: str
            Filename of the trajectory.

        """
        traj = Trajectory(trajectory, 'w')
        for img in self.minimum_images:
            if img is not None:
                img.set_constraint()
                traj.write(img)
            else:
                traj.write(self.placeholder)  # Placeholder
        traj.close()
        world.barrier()

    def calc_all(self, stepsize, initialize=do_nothing2in1,
                 reactant_trajectory='pull/pull.traj',
                 transition_trajectory1='pull_max/press.traj',
                 transition_trajectory2='pull_max.traj',
                 product_trajectory1='pull_min/pull.traj',
                 product_trajectory2='pull_min.traj',
                 uptoimgnum=None):
        """Calculate the 3S-COGEF path.

        Calculate the reactant minimum, transition maximum and product minimum
        curves.

        stepsize: float
            Step size used.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing2in1*.
        reactant_trajectory: str
            Name of the trajectory file where the images of the reactant
            curve will be saved.
        transition_trajectory1: str
            Name of the trajectory file where the images of the transition
            maximum curve will be saved.
        transition_trajectory2: str
            Name of the trajectory file where the images of the transition
            maximum curve will be saved in the order of the reactant image
            numbers. *self.placeholder* will be used as placeholder if
            not all transition maximum images are calculated.
        product_trajectory1: str
            Name of the trajectory file where the images of the product
            minimum curve will be saved.
        product_trajectory2: str
            Name of the trajectory file where the images of the product
            minimum curve will be saved in the order of the reactant image
            numbers. *self.placeholder* will be used as placeholder if
            not all product maximum images are calculated.
        uptoimgnum: int (optional)
            The product minimum curve is calculated up to image
            number *uptoimgnum* or up to the maximum image number of the
            reactant curve if it is *None*.

        """
        self.calc_reactant_curve(stepsize, initialize, reactant_trajectory)
        self.calc_transition_curve(stepsize, initialize,
                                   transition_trajectory1,
                                   transition_trajectory2)
        self.calc_product_curve(stepsize, initialize, product_trajectory1,
                                product_trajectory2, uptoimgnum,
                                reactant_trajectory)

    def get_maximum_energy_curve(self, imagemin=0, imagemax=-1, modulo=1):
        """Return the energy values and associated distances of the
        transition maximum curve.

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
