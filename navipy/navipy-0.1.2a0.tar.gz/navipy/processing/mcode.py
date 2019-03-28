"""
Motion code
"""
from navipy.scene import __spherical_indeces__
from navipy.scene import is_numeric_array
from navipy.maths.homogeneous_transformations\
    import compose_matrix
from navipy.maths.coordinates\
    import spherical_to_cartesian, cartesian_to_spherical_vectors
import numpy as np
import pandas as pd
from navipy.maths.euler import angular_velocity
from navipy.maths.constants import _AXES2TUPLE


def _check_optic_flow_param(viewing_directions,
                            velocity):
    if not isinstance(velocity, pd.Series):
        raise TypeError('velocity should be a pandas Series')
    if velocity is None:
        raise ValueError("velocity must not be None")
    if velocity.empty:
        raise Exception('velocity must not be empty')
    if not isinstance(velocity.index, pd.core.index.MultiIndex):
        raise Exception('velocity must have a multiindex containing \
                         the convention used')

    index = velocity.index
    convention = sorted(index.get_level_values(0))[-1]
    if convention not in _AXES2TUPLE.keys():
        msg = "the chosen convention {} is not supported"
        msg = msg.format(convention)
        raise ValueError(msg)
    if 'x' not in velocity.index.get_level_values(1):
        raise ValueError('missing index x')
    if 'y' not in velocity.index.get_level_values(1):
        raise ValueError('missing index y')
    if 'z' not in velocity.index.get_level_values(1):
        raise ValueError('missing index z')
    if 'alpha_0' not in velocity.index.get_level_values(1):
        raise ValueError('missing index alpha_0')
    if 'alpha_1' not in velocity.index.get_level_values(1):
        raise ValueError('missing index alpha_1')
    if 'alpha_2' not in velocity.index.get_level_values(1):
        raise ValueError('missing index alpha_2')
    if np.any(pd.isnull(velocity)):
        raise ValueError('velocity must not contain nan')
    if viewing_directions is None:
        raise ValueError("viewing direction must not be None")
    if (not isinstance(viewing_directions, list)) and\
       (not isinstance(viewing_directions, np.ndarray)):
        raise TypeError("angels must be list or np.ndarray")
    if not is_numeric_array(viewing_directions):
        raise TypeError("viewing_direction must be of numerical type")

    return index, convention


def optic_flow_rotationonal(viewing_directions, velocity):
    """ rotational optic flow
    :param viewing_directions: viewing direction of each pixel
           (azimuth,elevation)
    :param velocity: pandas series
                     (x,y,z,alpha,beta,gamma,dx,dy,dz,dalpha,dbeta,dgamma)
    """
    passindex, convention = _check_optic_flow_param(viewing_directions,
                                                    velocity)
    elevation = viewing_directions[..., __spherical_indeces__['elevation']]
    azimuth = viewing_directions[..., __spherical_indeces__['azimuth']]
    final_shape = elevation.shape
    elevation = elevation.flatten()
    azimuth = azimuth.flatten()

    yaw = velocity[convention]['alpha_0']
    pitch = velocity[convention]['alpha_1']
    roll = velocity[convention]['alpha_2']
    dyaw = velocity[convention]['dalpha_0']
    dpitch = velocity[convention]['dalpha_1']
    droll = velocity[convention]['dalpha_2']
    # Check if rotation are not too large
    # because we assume small rotation
    # according to Koenderink van Dorn
    if ((np.abs(dyaw) > np.pi / 2 and 2 * np.pi - np.abs(dyaw) > np.pi / 2) or
        (np.abs(dpitch) > np.pi / 2 and 2 * np.pi - np.abs(dpitch) > np.pi / 2) or
            (np.abs(droll) > np.pi / 2 and 2 * np.pi - np.abs(droll) > np.pi / 2)):
        raise ValueError('rotation exceeds 90°, computation aborted')
    # we init a matrix for rot
    rof = np.zeros_like(elevation)
    hof = np.zeros_like(rof)
    vof = np.zeros_like(rof)
    # Calculate the angular velocities
    angvel = angular_velocity(yaw, pitch, roll,
                              dyaw, dpitch, droll, convention)
    M = compose_matrix(angles=[yaw, pitch, roll], translate=None,
                       perspective=None, axes=convention)[:3, :3]
    angvel_bee = np.dot(M, angvel)
    # The spline express in the bee coordinate system
    spline = np.array(spherical_to_cartesian(elevation, azimuth))
    # the Rotation-part of the Optic Flow in cartesian coord:
    # Cross product of angvel_bee and spline
    opticFlowR = np.zeros_like(spline)
    opticFlowR[2, :] = angvel_bee[0] * \
        spline[1, :] - angvel_bee[1] * spline[0, :]
    opticFlowR[1, :] = angvel_bee[2] * \
        spline[0, :] - angvel_bee[0] * spline[2, :]
    opticFlowR[0, :] = angvel_bee[1] * \
        spline[2, :] - angvel_bee[2] * spline[1, :]
    opticFlowR = -opticFlowR
    # opticFlow in spherical coordinate system
    (rof, hof, vof) = cartesian_to_spherical_vectors(
        opticFlowR, [azimuth, elevation])
    # Reshape according to eye
    rof = np.reshape(rof, final_shape)
    hof = np.reshape(hof, final_shape)
    vof = np.reshape(vof, final_shape)
    return rof, hof, vof


def optic_flow_translational(distance, viewing_directions,
                             velocity):
    """ translational optic flow
    : param distance: distance to objects
    : param viewing_directions: viewing direction of each pixel
           (azimuth, elevation)
    : param velocity: pandas series
                     (x, y, z, alpha, beta, gamma, dx,
                      dy, dz, dalpha, dbeta, dgamma)
    """
    if np.any(distance.shape != viewing_directions.shape[:-1]):
        msg = 'distance and viewing_directions should have the same size'
        msg += '{} != {}'.format(distance.shape,
                                 viewing_directions.shape[:-1].shape)
        raise ValueError(msg)
    passindex, convention = _check_optic_flow_param(viewing_directions,
                                                    velocity)
    elevation = viewing_directions[..., __spherical_indeces__['elevation']]
    azimuth = viewing_directions[..., __spherical_indeces__['azimuth']]
    final_shape = elevation.shape
    elevation = elevation.flatten()
    azimuth = azimuth.flatten()
    yaw = velocity[convention]['alpha_0']
    pitch = velocity[convention]['alpha_1']
    roll = velocity[convention]['alpha_2']
    # optic flow depnd of distance
    distance = distance.copy().flatten()
    distance[distance == 0] = np.nan  # Contact with object
    # and translational velocity
    # Express in the global coordinate system
    u = [velocity['location']['dx'],
         velocity['location']['dy'],
         velocity['location']['dz']]
    v = np.linalg.norm(u)
    if(v == 0):
        u = [0, 0, 0]
    else:
        u = u / np.linalg.norm(u)
    # we init a matrix for rot
    # we init a matrix for rot
    rof = np.zeros_like(elevation)
    hof = np.zeros_like(rof)
    vof = np.zeros_like(rof)
    # transformation
    M = compose_matrix(angles=[yaw, pitch, roll], translate=None,
                       perspective=None, axes=convention)[:3, :3]
    u_bee = M.dot(u)
    # The spline express in the bee coordinate system
    spline = np.array(spherical_to_cartesian(elevation, azimuth))
    # the Translation-part of the Optic Flow:
    dotvu = v * u_bee
    # cross product
    crossprod = np.zeros_like(spline)
    crossprod[2, :] = spline[0, :] * dotvu[1] - spline[1, :] * dotvu[0]
    crossprod[1, :] = spline[2, :] * dotvu[0] - spline[0, :] * dotvu[2]
    crossprod[0, :] = spline[1, :] * dotvu[2] - spline[2, :] * dotvu[1]
    # Calc opticFlow in cartesian coordinate system
    opticFlowT = np.zeros_like(spline)
    opticFlowT[2, :] = crossprod[0, :] * \
        spline[1, :] - crossprod[1, :] * spline[0, :]
    opticFlowT[1, :] = crossprod[2, :] * \
        spline[0, :] - crossprod[0, :] * spline[2, :]
    opticFlowT[0, :] = crossprod[1, :] * \
        spline[2, :] - crossprod[2, :] * spline[1, :]
    opticFlowT = -opticFlowT
    # opticFlow in spherical coordinate system
    (rof, hof, vof) = cartesian_to_spherical_vectors(
        opticFlowT, [azimuth, elevation])
    # Divide  by distance
    rof /= distance
    hof /= distance
    vof /= distance
    # Reshpae according to eye
    rof = np.reshape(rof, final_shape)
    hof = np.reshape(hof, final_shape)
    vof = np.reshape(vof, final_shape)
    return rof, hof, vof


def optic_flow(distance, viewing_directions, velocity):
    """ optic flow
    : param distance: distance to surrounding objects
    : param viewing_directions: viewing direction of each pixel
           (azimuth, elevation)
    : param velocity: pandas series
                     (x, y, z, alpha, beta, gamma, dx,
                      dy, dz, dalpha, dbeta, dgamma)
    """
    rofr, hofr, vofr = optic_flow_rotationonal(viewing_directions, velocity)
    roft, hoft, voft = optic_flow_translational(distance, viewing_directions,
                                                velocity)
    return rofr + roft, hofr + hoft, vofr + voft


class Module():
    """
    This class represents a Module that functions as a storage
    """

    def __init__(self, size=(180, 360)):
        """
        initializes the storage as an np.ndarray containing zeros
        of size size
        : param size: the tupel containing the size of the
                     storage(Input)
        """
        if size is None:
            raise ValueError("size must not be None")
        if not isinstance(size, tuple):
            raise TypeError("size must be a tuple")
        if len(size) < 2:
            raise Exception("length of size must at least be two")
        self.size = size
        self.Input = np.zeros(size)

    @property
    def size(self):
        """
        getter for the the size field
        : returns size: size of the Input field
        : rtype tuple
        """
        return self.__size

    @size.setter
    def size(self, size):
        """
        setter for the size of the storage
        : param size: tuple that contains the size of the storage
        """
        if size is None:
            raise ValueError("size must not be None")
        if not isinstance(size, tuple):
            raise TypeError("size must be a tuple")
        if len(size) < 2:
            raise Exception("length of size must at least be two")
        self.__size = size

    @property
    def Input(self):
        """
        getter for the Input field
        : returns Input
        : rtype np.ndarray
        """
        return self.__Input

    @Input.setter
    def Input(self, Input):
        """
        setter for the Input field, automaticaly sets the
        the size field to the shape of the Input
        : param Input
        """
        if Input is None:
            raise ValueError("Input must not be None")
        if not isinstance(Input, np.ndarray):
            raise TypeError("Input must be np array")
        if len(Input.shape) < 2:
            raise Exception("Input must have at least 2 dimensions")
        if (Input.shape[0] < 1) and (Input.shape[1] < 1):
            raise Exception("Each dimension of the Input\
                             must have at least be of size one")
        self.__Input = Input
        self.size = Input.shape

    def update(self,):
        """"
        update function can be implemented for
        inheriting classes
        """
        pass


class lp(Module):
    """
    Implementation of a low pass filter
    """

    def __init__(self, tau, inM):
        """
        Initializes the lowpass filter, the size of the output is
        set to the size of the input signal(inM)
        : param tau: time constant of the filter
        : param freq: cut off frequence of the filter
        : param inM: Module that stores and represents the input signal
        """
        if not isinstance(tau, float) and isinstance(tau, int):
            raise ValueError("tau must be of type float or integer")
        if inM is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM, Module):
            raise ValueError("input Module must be of type Module")
        self.size = inM.size
        Module.__init__(self, self.size)
        self.inM = inM
        self.itau = tau

    @property
    def itau(self):
        """
        getter of the time constant which is
        calculated by 1000/(tau*freq)
        """
        return self.__itau

    @itau.setter
    def itau(self, itau):
        """
        setter of the time constant
        : param itau: time constant
        """
        if not isinstance(itau, float) and isinstance(itau, int):
            raise ValueError("itau must be of type float or integer")
        self.__itau = itau

    @property
    def inM(self):
        """
        setter of the input Module
        : returns inM
        : rtype Module
        """
        return self.__inM

    @inM.setter
    def inM(self, inM):
        """
        setter of the input Module
        : param inM
        """
        if inM is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM, Module):
            raise ValueError("input Module must be of type Module")
        self.__inM = inM

    def update(self,):
        """
        update functions, updates the filtered signal for the
        the current input signal. out_t+1 += tau*(input-out_t)
        """
        In = self.inM.Input
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.Input[i, j] += self.itau * (In[i, j] - self.Input[i, j])


class hp(Module):  # for second order just take hp for inM
    """
    Implements a high pass filter
    """

    def __init__(self, tau, inM):
        """
        Initializes the high pass filter
        : param tau: time constant
        : param freq: cut off frequency
        : param inM: Module that stores the input signal
        """
        if not isinstance(tau, float) and isinstance(tau, int):
            raise ValueError("tau must be of type float or integer")
        if inM is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM, Module):
            raise ValueError("input Module must be of type Module")
        self.size = inM.size
        Module.__init__(self, self.size)
        self.inM = inM
        self.lowpass = lp(tau, inM)

    @property
    def inM(self):
        """
        getter for the input Module
        : returns inM
        : rtype Module
        """
        return self.__inM

    @inM.setter
    def inM(self, inM):
        """
        setter for the input Module
        : param inM: input Module for the input signal
        """
        if inM is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM, Module):
            raise ValueError("input Module must be of type Module")
        self.__inM = inM

    def update(self,):
        """
        updates the output signal with the current input signal
        out_t+1 = Input-lowpass(Input)
        """
        self.inM.update()
        self.lowpass.update()
        lpOut = self.lowpass.Input
        In = self.inM.Input
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.Input[i, j] = (In[i, j] - lpOut[i, j])


class mul(Module):
    """
    Implements the multiplication of two Modules
    """

    def __init__(self, inM1, inM2):
        """
        Initializes the multiplication module
        : param inM1: first input Module
        : param inM2: second input Module
        """
        if inM1 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM1, Module):
            raise ValueError("input Module must be of type Module")
        if inM2 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM2, Module):
            raise ValueError("input Module must be of type Module")
        Module.__init__(self, inM1.size)
        self.inM1 = inM1
        self.inM2 = inM2

    @property
    def inM1(self):
        """
        getter for the first input Module
        : returns inM1
        : rtype Module
        """
        return self.__inM1

    @inM1.setter
    def inM(self, inM1):
        """
        setter for the first input Module
        : param inM1
        """
        if inM1 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM1, Module):
            raise ValueError("input Module must be of type Module")
        self.__inM1 = inM1

    @property
    def inM2(self):
        """
        getter for the second input Module
        : returns inM2
        : rtype Module
        """
        return self.__inM2

    @inM2.setter
    def inM2(self, inM2):
        """
        setter for the first input Module
        : param inM1
        """
        if inM2 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM2, Module):
            raise ValueError("input Module must be of type Module")
        self.__inM2 = inM2

    def update(self, shift, axis=None):
        """
        updates the output(multiplication of the two input Modules)
        for the current input(see numpy roll)
        : param shift: shifts the Input provided by the first module
                      by the given amount
        : param axis: shifts the Input of the first module along the
                     provided axis
        """
        if not isinstance(shift, int):
            raise TypeError("shift must be an integer")
        if axis is not None:
            if not isinstance(axis, int):
                raise TypeError("axis must be of type integer")
        shiftedInput = np.roll(self.inM1.Input, shift, axis)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                sig_left1 = self.inM1.Input[i, j]
                sig_left2 = shiftedInput[i, j]
                self.Input[i, j] = sig_left1 * sig_left2


class div(Module):
    """
    Implements the division of two Modules
    """

    def __init__(self, inM1, inM2):
        """
        Initializes the multiplication module
        : param inM1: first input Module
        : param inM2: second input Module
        """
        if inM1 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM1, Module):
            raise ValueError("input Module must be of type Module")
        if inM2 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM2, Module):
            raise ValueError("input Module must be of type Module")
        Module.__init__(self, inM1.size)
        self.inM1 = inM1
        self.inM2 = inM2

    @property
    def inM1(self):
        """
        getter for the first input Module
        : returns inM1
        : rtype Module
        """
        return self.__inM1

    @inM1.setter
    def inM(self, inM1):
        """
        setter for the first input Module
        : param inM1
        """
        if inM1 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM1, Module):
            raise ValueError("input Module must be of type Module")
        self.__inM1 = inM1

    @property
    def inM2(self):
        """
        getter for the second input Module
        : returns inM2
        : rtype Module
        """
        return self.__inM2

    @inM2.setter
    def inM2(self, inM2):
        """
        setter for the first input Module
        : param inM1
        """
        if inM2 is None:
            raise ValueError("input Module must not be None")
        if not isinstance(inM2, Module):
            raise ValueError("input Module must be of type Module")
        self.__inM2 = inM2

    def update(self, shift, axis=None):
        """
        updates the output(division of the two input Modules)
        for the current input(see numpy roll)
        : param shift: shifts the Input provided by the first module
                      by the given amount
        : param axis: shifts the Input of the first module along the
                     provided axis
        """
        if not isinstance(shift, int):
            raise TypeError("shift must be an integer")
        if axis is not None:
            if not isinstance(axis, int):
                raise TypeError("axis must be of type integer")
        shiftedInput = np.roll(self.inM1.Input, shift, axis)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                sig_left1 = self.inM1.Input[i, j]
                sig_left2 = shiftedInput[i, j]
                if sig_left2 != 0:
                    self.Input[i, j] = sig_left1 / sig_left2
                else:
                    self.Input[i, j] = 0
