"""This script is meant to help planning a paired-comparison experiment,
providing a preliminary Sample Size Determination (SSD).

Calculations are based on simulations of several complete group experiments
with exactly TWO test objects, A and B.

*** Usage: Edit this template script as desired and run it.

*1: Guess anticipated population quality means as (m_A, m_B) = (0., m_diff), where

m_diff = a preliminary estimate of the true MEAN quality difference in the population,
    in Thurstone d-prime scale units.
q_std = a preliminary estimate of INTER-INDIVIDUAL STANDARD DEVIATIONS for
    independent individual quality values (q_A, q_B) for objects A and B,
    in Thurstone d-prime scale units.
    Thus, std(q_B - q_A) ==  q_std * sqrt(2) in the population.

*2: Specify the intended test procedure in a PairedCompFrame instance

*3: Choose desired performance parameters (p_true_pos, p_false_pos),
    if different from the default values (0.9, 0.05)

*4: Estimate an approximate number of participants needed,
    by calling function estimate_n_subjects

*5: Estimate the resulting performance measures more accurately,
    by calling power_ab_mean.

If desired, estimate the ability of the experiment to detect the quality difference
    for a single individual randomly drawn from the population,
    by calling power_ab_individual

NOTE: The power calculations are rather slow, because they
run complete model learning procedures for many simulated data sets.
The script might take an hour or so to finish.


*** Definition of performance measures

p_true_pos = probability that the estimated quality difference is > 0,
    given the anticipated true m_diff and q_std in the population.
p_false_pos = probability that the estimated quality difference given true ZERO difference,
    is greater than the anticipated value of m_diff.

Thus, these two measures are symmetrically defined:
IFF the estimated posterior distributions of quality parameters
would be exactly EQUAL, except for the location,
for both the NULL and DIFFERENT populations models, we would get
p_true_pos = 1. - p_false_pos.

NOTE: The accuracy of the resulting performance measures is quite crude.
Better accuracy can be achieved by increasing the parameter n_sim
in function calls, at a cost of longer computation time.
In any case, it is a good practice to run the power calculation twice,
to see the variability of estimated results.

Finally, it is recommended to also simulate a complete experiment and result analysis
using the script run_sim.py.
This will generate an example of all analysis results for the planned experiment.


*** Method Discussion and References: See module pc_planning.py

*** Version History:
2018-08-08, first functional version
2019-04-03, modified to use updated modules pc_simulation, pc_planning
2019-04-06, include SSD assuming ideal exact quality measurements
"""

import logging
from pathlib import Path

from PairedCompCalc import pc_logging
from PairedCompCalc.pc_data import PairedCompFrame
from PairedCompCalc import pc_planning as pcp


# ------------------------------- Set up result logging:

pc_logging.setup(result_path=Path.home() / 'Documents' / 'PairedComp_plan',  # or whatever...
                 log_file='run_plan.log')  # to save the log file
# OR
# pc_logging.setup()  # to get only console output

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ------------------------------- Define Anticipated Population Properties:
m_diff = 0.5
# = mean quality difference B - A in the population, Thurstone d-prime units

q_std = 1.
# = inter-individual standard deviations for objects A and B in the population
# Thus, the standard deviation of the difference is std(q_B - q_A) = q_std * sqrt(2)

# ------------------------------- Define Experimental Procedure:

n_difference_grades = 4
pcf = PairedCompFrame(attributes=['SimQ'],
                      objects=['A', 'B'],
                      difference_grades=[f'Diff{i}' for i in range(n_difference_grades)],
                      forced_choice=False)

n_pres = 6
# = Number of pair presentations for each test participant

# ------------------------------ Ideal Sample Size Determination (SSD), assuming exact measurements:

p_true_crit = 0.9
p_false_crit = 0.05
# (n_aubj_ideal, p1, p0) = pcp.ideal_n_subjects(m_diff, q_std,
n_subj_ideal = pcp.ideal_n_subjects(m_diff, q_std,
                                    n_min=3,
                                    n_max=50,
                                    p_true_pos=p_true_crit,
                                    p_false_pos=p_false_crit,
                                    n_sim=1000)

logger.info(f'Ideal measurements with {n_subj_ideal} subjects,' +
            f' with true difference mean = {m_diff:.1f}, object std. = {q_std:.1f},\n' +
            f'\t\t would achieve p_true_pos > {p_true_crit:.1%}; p_false_pos < {p_false_crit:.1%}')

# ------------------------------ Crude Experimental Sample Size Determination (SSD):
# may be omitted, just use the ideal estimate instead.
n_estim = n_subj_ideal

# logger.info(f'*** Estimating Needed Experimental Sample Size,' +
#             f' assuming true difference mean = {m_diff:.1f}, object std. = {q_std:.1f}')
# logger.info(f'*** Using {n_difference_grades} difference grades, forced_choice={pcf.forced_choice},' +
#             f' {n_pres} pair presentations:')
#
# n_estim = pcp.estimate_n_subjects(pcf, m_diff, q_std, n_pres,
#                                   n_min=3,
#                                   n_max=2 * n_subj_ideal,
#                                   p_true_pos=0.9,
#                                   p_false_pos=0.05,
#                                   n_sim=5)

# ------------------------------ Performance Measures with better precision:

logger.info(f'*** Estimating Test Performance for Population Mean,' +
            f' assuming true difference mean = {m_diff:.1f}, object std. = {q_std:.1f}')

(p_true_pos, p_false_pos) = pcp.power_ab_mean(pcf, m_diff, q_std, n_estim, n_pres,
                                              n_sim=10)

logger.info(f'*** Using {n_difference_grades} difference grades, forced_choice={pcf.forced_choice},' +
            f' {n_pres} pair presentations:')
result_log = (f'Estimated Performance for Population Mean with {n_estim} tested subjects:\n' +
              f'p_true_pos = {p_true_pos:.1%}; p_false_pos = {p_false_pos:.1%}\n')

logger.info(result_log)

# ------------------------------ Optionally, estimate performance for Random Individual:

# logger.info(f'*** Estimating Performance for Population Individual,' +
#             f' assuming true difference mean = {m_diff:.1f}, object std. = {q_std:.1f}')
#
# (p_true_pos, p_false_pos) = pcp.power_ab_individual(pcf, m_diff, q_std, n_estim, n_pres,
#                                                           n_sim=10)
#
# logger.info(f'*** Using {n_difference_grades} difference grades, forced_choice={pcf.forced_choice},' +
#             f' {n_pres} pair presentations:')
# result_log = (f'Estimated Performance for Population Individual with {n_estim} tested subjects:\n' +
#               f'p_true_pos = {p_true_pos:.1%}; p_false_pos = {p_false_pos:.1%}\n')
# logger.info(result_log)

# ------------------------------ Optionally, try a different experimental procedure:
# n_difference_grades = 3
# pcf = PairedCompFrame(attributes=['SimQ'],
#                       objects=['A', 'B'],
#                       difference_grades=[f'Diff{i}' for i in range(n_difference_grades)],
#                       forced_choice=True)
# logger.info(f'*** Using {n_difference_grades} difference grades, forced_choice={pcf.forced_choice},' +
#             f' {n_pres} pair presentations:')
# logger.info(f'*** Estimating Performance for Population Mean,' +
#             f' assuming true difference mean = {m_diff:.1f}, object std. = {q_std:.1f}')
#
# (p_true_pos, p_false_pos) = pcp.power_ab_mean(pcf, m_diff, q_std, n_estim, n_pres, n_sim=10)
#
# result_log = (f'Estimated Performance for Population Mean with {n_estim} tested subjects:\n' +
#               f'p_true_pos = {p_true_pos:.1%}; p_false_pos = {p_false_pos:.1%}\n')
# logger.info(result_log)

# ------------------------------ Compare with other experimental procedure:

n_difference_grades = 1
pcf = PairedCompFrame(attributes=['SimQ'],
                      objects=['A', 'B'],
                      difference_grades=[f'Diff{i+1}' for i in range(n_difference_grades)],
                      forced_choice=True)

logger.info(f'*** Estimating Performance for Population Mean,' +
            f' assuming true difference mean = {m_diff:.1f}, object std. = {q_std:.1f}')

(p_true_pos, p_false_pos) = pcp.power_ab_mean(pcf, m_diff, q_std, n_estim, n_pres,
                                              n_sim=10)

logger.info(f'*** Using {n_difference_grades} difference grades, forced_choice={pcf.forced_choice},' +
            f' {n_pres} pair presentations:')
result_log = (f'Estimated Performance for Population Mean with {n_estim} tested subjects:\n' +
              f'p_true_pos = {p_true_pos:.1%}; p_false_pos = {p_false_pos:.1%}\n')
logger.info(result_log)

logging.shutdown()
