# Copyright (C) 2016-2019
# See accompanying license files for details.

"""Tests for cogef/probability.py

"""
from os.path import join
from numpy import array

from cogef import __path__
from cogef import load_rate_constants, load_all_rate_constants, Minima
from cogef import probability_density
from cogef import rupture_force_and_uncertainty_from_dpdf


# Class Minima

loading_rate = 10.
path = join(__path__[0], 'test')

print('\n' +
      '1) C6H14: 5 CC bonds, 3 different forward rates')
rates08, forces08 = load_rate_constants(join(path,
                                             'rate_0_8.dat'))  # outer bond
rates01, forces01 = load_rate_constants(join(path, 'rate_0_1.dat'))
rates12, forces12 = load_rate_constants(join(path,
                                             'rate_1_2.dat'))  # middle bond
forces = forces08
assert forces == forces01 and forces == forces12
# R -> P1
#   -> P2
#   -> P3
#   -> P4
#   -> P5
minima = Minima()
minima.add_destination(rates08)
minima.add_destination(rates01)
minima.add_destination(rates12)
minima.add_destination(rates01)
minima.add_destination(rates08)
dpdf = probability_density(minima, forces, loading_rate)
f_rup, f_err = rupture_force_and_uncertainty_from_dpdf(-array(dpdf[0]),
                                                       forces)
# Is final probability of reactant state zero?
assert minima.prob[0] < 1e-3
assert round(f_rup, 2) == 3.59
assert round(f_err, 2) == 0.05
print('Rupture force:')
print('(' + str(round(f_rup, 2)) + ' +- ' + str(round(f_err, 2)) + ') nN')

# ------------------------------------

print('\n' +
      '2) Spiropyran: two transitions with forward and backward rates ' +
      'respectively')
rates8_12, backrates8_12, forces8_12 = \
    load_all_rate_constants(join(path, 'rate_8_12.dat'))
rates29_11, backrates29_11, forces29_11 = \
    load_all_rate_constants(join(path, 'rate_29_11.dat'))
forces = forces8_12
assert forces == forces29_11
# R <-> I <-> P
minima = Minima()
minima.set_position(minima.add_destination(rates8_12, backrates8_12))
minima.add_destination(rates29_11, backrates29_11)
dpdf = probability_density(minima, forces, loading_rate)
f_rup, f_err = rupture_force_and_uncertainty_from_dpdf(-array(dpdf[0]),
                                                       forces)
assert minima.prob[0] < 1e-3
assert round(f_rup, 2) == 0.32
assert round(f_err, 2) == 0.09
print('Rupture force:')
print('(' + str(round(f_rup, 2)) + ' +- ' + str(round(f_err, 2)) + ') nN')

# ------------------------------------

print('\n' +
      '3) More complex spiropyran system')
rates_sp_inter, backrates_sp_inter, forces_sp_inter = \
    load_all_rate_constants(join(path, 'rate_SP-INTER.dat'))
rates_inter_ctc, backrates_inter_ctc, forces_inter_ctc \
    = load_all_rate_constants(join(path, 'rate_INTER-CTC.dat'))
rates_inter_ttc, backrates_inter_ttc, forces_inter_ttc \
    = load_all_rate_constants(join(path, 'rate_INTER-TTC.dat'))
rates_ctc_ttc, backrates_ctc_ttc, forces_ctc_ttc \
    = load_all_rate_constants(join(path, 'rate_CTC-TTC.dat'))
rates_ctc_ccc, backrates_ctc_ccc, forces_ctc_ccc \
    = load_all_rate_constants(join(path, 'rate_CTC-CCC.dat'))
forces = forces_sp_inter
assert forces == forces_inter_ctc and \
    forces == forces_inter_ttc and \
    forces == forces_ctc_ttc and \
    forces == forces_ctc_ccc
# SP <-> inter. <-> CTC <-> CCC
#                    ^
#                    |
#                    v
#               <-> TTC
minima = Minima()
minima.set_position(minima.add_destination(rates_sp_inter,
                                           backrates_sp_inter))
ctc = minima.add_destination(rates_inter_ctc,
                             backrates_inter_ctc)
ttc = minima.add_destination(rates_inter_ttc,
                             backrates_inter_ttc)
minima.set_position(ctc)
minima.add_destination(rates_ctc_ttc, backrates_ctc_ttc, ttc)
minima.add_destination(rates_ctc_ccc, backrates_ctc_ccc)
dpdf, probs = probability_density(minima, forces, loading_rate=1e-2,
                                  return_probs=True)
assert len(probs) == len(minima.system)
f_rup, f_err = rupture_force_and_uncertainty_from_dpdf(-array(dpdf[0]),
                                                       forces)
assert minima.prob[0] < 1e-3
assert round(f_rup, 3) == 0.035
assert round(f_err, 3) == 0.008
print('Rupture force:')
print('(' + str(round(f_rup, 3)) + ' +- ' + str(round(f_err, 3)) + ') nN')
print('Maximum probabilities during the transition:')
for i, name in enumerate(['SP', 'Inter.', 'CTC', 'TTC', 'CCC']):
    print(name + ': ' + str(max(probs[i])))
