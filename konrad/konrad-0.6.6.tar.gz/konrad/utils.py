"""Common utility functions. """
import copy
import logging
from datetime import timedelta
from numbers import Number

import numpy as np
import typhon as ty
from netCDF4 import Dataset
from scipy.interpolate import interp1d

from konrad import constants


__all__ = [
    'append_description',
    'append_timestep_netcdf',
    'return_if_type',
    'phlev_from_plev',
    'dz_from_z',
    'refined_pgrid',
    'get_pressure_grids',
    'ozonesquash',
    'ozone_profile_rcemip',
    'humidity_profile_rcemip',
    'parse_fraction_of_day',
    'standard_atmosphere',
    'prefix_dict_keys',
]

logger = logging.getLogger(__name__)


def append_description(dataset, description=None):
    """Append variable attributes to a given dataset.

    Parameters:
          dataset (xarray.Dataset): Dataset including variables to describe.
          description (dict): Dictionary containing variable descriptions.
            The keys are the variable keys used in the Dataset.
            The values are dictionaries themselves containing attributes
            and their names as keys, e.g.:
                desc = {'T': {'units': 'K', 'standard_name': 'temperature'}}
    """
    if description is None:
        description = constants.variable_description

    for key in dataset.variables:
        if key in description:
            dataset[key].attrs = constants.variable_description[key]


def append_timestep_netcdf(filename, data, timestamp):
    """Append a timestep to an existing netCDF4 file.

    Notes:
        The variables to append to have to exist in the netCDF4 file!

    Parameters:
        filename (str): Path to the netCDF4.
        data (dict{ndarray}): Dict-like object containing the data arrays.
            The key is the variable name and the value is an ``ndarray``, a
            ``pandas.Series`` or an ``xarray.DataArray`` e.g.:
                >>> data = {'T': np.array([290, 295, 300])}

        timestamp (float): Timestamp of values appended.
    """
    # Open netCDF4 file in `append` mode.
    with Dataset(filename, 'a') as nc:
        logging.debug('Append timestep to "{}".'.format(filename))
        t = nc.dimensions['time'].size  # get index to store data.
        nc.variables['time'][t] = timestamp  # append timestamp.

        # Append values for each data variable in ``data``.
        for var in data.data_vars:
            # Append variable if it has a `time` dimension.
            if 'time' in nc[var].dimensions:
                # TODO: Find a cleaner way to handle different data dimensions.
                if 'plev' in nc[var].dimensions:
                    if hasattr(data[var], 'values'):
                        nc.variables[var][t, :] = data[var].values
                    else:
                        nc.variables[var][t, :] = data[var]
                else:
                    if hasattr(data[var], 'values'):
                        nc.variables[var][t] = data[var].values
                    else:
                        nc.variables[var][t] = data[var]


def return_if_type(variable, variablename, expect, default):
    """Return a variable if it matches an expected type.

    Parameters:
          variable: Variable to check.
          variablename (str): Variable name for error message.
          expect (type): Expected variable type.
          default: Default value, if varibale is ``None``.

    Raises:
          TypeError: If variable does not match expected type.
    """
    if variable is None:
        # use a surface with heat capacity as default.
        variable = default
    elif not isinstance(variable, expect):
        raise TypeError(
            'Argument `{name}` has to be of type `{type}`.'.format(
                name=variablename, type=expect.__name__)
        )

    return variable


def phlev_from_plev(fulllevels):
    """Returns the linear interpolated halflevels for given array.

    Parameters:
        fulllevels (ndarray): Pressure at fullevels.

    Returns:
        ndarray: Coordinates at halflevel.

    """
    plev_log = np.log(fulllevels)  # Perform inter-/extrapolation in log-space

    inter = 0.5 * (plev_log[1:] + plev_log[:-1])
    bottom = plev_log[0] + 0.5 * (plev_log[0] - plev_log[1])
    top = plev_log[-1] - 0.5 * (plev_log[-2] - plev_log[-1])

    return np.exp(np.hstack((bottom, inter, top)))


def dz_from_z(z):
    """
    Return the level thickness given the height array.

    Parameters:
        z (ndarray): Height of each model level [m]

    Returns:
        ndarray: Thickness of model levels [m]
    """
    dz = np.hstack([z[0], np.diff(z)])  # TODO: is this a good approx?
    return dz


def refined_pgrid(start, stop, num=200, shift=0.5, fixpoint=0.):
    """Create a pressure grid with adjustable distribution in logspace.

    Notes:
          Wrapper for ``typhon.math.squeezable_logspace``.

    Parameters:
        start (float): The starting value of the sequence.
        stop (float): The end value of the sequence.
        num (int): Number of sample to generate (Default is 50).
        shift (float): Factor with which the first stepwidth is
            squeezed in logspace. Has to be between  ``(0, 2)`.
            Values smaller than one compress the gridpoints,
            while values greater than 1 strecht the spacing.
            The default is ``0.5`` (bottom heavy.)
        fixpoint (float): Relative fixpoint for squeezing the grid.
            Has to be between ``[0, 1]``. The  default is ``0`` (bottom).

    Returns:
        ndarray: Pressure grid.
    """
    grid = ty.math.squeezable_logspace(
        start=start, stop=stop, num=num, squeeze=shift, fixpoint=fixpoint
    )

    return grid


def get_pressure_grids(start=1000e2, stop=1, num=200, squeeze=0.5):
    """Create matching pressure levels and half-levels.

    Parameters:
        start (float): Pressure of the lowest half-level (surface) [Pa].
        stop (float): Pressure of the highest half-level (TOA) [Pa].
        num (int): Number of **full** pressure levels.
        squeeze (float): Factor with which the first step width is
            squeezed in logspace. Has to be between ``(0, 2)``.
            Values smaller than one compress the half-levels,
            while values greater than 1 stretch the spacing.
            The default is ``0.5`` (bottom heavy.)

    Returns:
        ndarray, ndarray: Full-level pressure, half-level pressure [Pa].
    """
    phlev = ty.math.squeezable_logspace(start, stop, num + 1, squeeze=squeeze)
    plev = np.exp(0.5 * (np.log(phlev[1:]) + np.log(phlev[:-1])))

    return plev, phlev


def ozonesquash(o3, z, squash):
    """
    Squashes the ozone profile upwards or stretches it downwards, with no
        change to the shape of the profile above the ozone concentration maximum
    Parameters:
        o3 (ndarray): initial ozone profile
        z (ndarray): corresponding height values
        squash: float, with 1 being no squash,
            numbers < 1 squashing the profile towards the maximum,
            numbers > 1, stretching the profile downwards
    Returns:
        ndarray: new ozone profile
    """
    i_max_o3 = np.argmax(o3)

    sqz = (z[:i_max_o3] - z[i_max_o3])*squash + z[i_max_o3]
    new_o3 = copy.copy(o3)
    new_o3[:i_max_o3] = np.interp(z[:i_max_o3], sqz, o3[:i_max_o3])
    return new_o3


def ozone_profile_rcemip(plev, g1=3.6478, g2=0.83209, g3=11.3515):
    """Compute the ozone volumetric mixing ratio from pressure.

    .. math::
        O_3 = g_1 \cdot p^{g_2} e^\frac{-p}{g_3}

    Parameters:
        plev (ndarray): Atmospheric pressure [Pa].
        g1, g2, g3 (float): Fitting parameters for gamma distribution
            according to Wing et al. (2017).

    Returns:
          ndarray: Ozone profile [VMR].

    Reference:
        Wing et al., 2017, Radiative-Convective Equilibrium Model
        Intercomparison Project

    """
    p = plev / 100
    return g1 * p**g2 * np.exp(-p / g3) * 1e-6


def humidity_profile_rcemip(z, q0=18.65, qt=1e-11, zt=15000, zq1=4000,
                            zq2=7500):
    r"""Compute the water vapor volumetric mixing ratio as function of height.

    .. math::
        \mathrm{H_2O} = q_0
          \exp\left(-\frac{z}{z_{q1}}\right)
          \exp\left[\left(-\frac{z}{z_{q2}}\right)^2\right]

    Parameters:
        z (ndarray): Height [m].
        q0 (float): Specific humidity at the surface [g/kg].
        qt (float): Specific humidity in the stratosphere [g/kg].
        zt (float): Troposphere height [m].
        zq1, zq2 (float): Shape parameters.

    Returns:
        ndarray: Absolute humidity [VMR].

    Reference:
        Wing et al., 2017, Radiative-Convective Equilibrium Model
        Intercomparison Project

    """
    q = q0 * np.exp(-z / zq1) * np.exp(-(z / zq2) ** 2)

    q[z > zt] = qt

    return ty.physics.specific_humidity2vmr(q * 1e-3)


def parse_fraction_of_day(time):
    """Calculate the fraction of a day.

    Parameters:
        time (str or float): Specified time delta (e.g. '6h').
            Valid units:
                's' for seconds
                'm' for minutes
                'h' for hours
                'd' for days
                'w' for weeks
            If numeric, return value.

    Returns:
        float: Fraction of a day.

    Example:
        >>> parse_fraction_of_day('12h')
        0.5
    """
    mapping = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks',
    }

    if isinstance(time, str):
        value, period = float(time[:-1]), mapping[time[-1]]
        return timedelta(**{period: value}).total_seconds() / 3600 / 24
    elif isinstance(time, Number):
        return time


# TODO: Replace with ``typhon.physics.standard_atmosphere`` after next
#  typhon relase (>0.6.0).
def standard_atmosphere(z, coordinates='height'):
    """International Standard Atmosphere (ISA).

    The temperature profile is defined between 0-85 km (1089 h-0.004 hPa).
    Values exceeding this range are linearly interpolated.

    Parameters:
        z (float or ndarray): Geopotential height above MSL [m]
            or pressure [Pa] (see ``coordinates``).
        coordinates (str): Either 'height' or 'pressure'.

    Returns:
        ndarray: Atmospheric temperature [K].

    Examples:

        .. plot::
            :include-source:
            import numpy as np
            from typhon.plots import (profile_p_log, profile_z)
            from typhon.physics import standard_atmosphere
            from typhon.math import nlogspace
            z = np.linspace(0, 84e3, 100)
            fig, ax = plt.subplots()
            profile_z(z, standard_atmosphere(z), ax=ax)
            p = nlogspace(1000e2, 0.4, 100)
            fig, ax = plt.subplots()
            profile_p_log(p, standard_atmosphere(p, coordinates='pressure'))
            plt.show()
    """
    h = np.array([-610, 11000, 20000, 32000, 47000, 51000, 71000, 84852])
    p = np.array(
        [108_900, 22_632, 5474.9, 868.02, 110.91, 66.939, 3.9564, 0.3734]
    )
    temp = np.array([+19.0, -56.5, -56.5, -44.5, -2.5, -2.5, -58.5, -86.28])

    if coordinates == 'height':
        z_ref = h
    elif coordinates == 'pressure':
        z_ref = np.log(p)
        z = np.log(z)
    else:
        raise ValueError(
            f'"{coordinates}" coordinate is unsupported. '
            'Use "height" or "pressure".')

    return interp1d(z_ref, temp + 273.15, fill_value='extrapolate')(z)


def prefix_dict_keys(dictionary, prefix, delimiter='/'):
    """Return a copy of a dictionary with a prefix added to every key.

    Parameters:
        dictionary (dict): Input dictionary.
        prefix (str): Prefix to add to every key.
        delimiter (str): String used to separate prefix and original key.

    Returns:
        dict

    Example:
        >>> prefix_dict_keys({'bar': 42}, prefix='foo', delimiter='.')
        {'foo.bar': 42}

    """
    return {delimiter.join((prefix, key)): val
            for key, val in dictionary.items()}
