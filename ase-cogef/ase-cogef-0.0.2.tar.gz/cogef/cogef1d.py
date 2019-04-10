# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Module for simulating forces with the COGEF
(COnstrained Geometries simulate External Force) method, where
the molecular geometry is relaxed with fixed bond length for each separation
of defined atoms (Beyer, M. K. J. Chem. Phys. 2000, 112, 7307).

"""

import os
from numpy import dot
from numpy.linalg import norm

from ase.constraints import FixBondLength, FixBondLengths
from ase.optimize import FIRE
from ase.parallel import world
from ase.io import read
from ase.io.trajectory import Trajectory
from ase.io.formats import UnknownFileTypeError


def do_nothing(image, imagenum, new_opt, get_filename, atom1, atom2, d1, d2):
    """Explanation of the initialization function needed for methods *pull*
    and *insert* in class *COGEF*.

    This function can be used to set a cell, to set a calculator and to
    return the name of the trajectory file for the optimization.
    Do not remove accidently *FixBondLength* with *set_constraint(...)*.

    Parameters
    ----------
    image: Atoms object
        Configuration which has to be optimized.
    imagenum: int
        Image number that can be added to the name of the trajectory file.
    new_opt: bool
        Is *True* if it is a new optimization and not the restart of a
        canceled optimization. For instance, the cell need only to be set if
        *new_opt* is *True*.
    get_filename: bool
        Just return trajectory name if *get_filename* is *True*.
    atom1: int (optional)
        First atom index where force acts on.
    atom2: int (optional)
        Second atom index where force acts on.
    d1: numpy array (optional)
       Last shift vector of first atom where force acts on.
    d2: numpy array (optional)
       Last shift vector of second atom where force acts on.

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


def do_nothing2(image):
    """Explanation of the finalize function for method *_pull* in class
    *COGEF*.

    Parameters
    ----------
    image: Atoms object
        Configuration after the optimization.

    """
    pass


class COGEF(object):
    """COnstraint GEometry to simulate Forces (COGEF).

    Pull two atoms apart or press two atoms together by applying the COGEF
    method.

    Beyer, M. K. J. Chem. Phys. 112 (2000) 7307

    Parameters
    ----------
    images: str or list of Atoms objects
        Initial trajectory or its filename.
    atom1: int
        First atom index where force acts on.
    atom2: int
        Second atom index where force acts on.
    optimizer: Optimizer object
        Used optimizer.
    fmax: float
        Maximum force for optimization.
    optimizer_logfile: file object or str
        If *optimizer_logfile* is a string, a file with that name will be
        opened. Use '-' for stdout.
    Atoms_alternative: class
        Alternative to class Atoms which should be used.
    fixed_atom_pairs: list of tuples of int
        Fixed Bond lengths which should be considered when atoms gets shifted
        and during optimization,
        e.g. *fixed_atom_pairs=[(1, 3), (4, 2), (10, 11)]*.

    """
    def __init__(self, images, atom1, atom2, optimizer=FIRE, fmax=0.1,
                 optimizer_logfile='-', Atoms_alternative=None,
                 fixed_atom_pairs=None):
        if isinstance(images, str):
            self.images = Trajectory(images)
        else:
            self.images = images
        # Make a list instead of a trajectory because the 'insert' method
        # is needed
        if not(Atoms_alternative):
            self.images = [image for image in self.images]
        else:
            # Use Atoms_alternative if you want e.g. Cluster objects from gpaw
            # instead of Atoms objects
            self.images = [Atoms_alternative(image) for image in self.images]
        self.atom1 = atom1
        self.atom2 = atom2
        self.optimizer = optimizer
        self.fmax = fmax
        self.optimizer_logfile = optimizer_logfile
        self.fixed_atom_pairs = None
        self.set_fixed_atom_pairs(fixed_atom_pairs)
        self.last_intact_bond_image = float("inf")

    def set_last_intact_bond_image(self, last_intact_bond_image):
        """Set the index of the last image with intact bond.

        From a certain image, on the COGEF trajectory can contain
        broken-bond images. You can set the last image number for which
        the bond is still intact to prevent error messages.

        Parameters
        ----------
        last_intact_bond_image: int

        """
        self.last_intact_bond_image = last_intact_bond_image

    def set_fixed_atom_pairs(self, pairs=None):
        """Define additional bond length constraints.

        Use this method if there are additional atom pairs whose bond
        length must be fixed during the complete pulling process.

        Parameters
        ----------
        pairs: list of tuples of int
            E.g. *pairs=[(1, 3), (4, 2), (10, 11)]*.

        """
        if pairs:
            # At least one atom of the two atoms (self.atom1, self.atom2) must
            # not be part of a fixed atom pair
            atom1in = False
            atom2in = False
            for pair in pairs:
                if self.atom1 in pair:
                    atom1in = True
                if self.atom2 in pair:
                    atom2in = True
            assert not(atom1in) or not(atom2in)
        self.fixed_atom_pairs = pairs

    def pull(self, stepsize, steps, initialize=do_nothing,
             trajectory='pull.traj'):
        """Pull or press atoms with numbers *self.atom1* and *self.atom2*.

        Parameters
        ----------
        stepsize: float
            Step size is positive for pulling and negative for pressing.
        steps: int
            Number of steps.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.

        Returns
        -------
        result: str or None
            'Canceled' is returned when the calculation of the COGEF path was
            canceled by a 'Finished'-return of the initialization function.

        """
        # Use last image
        imagenum = len(self.images) - 1
        return self._pull(imagenum, stepsize, steps, initialize, trajectory)

    def insert(self, imagenum, steps=1, initialize=do_nothing,
               trajectory='pull.traj'):
        """Insert images.

        Parameters
        ----------
        imagenum: int
            Insert between *imagenum* and *imagenum + 1*
        steps: int
            Number of images inserted.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.

        Returns
        -------
        result: str or None
            'Canceled' is returned when the calculation of the COGEF path was
            canceled by a 'Finished'-return of the initialization function.

        """
        image1 = self.images[imagenum]
        image2 = self.images[imagenum + 1]
        dist1 = self.get_distance(image1)
        dist2 = self.get_distance(image2)
        stepsize = (dist2 - dist1) / (steps + 1)
        return self._pull(imagenum, stepsize, steps, initialize, trajectory)

    def _pull(self, imagenum, stepsize, steps, initialize=do_nothing,
              trajectory='pull.traj', finalize=do_nothing2):
        """Pull or press atoms with numbers *self.atom1* and *self.atom2*.

        Parameters
        ----------
        imagenum: int
            Image number used for continue pulling or pressing.
        stepsize: float
            Step size is positive for pulling and negative for pressing.
        steps: int
            Number of steps.
        initialize: function
            Initialization function which is executed before the optimization
            of each image. See function *do_nothing*.
        trajectory: str
            Name of the trajectory file where the images of the COGEF path
            will be saved.
        finalize: function
            Function which is executed after the optimization of each image.
            See function *do_nothing2*.

        Returns
        -------
        result: str or None
            'Canceled' is returned when the calculation of the COGEF path was
            canceled by a 'Finished'-return of the initialization function.

        """
        optimizer_traj = None
        for step in range(steps):
            image = self.images[imagenum].copy()
            imagenum += 1
            self.images.insert(imagenum, image)
            d1, d2 = self.shift_atoms(image, stepsize)
            world.barrier()
            try:
                optimizer_traj = initialize(image, imagenum, new_opt=True,
                                            get_filename=True,
                                            atom1=self.atom1,
                                            atom2=self.atom2, d1=d1, d2=d2)
            except TypeError:
                optimizer_traj = initialize(image, imagenum, new_opt=True,
                                            get_filename=True)
            if optimizer_traj == 'Finished':
                del self.images[imagenum]
                break
            optimizer_traj_origin = optimizer_traj
            if optimizer_traj.startswith('new forces:'):
                optimizer_traj = optimizer_traj[len('new forces:'):]
                new_forces = True
            else:
                new_forces = False
            bak = False
            converged = False
            if (optimizer_traj) and (os.path.isfile(optimizer_traj)):
                # *optimizer_traj* already exists and will be further
                # optimized
                further_opt = True
                try:
                    # Do not change image to an *Atoms* object if image
                    # is no *Atoms* object
                    image.read(optimizer_traj)
                except AttributeError:
                    try:
                        # *Atoms* object has no attribute *read*
                        image = read(optimizer_traj)
                    except UnknownFileTypeError:
                        # Empty file?
                        further_opt = False
                except UnknownFileTypeError:
                    # Empty file?
                    further_opt = False
                if further_opt:
                    self.images[imagenum] = image
                    world.barrier()
                    if not(new_forces):
                        opt = self.optimizer(image)
                        opt.fmax = self.fmax
                        converged = opt.converged()
                    if not(converged):
                        # The return value of *initialize* should only depend
                        # on *imagenum* and not on *image*
                        try:
                            assert optimizer_traj_origin == \
                                initialize(image, imagenum, new_opt=False,
                                           get_filename=True,
                                           atom1=self.atom1, atom2=self.atom2,
                                           d1=0, d2=0)
                        except TypeError:
                            assert optimizer_traj_origin == \
                                initialize(image, imagenum, new_opt=False,
                                           get_filename=True)
                        if world.rank == 0:
                            os.rename(optimizer_traj, optimizer_traj + '.bak')
                        bak = True
            else:
                further_opt = False
            if not(converged):
                # Now it is clear that the optimization must start
                # therefore initialize the image with *get_filename=False*
                try:
                    initialize(image, imagenum, new_opt=not(further_opt),
                               get_filename=False, atom1=self.atom1,
                               atom2=self.atom2, d1=d1, d2=d2)
                except TypeError:
                    initialize(image, imagenum, new_opt=not(further_opt),
                               get_filename=False)
                world.barrier()
                opt = self.optimizer(image, trajectory=optimizer_traj,
                                     logfile=self.optimizer_logfile)
                self.log(step, steps, image, opt.logfile)
                opt.run(fmax=self.fmax)
                if (bak) and (world.rank == 0):
                    traj = Trajectory(optimizer_traj)
                    if (len(traj) == 1) and not(new_forces):
                        # Has not to be further optimized, so take old
                        # optimizer trajectory
                        os.rename(optimizer_traj + '.bak', optimizer_traj)
            finalize(image)
            if trajectory is not None:
                # Save the images
                self.write(trajectory)
        if optimizer_traj == 'Finished':
            return 'Canceled'

    def log(self, step, steps, atoms, logfile):
        """Show the progress.

        Parameters
        ----------
        step: int
        steps: int
        atoms: Atoms object
        logfile: file object

        """
        if logfile is None:
            return
        name = self.__class__.__name__
        logfile.write('\n%s: step %d/%d, distance %15.6f\n\n'
                      % (name, step + 1, steps, self.get_distance(atoms)))

    def get_distance(self, atoms):
        """Get the distance between the pulling positions.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: float

        """
        return norm(self.get_pulling_vector(atoms))

    def get_pulling_vector(self, atoms):
        """Get the relative position of the pulling positions.

        Parameters
        ----------
        atoms: Atoms object

        Returns
        -------
        result: numpy array of float

        """
        return atoms[self.atom2].position - atoms[self.atom1].position

    def shift_atoms(self, atoms, stepsize):
        """Increase the distance between two atoms along der connection line.

        The indices are defined by *self.atom1* and *self.atom2*. The
        the center of mass will not be changed if possible and a constraint
        is added for fixing this bond length and these defined by
        *self.fixed_atom_pairs*.

        Parameters
        ----------
        atoms: Atoms object
            Configuration used for modification.
        stepsize: float
            Total increase of distance between *self.atom1* and *self.atom2*.
            Set *stepsize* to *None* in order to only fix bond defined in
            *self.fixed_atom_pairs*.

        Returns
        -------
        result: tuple of two floats or tuple of two numpy arrays
            The shift vectors of both atoms.

        """
        if stepsize is None:
            if self.fixed_atom_pairs:
                con = FixBondLengths(self.fixed_atom_pairs)
            else:
                con = []
            atoms.set_constraint(con)
            return 0., 0.  # TODO: why not two times *zeros(3)*?
        vec = self.get_pulling_vector(atoms)
        vec /= norm(vec)
        mass1 = atoms[self.atom1].mass
        mass2 = atoms[self.atom2].mass
        value1 = mass2 / (mass1 + mass2) * stepsize
        value2 = mass1 / (mass1 + mass2) * stepsize
        if self.fixed_atom_pairs:
            atom1in = False
            atom2in = False
            for pair in self.fixed_atom_pairs:
                if self.atom1 in pair:
                    atom1in = True
                if self.atom2 in pair:
                    atom2in = True
            if atom1in:
                value2 = value1 + value2
                value1 = 0
            elif atom2in:
                value1 = value1 + value2
                value2 = 0
            con = FixBondLengths([(self.atom1, self.atom2)] +
                                 self.fixed_atom_pairs)
        else:
            con = FixBondLength(self.atom1, self.atom2)
        atoms[self.atom1].position -= value1 * vec
        atoms[self.atom2].position += value2 * vec
        atoms.set_constraint(con)
        return -value1 * vec, value2 * vec

    def write(self, filename):
        """Save the images.

        Parameters
        ----------
        filename: str

        """
        traj = Trajectory(filename, 'w')
        for image in self.images:
            traj.write(image)
        traj.close()

    def keep_images(self, imagenum):
        """Remove some images.

        Parameters
        ----------
        imagenum: int
            Keep only the images up to image number *imagenum*.
            If *imagenum* is zero, take only the zeroth image.

        """
        images = []
        for i, image in enumerate(self.images):
            if i > imagenum:
                break
            images.append(image)
        self.images = images

    def delete_image(self, imagenum):
        """Delete an image.

        Parameters
        ----------
        imagenum: int
             Image number of the image which will be deleted.

        """
        del self.images[imagenum]

    def get_maximum_force(self, method='use_energies', imagemin=0,
                          imagemax=-1, atoms1=None, atoms2=None):
        """Return the maximum force on the COGEF path.

        This is the maximum force acting between atoms with indices
        *self.atom1* and *self.atom2*.

        Parameters
        ----------
        See method *get_force_curve*.

        Returns
        -------
        result: float

        """
        return max(self.get_force_curve(method, imagemin, imagemax,
                                        atoms1=atoms1, atoms2=atoms2,
                                        only_intact_bond_images=True)[0])

    def get_energy_curve(self, imagemin=0, imagemax=-1,
                         only_intact_bond_images=False,
                         modulo=1):
        """Return the energy values and associated distances.

        Parameters
        ----------
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        only_intact_bond_images: bool
            *True* means that the given number of the last intact bond image
            defines the upper limit of used images.
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
        if only_intact_bond_images:
            imagemax = min(imagemax, self.last_intact_bond_image)
        energies = []
        distances = []
        for i in range(imagemin, imagemax + 1):
            if i % modulo != 0:
                continue
            image = self.images[i]
            energies.append(image.get_potential_energy(
                apply_constraint=False))
            distances.append(self.get_distance(image))
        return energies, distances

    def get_force_curve(self, method='use_energies', imagemin=0, imagemax=-1,
                        atoms1=None, atoms2=None,
                        only_intact_bond_images=False, modulo=1):
        """Return the constraint forces and associated distances.

        Parameters
        ----------
        method: str
            Use 'use_energies' to obtain constraint forces from energies by
            the finit-differences method. Use 'use_forces' to obtain
            constraint forces directly from forces.
        imagemin: int
            Image number of first image used.
        imagemax: int
            Image number of last image used. Negative values can be used to
            count from the other direction.
        atoms1: list of int (optional)
            Indices of atoms on the one side whose forces are used for the
            calculation of the constraint force. *self.atom1* is always
            included, additional atoms may be added to cancel forces which
            are zero only for a perfect structure optimization.
        atoms2: list of int (optional)
            Indices of atoms on the other side whose forces are used for the
            calculation of the constraint force. *self.atom2* is always
            included.
        only_intact_bond_images: bool
            *True* means that the given number of the last intact bond image
            defines the upper limit of used images.
        modulo: int
            Set it to a larger value that less images are used, e.g. modulo=2
            means that every second image is used.

        Returns
        -------
        result: two list of floats
            Constraint forces and associated distances in the order of the
            image numbers. Returned distances also depend on the method.

        """
        if imagemax < 0:
            imagemax += len(self.images)
        if only_intact_bond_images:
            imagemax = min(imagemax, self.last_intact_bond_image)
        if method == 'use_energies':
            energies, distances = self.get_energy_curve(
                imagemin, imagemax, only_intact_bond_images, modulo=modulo)
            forces = []
            fd_distances = []
            for i in range(len(energies) - 2):
                forces.append((energies[i + 2] - energies[i]) /
                              (distances[i + 2] - distances[i]))
                fd_distances.append((distances[i + 2] + distances[i]) / 2.)
            return forces, fd_distances
        elif method == 'use_forces':
            forces = []
            distances = []
            for i in range(imagemin, imagemax + 1):
                if i % modulo != 0:
                    continue
                image = self.images[i]
                forces.append(self.constraint_force(i, atoms1, atoms2))
                distances.append(self.get_distance(image))
            return forces, distances
        else:
            raise ValueError

    def constraint_force(self, imagenum, atoms1=None, atoms2=None):
        """Calculate the constraint force.

        Parameters
        ----------
        imagenum: int
            Image number of image used.
        atoms1: list of int (optional)
            Indices of atoms on the one side whose forces are used for the
            calculation of the constraint force. *self.atom1* is always
            included, additional atoms may be added to cancel forces which
            are zero only for a perfect structure optimization.
        atoms2: list of int (optional)
            Indices of atoms on the other side whose forces are used for the
            calculation of the constraint force. *self.atom2* is always
            included.

        Returns
        -------
        result: float
            Constraint force. Positive sign means attraction.

        """
        if atoms1:
            if self.atom1 not in atoms1:
                atoms1.append(self.atom1)
        else:
            atoms1 = [self.atom1]
        if atoms2:
            if self.atom2 not in atoms2:
                atoms2.append(self.atom2)
        else:
            atoms2 = [self.atom2]
        image = self.images[imagenum]
        # Do not consider constraints
        forces = image.get_forces(apply_constraint=False)
        vec = self.get_pulling_vector(image)
        vec /= norm(vec)
        delta_f = 0
        for atom in atoms1:
            delta_f += forces[atom]
        for atom in atoms2:
            delta_f -= forces[atom]
        return dot(delta_f, vec) / 2.
