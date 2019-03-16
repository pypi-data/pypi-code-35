# -*- coding: utf-8 -*-
"""Contains classes for handling atmospheric temperature lapse rates."""
import abc
import numbers

import numpy as np
from scipy.interpolate import interp1d
from typhon.physics import vmr2mixing_ratio

from konrad import constants
from konrad.component import Component
from konrad.physics import saturation_pressure


class LapseRate(Component, metaclass=abc.ABCMeta):
    """Base class for all lapse rate handlers."""
    @abc.abstractmethod
    def __call__(self, atmosphere):
        """Return the atmospheric lapse rate.

        Parameters:
              T (ndarray): Atmospheric temperature [K].
              p (ndarray): Atmospheric pressure [Pa].

        Returns:
              ndarray: Temperature lapse rate [K/m].
        """


class MoistLapseRate(LapseRate):
    """Moist adiabatic temperature lapse rate."""
    def __init__(self, fixed=False):
        """Initialize a moist-adiabatic lapse rate component.

        Parameters:
            fixed (bool): If `True` the moist adiabatic lapse rate is only
                calculated for the first time step and kept constant
                afterwards.
        """
        self.fixed = fixed
        self._lapse_cache = None

    def __call__(self, atmosphere):
        if self._lapse_cache is not None:
            return self._lapse_cache

        T = atmosphere['T'][0, :]
        p = atmosphere['plev'][:]
        phlev = atmosphere['phlev'][:]

        # Use short formula symbols for physical constants.
        g = constants.earth_standard_gravity
        L = constants.heat_of_vaporization
        Rd = constants.specific_gas_constant_dry_air
        Rv = constants.specific_gas_constant_water_vapor
        Cp = constants.isobaric_mass_heat_capacity

        gamma_d = g / Cp  # dry lapse rate

        w_saturated = vmr2mixing_ratio(saturation_pressure(T) / p)

        gamma_m = (gamma_d * ((1 + (L * w_saturated) / (Rd * T)) /
                              (1 + (L**2 * w_saturated) / (Cp * Rv * T**2))
                              )
        )
        lapse = interp1d(p, gamma_m, fill_value='extrapolate')(phlev[:-1])

        if self.fixed:
            self._lapse_cache = lapse

        return lapse


class FixedLapseRate(LapseRate):
    """Fixed linear lapse rate through the whole atmosphere."""
    def __init__(self, lapserate=0.0065):
        """Create a handler with fixed linear temperature lapse rate.

        Parameters:
              lapserate (float or ndarray): Critical lapse rate [K/m].
        """
        self.lapserate = lapserate

    def __call__(self, atmosphere):
        if isinstance(self.lapserate, numbers.Number):
            T = atmosphere['T'][0, :]
            return self.lapserate * np.ones(T.size)
        elif isinstance(self.lapserate, np.ndarray):
            return self.lapserate
