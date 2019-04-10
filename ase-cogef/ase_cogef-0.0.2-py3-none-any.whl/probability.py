# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Module for calculating probability densities and rupture forces of more
complex systems of minima.

"""

from numpy import exp, zeros, dot, maximum, array, tanh
from numpy.linalg import eig, inv, det
from warnings import warn

from ase.units import kB


def load_rate_constants(filein='rates.dat'):
    """Load and return dissociation rate constants for forward reaction only.

    Parameters
    ----------
    filein: str
        Name of the file created with method *save_rate_constants* of
        class *Dissociation*.

    Returns
    -------
    rates: list of floats
        Rate constants.
    forces: list of floats
        External forces.

    """
    rates = []
    forces = []
    fd = open(filein)
    first = True
    for line in fd:
        if first:
            first = False
            continue
        line_arr = line.rstrip().split()
        forces.append(float(line_arr[0]))
        rates.append(float(line_arr[1]))
    fd.close()
    return rates, forces


def load_all_rate_constants(filein='rates.dat'):
    """Load and return dissociation rate constants for forward and backward
    reaction.

    Parameters
    ----------
    filein: str
        Name of the file created with method *save_all_rate_constants* of
        class *Dissociation2d*.

    Returns
    -------
    rates: list of floats
        Rate constants for forward reaction.
    back_rates: list of floats
        Rate constants for backward reaction.
    forces: list of floats
        External forces.

    """
    rates = []
    back_rates = []
    forces = []
    fd = open(filein)
    first = True
    for line in fd:
        if first:
            first = False
            continue
        line_arr = line.rstrip().split()
        forces.append(float(line_arr[0]))
        rates.append(float(line_arr[1]))
        back_rates.append(float(line_arr[2]))
    fd.close()
    return rates, back_rates, forces


def load_external_forces(filein='force.dat'):
    """Load and return external forces of the reactant minimum.

    Parameters
    ----------
    filein: str
        Name of the file created with method *save_external_forces* of
        class *Dissociation*.

    Returns
    -------
    return 1: list of floats
        External forces.
    return 2: list of floats
        *f_ext* values with
        f_ext = 'spring constant' * 'velocity'  * 'time' + 'initial force'

    """
    return load_rate_constants(filein)


def load_all_external_forces(filein='force.dat'):
    """Load and return external forces for the reactant/intact-bond minimum
    and the product/broken-bond minimum curve.

    Parameters
    ----------
    filein: str
        Name of the file created with method *save_all_external_forces* of
        class *Dissociation2d*.

    Returns
    -------
    return 1: list of floats
        External forces for the reactant minimum.
    return 2: list of floats
        External forces for the product minimum.
    return 3: list of floats
        *f_ext* values with
        f_ext = 'spring constant' * 'velocity'  * 'time' + 'initial force'

    """
    return load_all_rate_constants(filein)


def load_mean_distances_intact(filein='dists.dat'):
    """Load and return mean distances of the reactant/intact-bond minimum.

    Parameters
    ----------
    filein: str
        Name of the file created with method *save_mean_distances* of
        class *Dissociation*.

    Returns
    -------
    dists: list of floats
        Mean distances.
    forces: list of floats
        External forces.

    """
    dists = []
    forces = []
    fd = open(filein)
    first = True
    for line in fd:
        if first:
            first = False
            continue
        line_arr = line.rstrip().split()
        forces.append(float(line_arr[0]))
        dists.append(float(line_arr[1]))
    fd.close()
    return dists, forces


def load_mean_distances(filein='dists.dat'):
    """Load and return mean distances of the reactant/intact-bond and
    product/broken-bond minima.

    Parameters
    ----------
    filein: str
        Name of the file created with method *save_mean_distances* of
        class *Dissociation2d*.

    Returns
    -------
    dists_i: list of floats
        Mean distances for reactant minimum.
    dists_b: list of floats
        Mean distances for the product minimum.
    forces: list of floats
        External forces.

    """
    dists_i = []
    dists_b = []
    forces = []
    fd = open(filein)
    first = True
    for line in fd:
        if first:
            first = False
            continue
        line_arr = line.rstrip().split()
        forces.append(float(line_arr[0]))
        dists_i.append(float(line_arr[1]))
        dists_b.append(float(line_arr[2]))
    fd.close()
    return dists_i, dists_b, forces


class Minimum(object):
    """A single energy minimum of the PES. A known and fixed list of
    external force values is required.

    Parameters
    ----------
    neighbours: list of tuples of Minimum object and two lists of floats
                (optional)
        Each tuple in *neighbours* contains a minimum object defining the
        neighbour, a list of forward and a list of backward rate constants
        for the transition to this neighbour. The order of the rate constants
        corresponds to the known list of external force values.
    distances: list of floats (optional)
        The mean distances of this minimum defined by *cogef.atom1* and
        *cogef.atom2* where *cogef* is the corresponding *COGEF2D* object.
        The order corresponds to the known list of external force values.

    """
    def __init__(self, neighbours=None, distances=None):
        if neighbours is None:
            neighbours = []
        self.neighbours = neighbours
        if distances is None:
            distances = []
        self.distances = distances

    def add_destination(self, rates, back_rates=None, minimum=None,
                        distances=None):
        """Add a transition to another minimum.

        Parameters
        ----------
        rates: list of floats
            List of rate constants corresponding to the considered forces.
        back_rates: list of floats (optional)
            If a back reaction is possible, the corresponding rate
            constants can be filled in the list *back_rates*.
        minimum: Minimum object (optional)
            Minimum object of the destination. If *minimum* is *None*,
            a new minimum will be created.
        distances: list of floats
            The mean distances of the destination minimum.

        Returns
        -------
        minimum: Minimum object
            The Desination.

        """
        if minimum is None:
            # Create a new minimum
            minimum = Minimum()
        if distances is not None:
            minimum.distances = distances
        if back_rates is None:
            self.neighbours.append((minimum, rates, None))
            minimum.neighbours.append((self, None, rates))
        else:
            self.neighbours.append((minimum, rates, back_rates))
            minimum.neighbours.append((self, back_rates, rates))
        return minimum

    def get_destinations(self, get_minima=True, get_rates=False):
        """Return all destination minima and/or the rate constants of the
        associated transition.

        Parameters
        ----------
        get_minima: bool
            Set it to *True* in order to get Minimum objects.
        get_rates: bool
            Set it to *True* in order to get rate constants.

        Returns
        ------
        result: list of tuples of Minimum object and list of floats or
                list of Minimum objects or list of lists of floats

        """
        assert get_minima or get_rates
        result = []
        for neighbour in self.neighbours:
            if neighbour[1] is None:
                continue
            if get_minima:
                if get_rates:
                    result.append((neighbour[0], neighbour[1]))
                else:
                    result.append(neighbour[0])
            else:
                result.append(neighbour[1])
        return result

    def get_sources(self, get_minima=True, get_rates=False):
        """Return all source minima and/or the rate constants of the
        associated transition.

        Parameters
        ----------
        get_minima: bool
            Set it to *True* in order to get Minimum objects.
        get_rates: bool
            Set it to *True* in order to get rate constants.

        Returns
        ------
        result: list of tuples of Minimum object and list of floats or
                list of Minimum objects or list of lists of floats

        """
        assert get_minima or get_rates
        result = []
        for neighbour in self.neighbours:
            if neighbour[2] is None:
                continue
            if get_minima:
                if get_rates:
                    result.append((neighbour[0], neighbour[2]))
                else:
                    result.append(neighbour[0])
            else:
                result.append(neighbour[2])
        return result

    def set_distances(self, distances):
        """Set the mean distances of this minimum.

        Parameters
        ----------
        distances: list of floats

        """
        self.distances = distances


class Minima(object):
    """The system of minima of the PES which you want to consider.

    A known and fixed list of external force values is required.

    """
    def __init__(self):
        minimum = Minimum()
        self.system = [minimum]
        self.prob = [1.]
        self.position = minimum
        self.simple_rates = None
        self.simple_indices = None

    def add_destination(self, rates, backrates=None, minimum=None,
                        distances=None):
        """Add a transition from *self.position* to another minimum.

        Parameters
        ----------
        rates: list of floats
            List of rate constants corresponding to the considered forces.
        back_rates: list of floats (optional)
            If a back reaction is possible, the corresponding rate
            constants can be filled in the list *back_rates*.
        minimum: Minimum object (optional)
            Minimum object of the destination. If *minimum* is *None*,
            a new minimum will be created.
        distances: list of floats
            The mean distances of the destination minimum.

        Returns
        -------
        minimum: Minimum object
            The Desination.

        """
        mini = self.position.add_destination(rates, backrates, minimum,
                                             distances)
        if mini not in self.system:
            self.system.append(mini)
            self.prob.append(0.)
        return mini

    def get_destinations(self):
        """Return all destination minima of *self.position*.

        Returns
        -------
        result: list of Minimum objects

        """
        return self.position.get_destinations()

    def add_minimum(self, minimum=None):
        """Add independent minimum without connection to other minima.

        Parameters
        ----------
        minimum: Minimum object (optional)
            Minimum object of the destination. If *minimum* is *None*,
            a new minimum will be created.

        Returns
        -------
        result:  Minimum object
            Added minimum.

        """
        if minimum is None:
            # Create a new minimum
            minimum = Minimum()
        if minimum not in self.system:
            self.system.append(minimum)
            self.prob.append(0.)
        self.set_position(minimum)
        return minimum

    def index(self, minimum=None):
        """Get the index of the *minimum* or *self.position*.

        Pameters
        --------
        minimum: Minimum object (optional)

        Returns
        -------
        result: int

        """
        if minimum is None:
            return self.system.index(self.position)
        else:
            assert minimum in self.system
            return self.system.index(minimum)

    def set_probability(self, probability):
        """Set the probability of *self.position*.

        Parameters
        ----------
        probability: float

        """
        self.prob[self.index()] = probability

    def get_probability(self):
        """Get the probability of *self.position*.

        Returns
        -------
        result: float

        """
        return self.prob[self.index()]

    def set_distances(self, distances):
        """Set the mean distances of *self.position*.

        Parameters
        ----------
        distances: list of floats

        """
        self.position.set_distances(distances)

    def set_position(self, minimum):
        """Set *self.position* to *minimum*.

        Parameters
        ----------
        minimum: Minimum object

        """
        assert minimum in self.system
        self.position = minimum

    def reset_probabilities(self):
        """Give the reactant state all of the probability.

        """
        self.prob[0] = 1.
        for i in range(1, len(self.prob)):
            self.prob[i] = 0.

    def check_simple_case(self, force_index=-1):
        """Check whether the system is a simple system with only rates
        from reactant state 0 to product states 1, 2, ... without back
        rates and without rates between the products.

        Parameters
        ----------
        force_index: int
            Set it to zero or positive values in order to save the product
            indices and rate constants for the reaction to the products
            associated to this force index into
            *self.simple_indices* and *self.simple_rates*.

        Returns
        -------
        result: bool

        """
        if force_index >= 0:
            self.simple_rates = []
            self.simple_indices = []
        else:
            self.simple_rates = None
            self.simple_indices = None
        for index, mini in enumerate(self.system):
            for neighbour, rates, back_rates in mini.neighbours:
                nindex = self.index(neighbour)
                if (index > 0) and (rates is not None) or \
                   (nindex > 0) and (back_rates is not None):
                    return False
                if (force_index >= 0) and (index == 0):
                    self.simple_rates.append(rates[force_index])
                    self.simple_indices.append(nindex)
        return True

    def get_differential_equations(self, force_index):
        """Get the system of differential equations.

        The form is
        d(self.prob[1:]) / dt=diffeqvec + diffeqmat * self.prob[1:]
        with a matrix *diffeqmat* and a vector *diffeqvec*.

        Parameters
        ----------
        force_index: int
            The differential equation depends on the rate constants which
            depends on the external force defined by this index.

        Returns
        -------
        diffeqmat: 2-dim. numpy array of float * float
        diffeqvec: numpy array of float

        """
        # The sum of probabilities is 1, so one can reduce the system by 1.
        diffeqmat = zeros((len(self.system) - 1, len(self.system) - 1))
        diffeqvec = zeros(len(self.system) - 1)
        for index, mini in enumerate(self.system):
            if index == 0:
                continue
            for neighbour, rates, back_rates in mini.neighbours:
                if rates is None:
                    rate = 0.
                else:
                    rate = rates[force_index]
                if back_rates is None:
                    back_rate = 0.
                else:
                    back_rate = back_rates[force_index]
                nindex = self.index(neighbour)
                diffeqmat[index - 1, index - 1] -= rate
                if nindex == 0:
                    # *self.prob[0]* is replaced by
                    # 1 - self.prob[1] - self.prob[2] - ...
                    diffeqvec[index - 1] += back_rate
                    for i in range(len(self.system) - 1):
                        diffeqmat[index - 1, i] -= back_rate
                else:
                    diffeqmat[index - 1, nindex - 1] += back_rate
        return diffeqmat, diffeqvec

    def time_step(self, force_index, ts=1e-6):
        """Make a time step and obtain the new probabilities.

        force_index: int
            Index of the external force which is assumed to be constant
            during the time step. It defines which rates from the associated
            lists will be used.
        ts: float
            Time step in seconds.

        """
        if self.check_simple_case(force_index):
            # This special case can be solved without inverting vecs
            k_all = sum(self.simple_rates)
            deltaprob = self.prob[0] * (exp(-k_all * ts) - 1)
            self.prob[0] += deltaprob
            for i, si in enumerate(self.simple_indices):
                self.prob[si] -= self.simple_rates[i] / k_all * deltaprob
            return
        diffeqmat, diffeqvec = self.get_differential_equations(force_index)
        vals, vecs = eig(diffeqmat)
        if abs(det(vecs)) < 1e-10:
            # Matrix vecs is almost singular
            raise RuntimeError('Solving of the differential equation has ' +
                               'crashed due to a singular matrix.')
        ivecs = inv(vecs)
        sum_p = sum(self.prob)
        transprob = dot(ivecs, self.prob[1:])
        transdiffeqvec = dot(ivecs, diffeqvec)
        for i in range(len(self.system) - 1):
            expo = exp(vals[i] * ts)
            if expo != 1:
                ratio = transdiffeqvec[i] / vals[i]
                transprob[i] = (transprob[i] + ratio) * expo - ratio
            else:
                transprob[i] += transdiffeqvec[i] * ts
        self.prob[1:] = dot(vecs, transprob).real
        self.prob[0] = sum_p - sum(self.prob[1:])

    def get_mean_distance(self, index):
        """Return the mean distance.

        Parameters
        ----------
        index: int
            Index of the external force.

        Returns
        -------
        mean_d: float

        """
        mean_d = 0.
        for i in range(len(self.system)):
            mean_d += self.prob[i] * self.system[i].distances[index]
        return mean_d


def probability_density(minima, forces, loading_rate, return_probs=False):
    """Return a list of dp/df-values where p is the bond-breaking probability
    and f is the external force.

    This function is similar to method *probability_density* of class
    *Dissociation*. But you can use this function for more complex systems
    of minima.

    Parameters
    ----------
    minima: Minima object
        System of minima.
    forces: list of floats
        List of external force values associated to the rate constants in
        *minima*.
    loading_rate: float
        The force is assumed to inceases uniformly by this loading rate.
    return_probs: bool
        Probabilities are also returned if it is *True*.

    Returns
    -------
    result: list of lists of floats or tuple of two list of lists of floats
        dp/df-values and optional p-values for each minimum.

    """
    prob_old = list(minima.prob)
    dpdf = []
    for i in range(len(minima.system)):
        dpdf.append([])
    if return_probs:
        probs = []
        for i in range(len(minima.system)):
            probs.append([minima.prob[i]])
    force_step = 0.
    step = 0.
    start = True
    for i, f_ext in enumerate(forces):
        step = 0.
        if start:
            start = False
            # In the first round only one half step
        else:
            # Half step
            minima.time_step(i, force_step / (2. * loading_rate))
            step += force_step / 2.
            if return_probs:
                for j in range(len(minima.system)):
                    probs[j].append(minima.prob[j])
        # In the last round only one half step
        if i + 1 < len(forces):
            force_step = forces[i + 1] - f_ext
            step += force_step / 2.
            # Half step
            minima.time_step(i, force_step / (2. * loading_rate))
        for j in range(len(minima.system)):
            dpdf[j].append((minima.prob[j] - prob_old[j]) / step)
        prob_old = list(minima.prob)
    if return_probs:
        return dpdf, probs
    else:
        return dpdf


def get_intersection(array1, array2):
    """Find one intersection of two curves.

    Parameters
    ----------
    array1: list of floats
        y-values of curve 1.
    array2: list of floats
        y-values of curve 2 for the same x-grid like curve 1.

    Returns
    -------
    result 1: float or None
        Array value from a linear interpolation or *None* if not possible.
    result 2: int
        Index nearest to the intersection point.

    """
    assert len(array1) == len(array2)
    last_index = len(array1) - 1
    array1 = array(array1)
    array2 = array(array2)
    diff = abs(array1 - array2)
    k = list(diff).index(min(diff))
    dy0 = array1[k] - array2[k]
    if dy0 == 0:
        return array1[k], k
    if (k > 0) and (dy0 * (array1[k - 1] - array2[k - 1]) < 0):
        dy1 = array1[k] - array1[k - 1]
        dy2 = array2[k] - array2[k - 1]
        dx = dy0 / (dy1 - dy2)
        return array1[k] - dy1 * dx, k
    if (k < last_index) and \
       (dy0 * (array1[k + 1] - array2[k + 1]) < 0):
        dy1 = array1[k + 1] - array1[k]
        dy2 = array2[k + 1] - array2[k]
        dx = dy0 / (dy2 - dy1)
        return array1[k] + dy1 * dx, k
    return None, k


def probability_density_polymer(minima, forces1, distances, forces2, forces3,
                                loading_rate, spring_constant, monomer_number,
                                return_probs=False, return_exforces=False):
    """Cold polymer model - a linear polymer.

    Return a list of dp/df-values where p is the bond-breaking probability
    and f is the external force.

    The assumption here in contrast to the function *probability_density* is
    that a polymer which contains many monomers is stretched by a spring whose
    endpoint is pulled with a certain velocity.
    It is assumed that the stretching of a
    single monomer relative to the average stretching is neglectable
    compared to the complete polymer stetching length. The second assumption
    is that the single monomers always feels the average external force
    arising from the average stretching length of the polymer.

    Parameters
    ----------
    minima: Minima object
        System of minima which contains the information of the rate
        constants of all transitions for a single monomer.
    forces1: list of floats
        External forces associated to the rate constants from *minima*.
    distances: list of lists of floats
        Lists of distance values relative to the equilibrium distance for
        each minimum in *minima*.
    forces2: list of floats
        External force values associated to the distance lists in *distances*.
    forces3: list of floats
        (loading_rate * time)-values, thus the external forces values if the
        polymer would be rigid, see *loading_rate* below.
    loading_rate: float
        Loading rate for a rigig polymer defined as
        *spring_constant* times pulling velocity.
    spring_constant: float
        Spring constant.
    monomer_number: int
        Number of monomers in the polymer.
    return_probs: bool
        Probabilities are also returned if it is *True*.
    return_exforces: bool
        External forces are also returned if it is *True*.

    Returns
    -------
    result 1: list of lists of floats
        dp/df-values for each minimum.
    result 2: list of lists of floats (optional)
        p-values for each minimum.
    result 3: list of floats (optional)
        External forces.

    """
    prob_old = list(minima.prob)
    dpdf = []
    for i in range(len(minima.system)):
        dpdf.append([])
        # In order to get later correct indices, the distances must
        # increase monotonically
        if (maximum.accumulate(distances[i]) != distances[i]).any():
            raise NotImplementedError(
                'I do not know yet, how I can find correct force indices ' +
                'when the distances do not increase monotonically.')
    if return_probs:
        probs = []
        for i in range(len(minima.system)):
            probs.append([minima.prob[i]])
    if return_exforces:
        exforces = []
    forces1 = array(forces1)
    different_forces = (forces1 != forces2).any()
    distances = array(distances)
    force_step = 0.
    step = 0.
    start = True
    for i, f_ext in enumerate(forces3):
        step = 0.
        if start:
            start = False
            # In the first round only one half step
        else:
            mean_dists = 0.
            for j in range(len(minima.system)):
                mean_dists += minima.prob[j] * distances[j, :]
            dists_tot = mean_dists * monomer_number
            forces = f_ext - spring_constant * dists_tot
            # Find intersection of *forces* and *forces2*
            f_tot, k = get_intersection(forces, forces2)
            if different_forces:
                diff = abs(f_tot - forces1)
                k = list(diff).index(min(diff))
            # Half step
            minima.time_step(k, force_step / (2. * loading_rate))
            step += force_step / 2.
            if return_probs:
                for j in range(len(minima.system)):
                    probs[j].append(minima.prob[j])
        mean_dists = 0.
        for j in range(len(minima.system)):
            mean_dists += minima.prob[j] * distances[j, :]
        dists_tot = mean_dists * monomer_number
        forces = f_ext - spring_constant * dists_tot
        # Find intersection of *forces* and *forces2*
        f_tot, k = get_intersection(forces, forces2)
        if return_exforces:
            exforces.append(f_tot)
        if (k == 0) and (f_tot < 2 * forces2[0] - forces2[1]):
            warn("'forces2' starts probably with too large forces.")
        if (k == len(forces2) - 1) and \
           (f_tot > 2 * forces2[-1] - forces2[-2]):
            warn("'forces2' ends probably with too small forces.")
        if different_forces:
            diff = abs(f_tot - forces1)
            k = list(diff).index(min(diff))
        if (k == 0) and (f_tot < 2 * forces1[0] - forces1[1]):
            warn("'forces1' starts probably with too large forces.")
        if (k == len(forces1) - 1) and \
           (f_tot > 2 * forces1[-1] - forces1[-2]):
            warn("'forces1' ends probably with too small forces.")
        # In the last round only one half step
        if i + 1 < len(forces3):
            # Half step
            force_step = forces3[i + 1] - f_ext
            step += force_step / 2.
            minima.time_step(k, force_step / (2. * loading_rate))
        for j in range(len(minima.system)):
            dpdf[j].append((minima.prob[j] - prob_old[j]) / step)
        prob_old = list(minima.prob)
    if return_probs:
        if return_exforces:
            return dpdf, probs, exforces
        else:
            return dpdf, probs
    else:
        if return_exforces:
            return dpdf, exforces
        else:
            return dpdf


def probability_density_polymer2(minima, forces1, distances, forces2,
                                 forces3, loading_rate, spring_constant, T,
                                 monomer_number, return_probs=False,
                                 return_exforces=False):
    """Ideal chain/freely jointed chain model.

    Return a list of dp/df-values where p is the bond-breaking probability
    and f is the external force.

    The assumption here in contrast to function *probability_density_polymer*
    is that the monomers are not aligned along the connecting line between the
    end points of the polymer but they behave like a random walk neglecting
    steric effects (ideal chain model). Different rotation
    angles of the monomers are weighted by a force-dependent Boltzmann factor.
    It is assumed that the stretching of a
    single monomer relative to the average stretching is neglectable
    compared to the complete polymer stetching length. The second assumption
    is that the single monomers always feels the average external force
    arising from the average stretching length of the polymer projected onto
    the monomer axis.

    Parameters
    ----------
    minima: Minima object
        System of minima which contains the information of the rate
        constants of all transitions for a single monomer.
    forces1: list of floats
        External forces associated to the rate constants from *minima*.
    distances: list of lists of floats
        Lists of distance values (length of the monomers, not relative
        distances!) for each minimum in *minima*.
    forces2: list of floats
        External force values associated to the distance lists in *distances*.
    forces3: list of floats
        (loading_rate * time)-values, thus the external forces values if the
        polymer would be rigid, see *loading_rate* below.
    loading_rate: float
        Loading rate for a rigig polymer defined as
        *spring_constant* times pulling velocity.
    spring_constant: float
        Spring constant.
    T: float
        Temperature.
    monomer_number: int
        Number of monomers in the polymer.
    return_probs: bool
        Probabilities are also returned if it is *True*.
    return_exforces: bool
        External forces are also returned if it is *True*.

    Returns
    -------
    result 1: list of lists of floats
        dp/df-values for each minimum.
    result 2: list of lists of floats (optional)
        p-values for each minimum.
    result 3: list of floats (optional)
        External forces.

    """
    prob_old = list(minima.prob)
    dpdf = []
    for i in range(len(minima.system)):
        dpdf.append([])
        # In order to get later correct indices, the distances must
        # increase monotonically
        if (maximum.accumulate(distances[i]) != distances[i]).any():
            raise NotImplementedError(
                'I do not know yet, how I can find correct force indices ' +
                'when the distances do not increase monotonically.')
    if return_probs:
        probs = []
        for i in range(len(minima.system)):
            probs.append([minima.prob[i]])
    if return_exforces:
        exforces = []
    forces1 = array(forces1)
    forces2 = array(forces2)
    distances = array(distances)
    # Determine the average forces *proj_f* projected onto the monomer axis
    # and the average distance values/length *proj_d* of the monomers
    # projected on the polymer axis in dependence of the external force
    # acting on the end points of the polymer
    assert (forces2 >= 0.).all()
    proj_f = []
    proj_d = []
    for j in range(len(minima.system)):
        proj_f.append([])
        proj_d.append([])
        for i, f_tot in enumerate(forces2):
            if f_tot == 0.:
                proj_f[j].append(0.)
                proj_d[j].append(0.)
                continue
            facs = f_tot * distances[j, :i + 1] / (kB * T)
            proj_forces = f_tot / facs * (facs / tanh(facs) - 1)
            force, k = get_intersection(proj_forces, forces2[:i + 1])
            proj_f[j].append(force)
            fac = f_tot * distances[j, k] / (kB * T)
            proj_d[j].append(
                distances[j, k] / fac * (fac / tanh(fac) - 1))
    proj_f = array(proj_f)
    proj_d = array(proj_d)
    force_step = 0.
    step = 0.
    start = True
    for i, f_ext in enumerate(forces3):
        step = 0.
        if start:
            start = False
            # In the first round only one half step
        else:
            mean_dists = 0.
            for j in range(len(minima.system)):
                mean_dists += minima.prob[j] * proj_d[j, :]
            dists_tot = mean_dists * monomer_number
            forces = f_ext - spring_constant * dists_tot
            # Find intersection of *forces* and *forces2*
            f_tot, k = get_intersection(forces, forces2)
            # For simplicity, use average projected force
            projf = 0.
            for j in range(len(minima.system)):
                projf += minima.prob[j] * proj_f[j, k]
            diff = abs(projf - forces1)
            k = list(diff).index(min(diff))
            # Half step
            minima.time_step(k, force_step / (2. * loading_rate))
            step += force_step / 2.
            if return_probs:
                for j in range(len(minima.system)):
                    probs[j].append(minima.prob[j])
        mean_dists = 0.
        for j in range(len(minima.system)):
            mean_dists += minima.prob[j] * proj_d[j, :]
        dists_tot = mean_dists * monomer_number
        forces = f_ext - spring_constant * dists_tot
        # Find intersection of *forces* and *forces2*
        f_tot, k = get_intersection(forces, forces2)
        if return_exforces:
            exforces.append(f_tot)
        if (k == 0) and (f_tot < 2 * forces2[0] - forces2[1]):
            warn("'forces2' starts probably with too large forces.")
        if (k == len(forces2) - 1) and \
           (f_tot > 2 * forces2[-1] - forces2[-2]):
            warn("'forces2' ends probably with too small forces.")
        # For simplicity, use average projected force
        projf = 0.
        for j in range(len(minima.system)):
            projf += minima.prob[j] * proj_f[j, k]
        diff = abs(projf - forces1)
        k = list(diff).index(min(diff))
        if (k == 0) and (f_tot < 2 * forces1[0] - forces1[1]):
            warn("'forces1' starts probably with too large forces.")
        if (k == len(forces1) - 1) and \
           (f_tot > 2 * forces1[-1] - forces1[-2]):
            warn("'forces1' ends probably with too small forces.")
        # In the last round only one half step
        if i + 1 < len(forces3):
            # Half step
            force_step = forces3[i + 1] - f_ext
            step += force_step / 2.
            minima.time_step(k, force_step / (2. * loading_rate))
        for j in range(len(minima.system)):
            dpdf[j].append((minima.prob[j] - prob_old[j]) / step)
        prob_old = list(minima.prob)
    if return_probs:
        if return_exforces:
            return dpdf, probs, exforces
        else:
            return dpdf, probs
    else:
        if return_exforces:
            return dpdf, exforces
        else:
            return dpdf


def constant_velocity(minima, forces, velocity, dist_step, dist_max):
    """Simulate a constant-velocity experiment.

    Perhaps obsolete function (?)

    """
    forces_out = []
    dist_out = []
    index = 0
    dist = minima.get_mean_distance(index)
    time_step = dist_step / velocity
    start = True
    while dist <= dist_max:
        if start:
            start = False
            # In the first round only one half step
        else:
            while minima.get_mean_distance(index) < dist:
                index += 1
                if index > len(forces) - 1:
                    raise ValueError('dist_max is too large or the range ' +
                                     'of forces is too small.')
            # Half step
            minima.time_step(index, time_step / 2.)
        # In the last round only one half step
        if dist + dist_step <= dist_max:
            # Half step
            minima.time_step(index, time_step / 2.)
        forces_out.append(forces[index])
        dist_out.append(dist)
        dist += dist_step
    return forces_out, dist_out


def rupture_force_from_dpdf(dpdf, forces, force_step=None):
    """Calculate the average rupture force for a given probability
    density and the associated force values by numerical integration.

    *f_ext* (the theoretical external force for a rigid molecule) is defined
    by f_ext = 'spring constant' * 'velocity'  * 'time' + 'initial force'
    or the real external force for zero sping constant.

    Parameters
    ----------
    dpdf: list of floats
        dp/df-values for each *f_ext*-value.
    forces: list of floats
        External forces for each *f_ext*.
    force_step: float (optional)
        Step size of *f_ext*.

    Returns
    -------
    result: float
        Rupture force.

    """
    if force_step is None:
        force_step = forces[1] - forces[0]
        for i in range(2, len(forces)):
            if abs(force_step - (forces[i] - forces[i - 1])) > 1e-6:
                raise ValueError('The force steps in list forces should ' +
                                 'be constant.')
    integration1 = 0.
    integration2 = 0.
    for i in range(len(dpdf)):
        integration1 += dpdf[i] * force_step * forces[i]
        integration2 += dpdf[i] * force_step
    return integration1 / integration2


def rupture_force_and_uncertainty_from_dpdf(dpdf, forces, force_step=None):
    """Calculate the average rupture force and its uncertainty for a
    given probability density.

    The uncertainty is defined as the range
    around the average rupture force which contains all forces with a
    total probability of 68.3% (one standard deviation).
    *f_ext* (the theoretical external force for a rigid molecule) is defined
    by f_ext = 'spring constant' * 'velocity'  * 'time' + 'initial force'
    or the real external force for zero sping constant.

    Parameters
    ----------
    dpdf: list of floats
        dp/df-values for each *f_ext*-value.
    forces: list of floats
        External forces for each *f_ext*.
    force_step: float (optional)
        Step size of *f_ext*.

    Returns
    -------
    result 1: float
        Rupture force.
    result 2: float
        Standard deviation.

    """
    if force_step is None:
        force_step = forces[1] - forces[0]
        for i in range(2, len(forces)):
            if abs(force_step - (forces[i] - forces[i - 1])) > 1e-6:
                raise ValueError('The force steps in list forces should ' +
                                 'be constant.')
    f_rup = rupture_force_from_dpdf(dpdf, forces, force_step)
    # Get index of *forces* with associated force nearest to *f_rup*
    diff = list(abs(forces - f_rup))
    index = diff.index(min(diff))
    diff[index] = float("inf")
    index2 = diff.index(min(diff))
    # In order to get the correct index, the forces must increase
    # monotonically around *f_rup*
    if abs(index - index2) != 1:
        raise NotImplementedError(
            'I do not know yet, how I can find the force index associated ' +
            'to the rupture force when the forces do not increase ' +
            'monotonically around f_rup. Is the step size of the energy' +
            'curves small enough?')
    prob = dpdf[index] * force_step
    di = 0
    while 100 * prob < 68.3:
        di += 1
        try:
            prob += (dpdf[index + di] + dpdf[index - di]) * force_step
        except IndexError:
            raise ValueError('Range of the force interval is too ' +
                             'small to calculate the uncertainty.')
    return f_rup, (forces[index + di] - forces[index - di]) / 2.
