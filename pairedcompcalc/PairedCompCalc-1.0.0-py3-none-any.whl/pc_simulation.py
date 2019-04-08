"""This module defines classes and methods for
simulated paired-comparison experiments with groups of test subjects,
drawn at random from population(s) with specified
inter-individual distributions of all model parameters.

The simulations can generate artificial data with exactly the same structure
as that obtained from a real experimental data set.


*** Main Module Classes:

PairedCompSimPopulation: defines distribution of model parameters
    for two or more tested Objects,
    in ONE population of subjects,
    for one or several perceptual Attributes,
    in one or several Test Conditions, each defined as
    a combination of one category from each Test Factor.

PairedCompSimExperiment: defines a paired-comparison experiment,
    and generates simulated responses for one or more groups of subjects,
    sampled from PairedComSimPopulation instance(s).

SubjectThurstone: single subject with decisions using the Thurstone Case V model

SubjectBradley: single subject with decisions using the Bradley-Terry-Luce (BTL) model


*** Module Function:

gen_dataset(...), generate a PairedCompDataSet object,
    containing simulated results from a simple experiment
    with only ONE subject group, for ONE perceptual Attribute, in ONE Test Condition.


*** Main Class Methods:

PairedCompSimPopulation.gen_subject_group(...)
    draws a group of simulated subjects at random from the Population.

PairedCompSimExperiment.gen_dataset(...)
    generates a pc_data.PairedCompDataSet instance with simulated paired-comparison results
    for one or more groups of simulated subjects.
    All data can be saved to files using the dataset.save(...) method.

*** Usage example: See script run_sim.py

*** Version History:
2018-03-18, allow inter-individual variations in simulated population
2018-04-27, changed internal simulator structure and call signatures
2018-08-13, adapted for new simplified PairedCompRecord structure
2018-10-02, modified for PairedCompFile structure
2018-12-09, allow several Test Conditions with different quality parameters
2018-12-09, allow several attributes with different quality parameters

2019-03-29, new classes PairedCompSimPopulation, PairedCompSimExperiment
            allow general simulation of a paired-comparison experiment
            with several subject Groups, perceptual Attributes, and Test Conditions.
2019-03-29, PairedCompSimPopulation can generate group of subjects with randomized
            quality parameters, response thresholds, and lapse probability,
            although default is fixed response thresholds and zero lapse probability.
"""
# *** allow different std:s of quality and response_intervals for each Attribute
#       Not necessary, same effect using different quality params...

import numpy as np
from scipy.stats import randint, uniform, norm
import itertools
import copy
import logging

from .safe_logistic import logistic

from .pc_data import StimRespItem
from .pc_data import PairedCompDataSet

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # test


# --------------------------------------- subject response models
class SubjectThurstone:
    """simulate one individual participant in a paired-comparison experiment.
    The subject responds using the Thurstone Case V choice model.
    """
    def __init__(self, quality, response_thresholds, lapse_prob=0.):
        """
        :param quality: 2D array with object quality values in Thurstone d-prime scale
            q[t, i] = quality of i-th object in t-th test condition
        :param response_thresholds: 1D array with non-negative response-interval lower limits,
            in Thurstone d-prime units
        :param lapse_prob: scalar probability of lapse response

        NOTE: in a forced_choice experiment, min(response_thresholds) == 0.,
        so response == 0 becomes impossible.
        """
        self.quality = quality
        # = individual quality params for this subject
        self.response_thresholds = response_thresholds
        self.lapse_prob = lapse_prob

    def __repr__(self):
        return (f'{self.__class__.__name__}(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    @property
    def n_response_magn(self):
        return len(self.response_thresholds) + 1

    def response(self, pair, tc_ind=0):
        """Simulate response to one paired-comparison presentation
        :param pair: tuple (i,j) with indices to self.quality
        :param tc_ind: test-condition index into self.quality
        :return: scalar integer r
            r is determined by decision variable x, as
            r = 0 iff -self.response_thresholds[0] < x < +self.response_thresholds[0]
                (i.e., cannot happen if self.response_thresholds[0] == 0, i.e., forced_choice)
            r = i iff self.response_thresholds[i-1] <= x < self.response_thresholds[i]
            r = -i iff -self.response_thresholds[i] < x <= -self.response_thresholds[i-1]
        """
        if self.lapse():
            return self.lapse_response()
        (i,j) = pair
        d = self.quality[tc_ind, j] - self.quality[tc_ind, i]
        x = self.decision_variable(d)
        return int(sum(abs(x) >= self.response_thresholds)) * (1 if x > 0 else -1)

    @staticmethod
    def decision_variable(d):
        """Generate one random decision variable from Thurstone model
        :param d: scalar quality difference in Thurstone d-prime units
        :return: scalar random variate of model sensory variable
        """
        return norm.rvs(loc=d, scale=np.sqrt(2))

    def lapse(self):
        """Generate True with prob = self.lapse_prob
        """
        return uniform.rvs(0, 1.) < self.lapse_prob

    def lapse_response(self):
        """Generate a random result, disregarding quality parameters
        :return: scalar integer
            in {-n_difference_grades, ...,-1, +1,..., + n_difference_grades}, if forced_choice
            in {-n_difference_grades+1, ...,0, ...,  + n_difference_grades-1}, if not forced_choice
            i.e., excluding 0 if self.pcf.forced_choice
        """
        n_response_limits = len(self.response_thresholds)
        # if self.pcf.forced_choice:
        if self.response_thresholds[0] == 0.:  # forced_choice
            return ((-1 if uniform.rvs() < 0.5 else +1) *
                    randint.rvs(low=1, high=n_response_limits + 1))

        else:
            return randint.rvs(low=-n_response_limits,
                               high=n_response_limits + 1)


class SubjectBradley(SubjectThurstone):
    """Simulate one individual participant in a paired-comparison experiment.
    The subject responds using the Bradley-Terry-Luce choice model,
    with parameters defined in the log domain.

    NOTE: to facilitate comparisons, the model is initialized by parameters
    defined in the THURSTONE scale, and transformed internally.
    """
    def __init__(self, *args, **kwargs):
        """
        :param args, kwargs: arguments for superclass, in d-prime units
        """
        super().__init__(*args, **kwargs)
        self.quality = thurstone2bradley(self.quality)
        self.response_thresholds = thurstone2bradley(self.response_thresholds)

    def decision_variable(self, d):
        """Generate one random decision variable from BTL model
        :param d: scalar quality difference in BTL units
        :return: scalar random variate of model sensory variable
        """
        return logistic.rvs(loc=d)


# --------------------------------------- simple simulator:
def gen_dataset(pcf,
                n_subjects,
                quality_mean,
                quality_std=0.,
                response_width_mean=1.,
                log_response_width_std=0.,
                lapse_prob_range=(0., 0.),
                subject_class=SubjectThurstone,
                n_replications=3,
                pair_different=True):
    """Generate data from a simple simulated paired-comparison experiment
    with ONE group of subjects, for ONE perceptual Attribute, in ONE Test Condition.
    :param pcf: a PairedCompFrame object defining experimental format
    :param n_subjects: scalar integer number of simulated subjects
    :param quality_mean: 1D array-like list of population mean quality parameters
    :param quality_std: scalar or array-like list with inter-individual st.deviations
    :param response_width_mean: scalar mean response interval width
    :param log_response_width_std: scalar st.deviation of log(response interval widths)
    :param lapse_prob_range: tuple (min, max) of individual lapse probability
    :param subject_class: class of subject model
    :param n_replications: scalar integer with number of comparisons (A, B),
        plus same number for (B, A)
    :param pair_different: boolean, allow only different objects to be compared

    :return: ds= single pc_data.PairedCompDataSet instance containing all simulated results

    NOTE: ds.save(...) may be called to store data in one file for each subject.
    """
    pcf = copy.deepcopy(pcf)
    # use local copy, so we do not modify caller's original.
    if pcf.objects is None:
        pcf.objects = [f'Obj{i}' for i in range(len(quality_mean))]
    if len(pcf.objects) != len(quality_mean):
        raise RuntimeError('Length of quality_mean must agree with number of objects')
    if len(pcf.attributes) > 1:
        logger.warning(f'Same population properties for attributes {pcf.attributes}')
        # This is allowed, but makes no sense really.
    if len(pcf.test_factors) > 0:
        pcf.test_factors = dict()
        logger.warning('Using only one un-named Test Condition')

    pc_pop = PairedCompSimPopulation(objects=pcf.objects,
                                     quality_mean={a:quality_mean
                                                   for a in pcf.attributes},
                                     quality_std=quality_std,
                                     response_width_mean=response_width_mean,
                                     log_response_width_std=log_response_width_std,
                                     lapse_prob_range=lapse_prob_range,
                                     subject_class=subject_class)
    pc_group = pc_pop.gen_subject_group(pcf, n_subjects=n_subjects)
    pc_exp = PairedCompSimExperiment(pcf,
                                     n_replications=n_replications,
                                     pair_different=pair_different)
    return pc_exp.gen_dataset(groups={'': pc_group})


# ----------------------------------- OLD Simulator Class:
# class PairedCompSimulator:
#     """Defines a simulated paired-comparison experiment.
#     Method run() generates and saves simulated data for one group of participants
#     drawn from a population with given properties.
#     Method gen_dataset() generates a PairedCompDataSet without saving any files.
#     """
#     # ******* Let user define response limits here, too !!!
#     # ******* separate classes for Population and PC_Simulator ???
#
#     def __init__(self, pcf,
#                  quality_mean,
#                  quality_std=0.,
#                  n_replications=3,  # i.e., 3 for (A, B) and 3 for (B, A)
#                  lapse_prob=0.,
#                  pair_different=True):
#         """
#         :param pcf: PairedCompFrame instance, defining experimental structure
#         :param quality_mean: dict with elements (attr, attr_quality), where
#             attr is a string label,
#             attr_quality = 1D or 2D array-like list with mean quality parameters
#             attr_quality[..., i] = quality for i-th object in ...-th test condition for this attribute.
#             ******** dict with test-conditions, too??? ******************
#         :param quality_std: scalar inter-individual standard deviation of quality parameters
#             in the simulated population; same value for all attributes, objects, test conditions.
#         :param n_replications: number of presentations of each ordered pair
#             NOTE: pair (A,B) and (B,A) are counted separately, so total number of
#             unordered A vs. B comparisons is 2 * n_replications
#         :param lapse_prob: probability of random lapse response
#         :param pair_different: boolean, allow only different objects to be compared
#         """
#         self.pcf = pcf
#         assert set(pcf.attributes) <= set(quality_mean.keys()), 'Missing attribute(s) in quality_mean'
#         self.quality_mean = quality_mean
#         # if self.quality_mean.shape[-1] != self.pcf.n_objects:
#         #     raise RuntimeError('Length mismatch for objects and quality parameters')
#         self.quality_std = quality_std
#         if self.pcf.forced_choice:
#             self.response_thresholds = np.arange(0., pcf.n_difference_grades, 1.)
#             # = upper limits of response intervals,
#             #   i.e. empty interval (-0., 0.) for non-allowed "zero" response
#         else:
#             self.response_thresholds = 0.5 + np.arange(0., pcf.n_difference_grades - 1, 1.)
#             # interval for "zero" difference is (-0.5, +0.5)
#         self.n_replications = n_replications
#         self.lapse_prob = lapse_prob
#         self.pair_different = pair_different
#         self.simulated_group = None   # {a: list() for a in self.pcf.attributes}
#         # empty lists to be filled with subject instances later
#
#     def __repr__(self):
#         return (f'{self.__class__.__name__}(\n\t' +
#                 ',\n\t'.join(f'{key}={repr(v)}'
#                              for (key, v) in vars(self).items()) +
#                 '\n\t)')
#
#     @property
#     def n_objects(self):
#         return self.pcf.n_objects
#
#     @property
#     def n_difference_grades(self):
#         return self.pcf.n_difference_grades
#
#     def gen_group_params(self, n_subjects):
#         """Generate random subject parameters for one group of subjects
#         :param n_subjects: integer number of subjects in the group
#         :return: None
#         Result: calculated parameters
#             self.quality = array of quality parameters
#             self.quality.shape == (n_subjects, *self.quality_mean.shape)
#         """
#         # ************* response_thresholds should also be individually randomized ???
#         # **** this should be done by separate SimPopulation object ???
#         self.simulated_group = dict()
#         for a in self.pcf.attributes:
#             m = np.array(self.quality_mean[a])
#             if m.ndim < 2:
#                 m = m.reshape((1, -1))
#             s = self.quality_std
#             a_quality = m + s * norm.rvs(size=(n_subjects, *m.shape))
#             a_quality -= a_quality[..., :1]
#             self.simulated_group[a] = a_quality
#
#     def gen_dataset(self, n_subjects=1,
#                     subject_class=SubjectThurstone,
#                     group=''):
#         """Generate a complete PairedCompDataSet for one experiment,
#         with ONE group of subjects drawn from given population,
#         and a complete set of comparisons for each subject.
#         :param n_subjects: number of participants
#         :param subject_class: probability model for decision variable
#         :param group: (optional) string name of this subject group
#         :return: a single PairedCompDataSet object
#
#         2018-08-13, simplified PairedCompDataSet dict nesting
#         """
#         def sim_one_subject(q):
#             """Generate data for ONE subject in all test conditions
#             for ONE externally known attribute
#             :param q: actual quality vector for this subject
#             :return: list of StimRespItem objects, one for each replication,
#                 for all required test conditions
#             """
#             res = self.run_one_session(subject_class(q, self.response_thresholds, self.lapse_prob))
#             return res
#         # ----------------------------------------------------------------
#         # ************* save subject instances in a list ????
#         subjects = [f'{group}Subject{i}' for i in range(n_subjects)]
#         self.gen_group_params(n_subjects)
#         pcd_g = {a: {s_id: sim_one_subject(q)
#                      # for (s_id, q) in zip(subjects, self.quality)}
#                      for (s_id, q) in zip(subjects, self.simulated_group[a])}
#                  for a in self.pcf.attributes}
#         return PairedCompDataSet(self.pcf, {group: pcd_g})
#
#     def run(self, n_subjects=1,
#             subject_class=SubjectThurstone,
#             result_path='./test',
#             group=''):
#         """run a complete simulated experiment
#         with ONE group of subjects drawn from given population.
#         :param n_subjects: number of participants
#         :param subject_class: probability model for decision variable
#         :param result_path: (optional) Path or string name of directory for result files.
#         :param group: (optional) string with group name
#         :return: None
#
#         Result: saved PairedCompDataSet in result_path, one file for each subject
#         """
#         ds = self.gen_dataset(n_subjects, subject_class, group)
#         ds.save(result_path)
#
#     def run_one_session(self, s):
#         """run_one_session wih one simulated subject in ALL test conditions
#         :param s: single SubjectThurstone or SubjectBradley instance
#         :return: list of StimRespItem objects with simulated responses
#         """
#         res = []
#         # = list of StimRespItem objects
#         for (tc_ind, tc) in enumerate(self.pcf.test_conditions()):
#             for ij in self.object_pairs():
#                 # ij = pair of object indices
#                 obj_pair = (self.pcf.objects[ij[0]], self.pcf.objects[ij[1]])
#                 res.extend([StimRespItem(obj_pair, s.response(ij, tc_ind), tc)
#                             for _ in range(self.n_replications)])
#         return res
#
#     def object_pairs(self):
#         """generator of all allowed pairs to be presented
#         Each pair is a tuple (i, j) with indices into self.pcf.objects
#         """
#         if self.pair_different:
#             return itertools.permutations(range(self.n_objects), 2)
#             # no pairs presented with equal system indices, like (1, 1)
#         else:
#             return itertools.product(range(self.n_objects), 2)
#             # pairs may include tuples with equal system indices, like (1, 1)


# -------------------------------------------------------------------------
class PairedCompSimPopulation:
    """Defines a simulated population
    from which groups of test subjects can be generated
    for a simulated paired-comparison experiment.

    The population instance defines a distribution of quality parameters for
    at least two objects to be evaluated by paired comparisons,
    for one or more perceptual attributes,
    in one or several Test Conditions.
    A subset of these can then be selected for use by actual test-subject groups.

    Each Test Condition is a combination of one category from each Test Factor.

    Property objects is a list of objects, for which population properties are defined.
    Property test_factors is a list of test-factor labels,
        one for each test-factor level in property quality_mean.
    Property quality_mean is a nested dict defining mean quality parameters
        for various Attributes and Test Conditions, as specified in method __init__.
    Property quality_std is the inter-individual standard deviation,
        same for all objects, attributes, and test conditions.
    Property response_width_mean is the mean width of all response intervals,
        same for all object pairs, attributes, and test conditions.
    Property log_response_width_std is the standard deviation of all log(response intervals),
        thus defining a log-normal distribution of response-interval widths,
        same for all object pairs, attributes, and test conditions.
        Default is fixed response intervals, with no inter-individual variations.
    Property lapse_prob_range defines uniform distribution of subject lapse probability,
        same for all object pairs, attributes, and test conditions.
    Property subject_class defines model class for simulated subjects.
    Property id is used as a prefix in names for all generated subjects.
    """
    def __init__(self,
                 objects,
                 quality_mean,
                 test_factors=None,
                 quality_std=0.,
                 response_width_mean=1.,
                 log_response_width_std=0.,
                 lapse_prob_range=(0., 0.),
                 subject_class=SubjectThurstone,
                 id=''):
        """
        :param objects: list of object labels
        :param quality_mean: nested dict with elements (attr, a_quality), where
            attr is a string label for one perceptual Attribute,
            a_quality = a nested dict with one level for each test_factor element, e.g.,
                {tc0_0: {tc1_0: quality_list_0_0,  # tf[0] = tc_0_0 AND tf[1] = tc_1_0
                         tc1_1: quality_list_0_1}, # tf[0] = tc_0_0 AND tf[1] = tc_1_1
                 tc0_1: {tc1_0: quality_list_1_0,  # tf[0] = tc_0_1 AND tf[1] = tc_1_0
                         tc1_1: quality_list_1_1}  # tf[0] = tc_0_1 AND tf[1] = tc_1_1
                etc., ... }
            quality_list is a list of quality parameters, one for each object, in d-prime units.
            len(quality_list_x_y...) == len(objects), for all x_y_...
            If test_factors is None or empty: a_quality = a single list of quality params,
                for one single unspecified test condition.
        :param test_factors: (optional) list of test_factor string labels
        :param quality_std: s(optional) scalar inter-individual standard deviation of quality parameters
        :param response_width_mean: (optional) scalar mean of response-interval-width
        :param log_response_width_std: (optional) scalar standard deviation of log(response-interval-width)
        :param lapse_prob_range: (optional) tupie (min, max) probability of random lapse response
        :param subject_class: (optional) subject probabilistic model for generating responses
        :param id: (optional) string label, used as prefix in all subject names
        """
        self.objects = objects
        if test_factors is None:
            test_factors = []
        self.test_factors = test_factors
        self.quality_mean = quality_mean
        self.quality_std = quality_std
        self.response_width_mean = response_width_mean
        self.log_response_width_std = log_response_width_std
        self.lapse_prob_range = lapse_prob_range
        self.subject_class = subject_class
        self.id = id

    def __repr__(self):
        return (f'{self.__class__.__name__}(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    def gen_subject_group(self, pcf, n_subjects=1):
        """Create a group of simulated-subject instances randomly drawn from self,
        with properties suitable for a planned experiment.
        :param pcf: a PairedCompFrame instance specifying the planned experiment
            Needed to select attributes and objects for testing,
            and to define response intervals for each subject included in the group.
        :param n_subjects: number of randomly drawn subjects from self
        :return: group = dict with elements (attribute, a_subjects), where
            attribute is an element in pcf.attributes
            a_subjects = a list of self.subject_class instances,
            each with quality properties randomly generated.

            NOTE: Several groups may be joined externally,
            in a dict with group names as keys.
        """
        self._check_properties(pcf)
        return {a: {self.id + f'_Subj{i}':
                        self.subject_class(self._rvs_q(a, pcf),
                                           self._rvs_response_thresholds(a, pcf),
                                           self._rvs_lapse_prob(a))
                    for i in range(n_subjects)}
                for a in pcf.attributes}

    # --------------------------------------- private help methods

    def _rvs_q(self, attr, pcf):
        """Generate random quality parameters in d-prime units, for subject definition
        :param attr: string label for desired Attribute
        :param pcf: PairedCompFrame object defining experiment
        :return: 2D array q, with
            q[t, i] = quality parameter for i-th object in t-th test condition
        """
        def mean_q(q, tf):
            """Parse nested q_dict to extract quality_mean in selected test conditions.
            :param q: recursively nested dict with elements (tc, sub_dict), where
                sub_dict is a list of quality params at deepest level, where len(tf)==0
            :param tf: list of remaining test factors to parse
                len(tf) == depth of nested dict q
            :return: q_list = nested list of lists of mean-quality parameters,
                corresponding to M-dimensional array with M = len(pcf.test_factors)
                np.array(q_list).shape == (*pcf.n_test_factor_categories, len(pcf.objects)
            """
            if len(tf) == 0:
                # at deepest recursion level: q is now a quality list, NOT a sub-dict
                if isinstance(q, dict):
                    raise RuntimeError('Levels of dict quality_mean must agree with len(test_factors)')
                if len(q) != len(self.objects):
                    raise RuntimeError('Mismatching len(quality_mean) != len(objects)')
                # must be checked for every extracted test condition
                return np.asarray(q)
            else:
                if tf[0] in pcf.test_factors.keys():
                    tf_tc = pcf.test_factors[tf[0]]
                    if any(tc not in q.keys()
                           for tc in tf_tc):
                        missing_tc = set(tf_tc) - set(q.keys())
                        err_msg = f'Test condition(s) {tf[0]}={missing_tc} undefined in population'
                        raise RuntimeError(err_msg)
                else:
                    tf_tc = q.keys()  # use ALL, and average later
                return [mean_q(q[tc], tf[1:])
                        for tc in tf_tc]
            # -------------------------------------------------

        tf = self.test_factors.copy()
        m = np.array(mean_q(self.quality_mean[attr], tf))
        # m[..., i] = self quality_mean for self.objects[i] in ...-th test condition
        object_ind = [self.objects.index(obj)
                      for obj in pcf.objects]
        m = m[..., object_ind]
        # m[..., i] = quality_mean for pcf.objects[i] in ...-th test condition
        for (i, tf_i) in enumerate(self.test_factors):
            if tf_i not in pcf.test_factors.keys():
                m = np.mean(m, axis=i)
                tf.remove(tf_i)
        tf_axes = [tf.index(tf_i)
                   for tf_i in pcf.test_factors.keys()] + [m.ndim-1]
        m = m.transpose(tf_axes)
        # to make sure m axis order corresponds to pcf.test_factors
        m = m.reshape((-1, len(pcf.objects)))
        # m[t, i] = mean quality for i-th object in t-th test condition, ordered as in pcf
        q = m + self.quality_std * norm.rvs(size=m.shape)
        q -= q[..., :1]
        # force quality == 0 for pcf.objects[0], because quality zero is arbitrary
        return q

    def _rvs_response_thresholds(self, attr, pcf):
        """Random response-category thresholds in d-prime units, for subject definition.
        For now, assumed same for all attributes
        :param attr: string label for desired Attribute
        :param pcf: PairedCompFrame object defining experiment
        :return: r_thr = 1D array = upper limits of response intervals, except highest = inf
        """
        r_widths = self.response_width_mean * np.ones(pcf.n_difference_grades - 1)
        # mean widhts, except for highest interval with width = inf
        r_widths *= np.exp(norm.rvs(scale=self.log_response_width_std, size=r_widths.shape))
        if pcf.forced_choice:
            r_thr = np.concatenate(([0.], np.cumsum(r_widths)))
            # = upper limits of response intervals,
            #   i.e. empty interval (-0., 0.) for non-allowed "zero" response
        else:
            r_widths[0] *= 0.5
            r_thr = np.cumsum(r_widths)
            # = upper limits of response intervals,
            # i.e., interval for allowed "zero" response is (-r_thr[0], r_thr[0])
        return r_thr

    def _rvs_lapse_prob(self, attr):
        """Random lapse probability, for subject definition.
        For now, assumed same for all attributes
        :param attr: string label for desired Attribute
        :return: scalar lapse_p parameter for subject definition
        """
        return np.random.uniform(low=min(self.lapse_prob_range),
                                 high=max(self.lapse_prob_range))

    def _check_properties(self, pcf):
        """Check required experiment consistency with population data
        :param pcf: PairedCompFrame object defining experiment
        :return: None
        Result: errors or logger warning in case of deviation
        """
        # ----- check attributes:
        pcf_attr = set(pcf.attributes)
        attr = set(self.quality_mean.keys())
        if len(pcf_attr - attr) > 0:
            raise RuntimeError(f'No population data for attribute(s) {pcf_attr - attr}')
        if pcf_attr < attr:
            logger.warning(f'Simulated subjects using subset of population attributes')

        # ----- check objects:
        pcf_obj = set(pcf.objects)
        obj = set(self.objects)
        if len(pcf_obj - obj) > 0:
            raise RuntimeError(f'No population data for object(s) {pcf_obj - obj}')
        if pcf_obj < obj:
            logger.warning(f'Simulated subjects using subset of population objects')

        # ----- check test factors:
        pcf_tf = set(pcf.test_factors.keys())
        tf = set(self.test_factors)
        if len(pcf_tf - tf) > 0:
            raise RuntimeError(f'No population data for test factor(s) {pcf_tf - tf}')
        if pcf_tf < tf:
            logger.warning(f'Simulated subjects using subset of population test factors')


# -------------------------------------------------------------------------
class PairedCompSimExperiment:
    """Defines a simulated paired-comparison experiment
    with one or more groups of simulated subjects, with
    each group generated from a separate PairedCompSimPopulation instance.

    Method gen_dataset() generates a complete set of paired-comparison results.

    The experimental procedure is defined by
    property pcf = a PairedCompFrame instance, and
    property n_replications = number of presentations of each ordered object pair,
    property pair_different = boolean switch, with
        default = True, forcing every presented pair to include different objects.
        Pairs with two equal objects might help estimating response thresholds,
        especially if tied responses are allowed, i.e., pcf.forced_choice=False.
    """
    def __init__(self, pcf,
                 n_replications=3,
                 pair_different=True):
        """
        :param pcf: PairedCompFrame instance, defining most experimental parameters
        :param n_replications: number of presentations of each ordered pair
            NOTE: pair (A,B) and (B,A) are counted separately, so total number of
            unordered A vs. B comparisons is 2 * n_replications
        :param pair_different: boolean, allow only different objects to be compared
        """
        self.pcf = pcf
        self.n_replications = n_replications
        self.pair_different = pair_different

    def __repr__(self):
        return (f'{self.__class__.__name__}(\n\t' +
                ',\n\t'.join(f'{key}={repr(v)}'
                             for (key, v) in vars(self).items()) +
                '\n\t)')

    def gen_dataset(self, groups):
        """Generate a complete PairedCompDataSet for one experiment,
        with one or more groups of subjects,
        and a complete set of comparisons for each subject.
        :param groups: nested dict with items (group_id, g_subjects), where
            group_id = a string with group name
            g_subjects is a dict with items (attr, a_subjects),
                as generated from PairedCompSimPopulation.gen_subject_group(...), where
            attr is an attribute label,
            a_subjects is a dict with (subject_id, subject_class_instance)
        :return: a single PairedCompDataSet object
        """
        pcd = {g: {a: {s_id: self.run_one_session(s)
                       for (s_id, s) in ga_subjects.items()}
                   for (a, ga_subjects) in g_subjects.items()}
               for (g, g_subjects) in groups.items()}
        return PairedCompDataSet(self.pcf, pcd)

    def run_one_session(self, s):
        """run_one_session wih one simulated subject in ALL test conditions
        :param s: single SubjectThurstone or SubjectBradley instance
        :return: list of StimRespItem objects with simulated responses
        """
        res = []
        # = list of StimRespItem objects
        for (tc_ind, tc) in enumerate(self.pcf.test_conditions()):
            for ij in self.object_pairs():
                # ij = pair of object indices
                obj_pair = (self.pcf.objects[ij[0]], self.pcf.objects[ij[1]])
                res.extend([StimRespItem(obj_pair, s.response(ij, tc_ind), tc)
                            for _ in range(self.n_replications)])
        return res

    def object_pairs(self):
        """generator of all allowed pairs to be presented
        Each pair is a tuple (i, j) with indices into self.pcf.objects
        """
        if self.pair_different:
            return itertools.permutations(range(self.pcf.n_objects), 2)
            # no pairs presented with equal system indices, like (1, 1)
        else:
            return itertools.product(range(self.pcf.n_objects), 2)
            # pairs may include tuples with equal system indices, like (1, 1)

    # ---------------------------- private help method
    # def _check_properties(self):
    #     """Check consistency of given properties
    #     :return: None
    #     """
    #     pass


# ------------------------------------- internal help function:
def thurstone2bradley(x):
    """transform parameters defined on Thurstone d-prime scale,
    to equivalent parameters on the BTL model scale
    :param: x = array or array-like list of values in d-prime units
    :return: array with transformed values
    """
    return logistic.ppf(norm(scale=np.sqrt(2)).cdf(x))


def bradley2thurstone(x):
    """transform parameters defined on Bradle scale,
    to equivalent parameters on the Thurstone model scale
    :param: x = array or array-like list of values in BTL units
    :return: array with transformed values
    """
    return norm.ppf(logistic.cdf(x), scale=np.sqrt(2))
