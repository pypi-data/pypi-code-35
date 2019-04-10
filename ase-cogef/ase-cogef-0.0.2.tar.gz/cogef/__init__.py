# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Module cogef.

"""
from cogef.vibrations import SpringVib, SpringInf
from cogef.probability import load_rate_constants, load_all_rate_constants
from cogef.probability import load_external_forces
from cogef.probability import load_all_external_forces
from cogef.probability import load_mean_distances_intact
from cogef.probability import load_mean_distances, Minima
from cogef.probability import probability_density, rupture_force_from_dpdf
from cogef.probability import rupture_force_and_uncertainty_from_dpdf
from cogef.probability import constant_velocity
from cogef.probability import probability_density_polymer
from cogef.probability import probability_density_polymer2
from cogef.cogef1d import COGEF, do_nothing
from cogef.dissociation import force_factor
from cogef.dissociation import Dissociation, estimate_force_change
from cogef.cogef2d import COGEF2D, do_nothing2d
from cogef.dissociation2d import Dissociation2d
from cogef.cogef2in1 import COGEF2IN1, do_nothing2in1
from cogef.dcogef import DCOGEF, DCOGEF2D, DCOGEF2IN1

__version__ = '0.0.2'

__all__ = ['SpringVib', 'SpringInf', 'load_rate_constants',
           'load_all_rate_constants', 'load_external_forces',
           'load_all_external_forces',
           'load_mean_distances_intact', 'load_mean_distances', 'Minima',
           'probability_density', 'rupture_force_from_dpdf',
           'rupture_force_and_uncertainty_from_dpdf', 'constant_velocity',
           'probability_density_polymer', 'probability_density_polymer2',
           'COGEF', 'Dissociation', 'estimate_force_change', 'do_nothing',
           'force_factor',
           'COGEF2D', 'Dissociation2d', 'do_nothing2d', 'COGEF2IN1',
           'do_nothing2in1', 'DCOGEF', 'DCOGEF2D', 'DCOGEF2IN1']
