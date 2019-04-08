"""This module defines classes for Bayesian analysis of paired-comparison data.
This hierarchical version includes a prior representing the distribution of model parameters
in the population from which test subjects were recruited.
It also includes a simple hyper-prior for the population model.

The population model, as well as individual subject models, are adapted to
observed paired-comparison data.

The learned posterior models are used to derive three types of predictive distributions:
*1: a random individual in a Group, for whom paired-comp data are available
*2: a random individual in the Population from which participants were recruited,
    but for whom no data have been collected
*3: mean (=median) across individuals in the Population

All results are estimated
*A: separately for each Group and each Attribute
*B: for a combined Overall Group including all subjects from all groups,
    stored as an additional merged Group with key = tuple of group keys

*** Main Classes:

PairedCompResultSet: analysis results for a complete paired-comparison experiment,
    including PairedCompGroupModel instances for
    one or more groups of test participants (subjects),
    tested for one or more perceptual attributes,
    in all selected test conditions.
    A single PairedCompResultSet instance includes all statistical analysis results.
    All input data for learning a PairedCompResultSet is provided by a
    pc_data.PairedCompDataSet instance.

PairedCompGroupModel: probability distribution of quality parameters for
    all individuals in ONE Group of test subjects for ONE perceptual Attribute,
    AND a prior model for the population from which the test subjects were recruited.

PairedCompIndModel: probability distribution of quality parameters for
    two or more sound-presentation objects, as judged by
    ONE SUBJECT, for ONE perceptual attribute, in ALL selected test conditions.
    Models may be joined later to include data from several subjects,
    thus representing a single mixture distribution for all individuals in a group.

PopulationModel: a GaussianRV prior and posterior model for population parameters.

PopulationPredictiveModel: Parametric predictive model for population parameters.

Bradley:   Bradley-Terry-Luce model: logistic probability distribution for decision variables
Thurstone: Thurstone Case V model: Gaussian probability distribution for decision variables

*** Reference:
Leijon et al (2019) Bayesian Analysis of Paired-comparison Sound Quality Ratings.
    Appendices describe the probabilistic model in detail.

*** Version History:
2017-12-29, first plain-prior functional version
2018-03-27, corrected some doc-strings
2018-03-27, class name change to PairedCompIndModel, to allow other model variants
2018-03-28, PairedCompResultSet.models[g][a] is now a PairedCompGroupModel instance,
            with attribute subjects = dict with (subject_id, PairedCompIndModel) items
            to allow extension to hierarchical population prior
2018-04-02, METHODS PairedCompResultSet.predictive_...
2018-04-05, hierarchical prior model structure
2018-04-12, hierarchical model tested, similar results as older plain-prior variant
2018-05-15, renamed METHODS PairedCompResultSet.predictive_xxx
2018-07-08, changed from Wishart to gauss_gamma.py for population model
2018-08-02, fixed PairedCompMdata likelihood calc for Binary Forced-choice data
2018-08-14, adapted to simplified PairedCompDataSet structure
2018-10-08, method cat_limit_samples in PopulationPredictiveModel
2018-11-27, can learn NULL model with population mean quality params forced to zero, for model comparison
"""

# perhaps integrate out population mean and prec and use Student-t distribution directly,
# with ML type II point estimation of hyperparameters (\beta, a, b) ???
# or perhaps fixed \beta = N, and free (a, b) only ???
# *** but present VI approximation seems already quite OK

# **** save sampler as property to preserve state between VI steps ?

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, ndtr, logit

from collections import OrderedDict, Counter
import logging
import copy

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy

# from PairedCompCalc import gauss_gamma
# from PairedCompCalc import gauss_gamma_null
# absolute import needed only to test this module as __main__

from . import gauss_gamma
from . import gauss_gamma_null

PopulationModel = gauss_gamma.GaussianRV
PopulationNullModel = gauss_gamma_null.GaussianNullRV

# an alternative model might be gauss_wishart.GaussianRV
# with correlated quality parameters

# pc_model_version = 'pc_model with hierarchical population gauss_gamma prior'

N_SAMPLES = 1000  # number of samples for each subject model

MINIMUM_GROUP = 3
# = min number of subjects to avoid warning for population estimates

# ------------------------- prior population distribution parameters:
PRIOR_WEIGHT = 0.2

PRIOR_QUALITY_SCALE = 1.
# = prior scale of quality parameters in Thurstone d-prime units
# = typical prior scale of inter-individual quality distribution
# *** should be modified for equivalent effect with Bradley model ***

PRIOR_CAT_WIDTH_SCALE = 1.
# = prior scale for log response-interval width parameters
#   used to restrict ratio between interval widths
# typical width ratio = cw_big / cw_small = exp(2 * PRIOR_CAT_WIDTH_SCALE)

# 2018-07-11, gives OK empirical coverage of cred.interval for population mean
# initial sampler epsilon = 0.1 seems generally OK, several tests

# ------------------------------------------------------------------------


logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # test


# ------------------------------------------------------------------
class Bradley:
    """Distribution of decision variable in the Bradley-Terry-Luce model.
    """
    unit_label = 'BTL units'
    # for axis label in quality plots

    @staticmethod
    def log_cdf_diff(a, b):
        """log prob( a < Z <= b)
        where Z is a standard logistic random variable
        :param a, b: = arrays with lower and upper interval limits
            a.shape == b.shape
            all( a < b )
        :return: log_p = array with log probabilities, element-wise
            log_p.shape == a.shape == b.shape
        """
        return np.log(expit(b) - expit(a))

    @staticmethod
    def d_log_cdf_diff(a, b):
        """Element-wise partial derivatives of log_cdf_diff(a, b)
        :param a, b: = arrays with lower and upper interval limits
            a.shape == b.shape
            all( a < b )
        :return: tuple (dll_da, dll_db) of arrays, where
            dll_da[...] = d log_cdf_diff(a[...], b[...]) / d a[...]
            dll_db[...] = d log_cdf_diff(a[...], b[...]) / d b[...]
            dll_da.shape == dll_db.shape == a.shape == b.shape
        Arne Leijon, 2017-12-08, tested by finite-diff comparison
        """
        return (1. / np.expm1(a - b) + expit(-a),
                1. / np.expm1(b - a) + expit(-b))

    def __repr__(self):
        return '<class Bradley>'


class Thurstone:
    """Distribution of decision variable in the Thurstone Case V model.
    NOTE: Thurstone.scale is now included in all calculations.
    This is different from corresponding MatLab code.
    """
    unit_label = 'd-prime units'

    sqrt_2pi = np.sqrt(2. * np.pi)
    scale = np.sqrt(2.)

    @staticmethod
    def cdf_diff(a, b):
        """prob( a < Z <= b)
        where Z is a Gaussian standard random variable with variance = 2.
        :param a, b: = arrays with lower and upper interval limits
            a.shape == b.shape
            all( a < b )
        :return: log_p = array with log probabilities, element-wise
            log_p.shape == a.shape == b.shape
        2018-04-24, include Thurstone.scale factor
        """
        a_s = a / Thurstone.scale
        b_s = b / Thurstone.scale
        cdf_diff = ndtr(b_s) - ndtr(a_s)
        ch_sign = a_s >= 0.  # and (b > a) always
        cdf_diff[ch_sign] = ndtr(-a_s[ch_sign]) - ndtr(-b_s[ch_sign])
        # better precision of difference in case of large positive a, b
        return cdf_diff

    @staticmethod
    def log_cdf_diff(a, b):
        """log cdf_diff(a, b)
        :param a, b: = arrays with lower and upper interval limits
            a.shape == b.shape
            all( a < b )
        :return: log_p = array with log probabilities, element-wise
            log_p.shape == a.shape == b.shape
        """
        return np.log(Thurstone.cdf_diff(a, b))

    @staticmethod
    def d_log_cdf_diff(a, b):
        """Element-wise partial derivatives of log_cdf_diff(a, b)
        :param a, b: arrays with lower and upper interval limits
            a.shape == b.shape
            all( a < b )
        :return: tuple (dll_da, dll_db), where
            dll_da[...] = d log_cdf_diff[a[...], b[...]) / d a[...]
            dll_db[...] = d log_cdf_diff[a[...], b[...]) / d b[...]
            dll_da.shape == dll_db.shape == a.shape == b.shape
        Arne Leijon, 2017-12-08, tested by finite-diff comparison
        2018-04-24, include Thurstone.scale factor
        """
        def norm_pdf(x):
            """Gaussian density function = derivative of ndtr(x / scale)
            """
            return np.exp(- (x / Thurstone.scale)**2 / 2) / Thurstone.sqrt_2pi / Thurstone.scale
        # ----------------------------------------------------
        cdf_diff = Thurstone.cdf_diff(a, b)
        return - norm_pdf(a) / cdf_diff, norm_pdf(b) / cdf_diff

    def __repr__(self):
        return '<class Thurstone>'


# ------------------------------------------------------------------
class PairedCompResultSet:
    """Defines probabilistic models for all selected data
    from a paired-comparison experiment.
    """
    def __init__(self, pcf, models, rv_class):
        """Create a PairedCompResultSet from pre-learned attributes.
        :param pcf: single PairedCompFrame instance,
            specifying common aspects of a paired-comparison experiment,
            which are common for all subjects.
        :param models: nested dict with PairedCompGroupModel instances, stored as
            models[group][attribute] = one PairedCompGroupModel instance
            models[group][attribute].subjects = dict with (subject_id, PairedCompIndModel instance)
            where
            group, attribute, subject are string-valued keys,
            for all attribute values in pcf.attributes, for every subject.
        :param rv_class: a class for the distribution of model decision variables, with methods
            rv_class.log_cdf_diff, rv_class.d_log_cdf_diff
            rv_class distribution is Gaussian for rv_class=Thurstone, and
            logistic for rv_class=Bradley
        """
        self.pcf = pcf
        self.models = models  # **** rename to self.groups ???
        self.rv_class = rv_class

    def __repr__(self):
        return f'PairedCompResultSet(pcf=pcf, models=models, rv_class={repr(self.rv_class)})'

    @classmethod
    def learn(cls, ds, rv_class=Thurstone, null_quality=False):
        """Create and learn PairedCompGroupModel instances
        for each group and attribute
        defined by a given PairedCompDataSet instance
        :param ds: a single PairedCompDataSet instance
        :param rv_class: a class for the model latent variable,
            either Thurstone or Bradley
        :param null_quality: (optional) boolean => population model with quality param == 0.
        :return: a single cls instance containing all analysis results

        Arne Leijon,
        2018-03-30, adapted to changed nesting order in ds
        2018-05-19, single population prior for all groups and attributes
        2018-05-19, merge all subject groups into a single group, for each attribute
        2018-11-27, allow learning with NULL population model
        """
        ds.ensure_complete()
        # check that subjects have sufficiently complete data
        pcf = ds.pcf
        pcm = OrderedDict((g, dict()) for g in ds.pcd)
        # model objects will be organized as
        # pcm[group][attribute] ≈ one PairedCompGroupModel instance with
        # pcm[group][attribute].subjects = dict with elements
        # pcm[group][attribute].subjects[subject_ID] = a PairedCompIndModel instance
        population_prior = _make_population_prior(pcf, null_quality)
        # = single hyper-prior used for all groups and all attributes
        for (g, g_attributes) in ds.pcd.items():
            for (a, ga_subjects) in g_attributes.items():
                pcm[g][a] = PairedCompGroupModel.learn(pcf, ga_subjects, rv_class, population_prior)
                logger.debug(f'Learned group {repr(g)}, attribute {a}, for {len(ga_subjects)} subjects')
        if len(pcm) > 1:
            # create separate new group including all groups merged
            # Includes all subject models unchanged, but a new population model
            merged_g = tuple(g for g in pcm.keys())
            ag_models = {a: PairedCompGroupModel.merge([g_models[a]
                                                        for g_models in pcm.values()])
                         for a in pcf.attributes}
            pcm[merged_g] = ag_models
        return cls(pcf, pcm, rv_class)

    def predictive_group_individual(self):
        """Predictive model for each group and attribute,
        for a single RANDOM INDIVIDUAL drawn from the TEST GROUP.

        NOTE: estimated as the mixture distribution for the participant group,
        i.e., NOT including the random effects of subject sampling from the population.

        Each model may include different subjects, thus not directly comparable across attributes.
        Thus, samples may be UNRELATED across attributes within a group.
        Samples are always assumed UNRELATED between groups,
        because groups normally include different subjects.

        :return: res = PredictiveResultSet with
            res.models[group][attribute] = PairedCompIndModel (joined across subjects)

            If the number of samples are equal for all attributes in a group,
            the samples are guaranteed to be RELATED across attributes,
            so correlations among attributes can be calculated.

        2018-10-07, fixed trivial bug that generated only the first group
        """
        models = dict()
        for (g, g_models) in self.models.items():
            # ****** check if subjects are the same across attributes
            common_subjects = set.intersection(*(set(ga.subjects.keys())
                                                 for ga in g_models.values()))
            all_subjects = set.union(*(set(ga.subjects.keys())
                                       for ga in g_models.values()))
            if all_subjects <= common_subjects:
                # we have complete data for all subjects in all attributes
                # ensure subject models are joined in the same order for all attributes
                # so model samples become RELATED across attributes
                common_subjects = list(common_subjects)
                models[g] = {a: PairedCompIndModel.join(*(ga.subjects[s]
                                                          for s in common_subjects))
                             for (a, ga) in g_models.items()}
            else:
                logger.warning(f'Missing data for {all_subjects - common_subjects} ' +
                               f'in group {repr(g)}, for some attribute')
                # simply include all available subjects for each attribute, in arbitrary order,
                # so model samples become UNRELATED across attributes
                models[g] = {a: PairedCompIndModel.join(*ga.subjects.values())
                             for (a, ga) in g_models.items()}
        return PredictiveResultSet(models, self.pcf, self.rv_class)

    def predictive_population_individual(self):
        """Predictive model for EACH GROUP AND ATTRIBUTE,
        for a random INDIVIDUAL in the POPULATION from which the group is recruited.
        :return: res = PredictiveResultSet with
            res[group][attribute] = single PopulationPredictiveModel instance,
                which can generate quality_samples from the predictive model.
        """
        self._check_min_group()
        models = {g: {a: PopulationPredictiveModel(ga_model.population.predictive,
                                                   self.pcf, self.rv_class)
                      # if len(ga_model.subjects) >= MINIMUM_GROUP else None
                      for (a, ga_model)in g_models.items()}
                  for (g, g_models) in self.models.items()}
        return PredictiveResultSet(models, self.pcf, self.rv_class)

    def predictive_population_mean(self):
        """Predictive model for EACH GROUP AND ATTRIBUTE,
        for the MEAN quality params in the POPULATION from which the group is recruited.
        :return: res = PredictiveResultSet with
            res[group][attribute] = single PopulationPredictiveModel instance,
                which can generate quality_samples from distribution of population mean quality.
        """
        self._check_min_group()
        models = {g: {a: PopulationPredictiveModel(ga_model.population.mean.predictive,
                                                   self.pcf, self.rv_class)
                      # if len(ga_model.subjects) >= MINIMUM_GROUP else None
                      for (a, ga_model)in g_models.items()}
                  for (g, g_models) in self.models.items()}
        return PredictiveResultSet(models, self.pcf, self.rv_class)

    def _check_min_group(self):
        msg = 'Unreliable population estimate! Too few subjects in '
        for (g, g_models) in self.models.items():
            for (a, ga_models) in g_models.items():
                if len(ga_models.subjects) < MINIMUM_GROUP:
                    logger.warning(msg + f'group {repr(g)}, attribute {a}')


# ------------------------------------------------------------
class PredictiveResultSet:
    """Set of Predictive distributions derived from analysis results,
    storing predictive models of selected type, suitable for display.
    """
    def __init__(self, models, pcf, rv_class):
        """
        Similar data structure as a PairedCompResultSet
        :param models: nested dict with predictive model instances, stored as
            models[group][attribute] = one predictive model instance
            where
            group, attribute are string-valued keys,
            for all attribute values in pcf.attributes.
            If there was more than one subject group,
            a new merged group may be included, including all subjects from all groups
        :param pcf: reference to a single PairedCompFrame instance used for the analysis
        :param rv_class: reference to decision-variable class used for the analysis
        """
        self.models = models
        self.pcf = pcf
        self.rv_class = rv_class

    def __repr__(self):
        return f'PredictiveResultSet(pcf=pcf, models=models, rv_class={repr(self.rv_class)})'


# ------------------------------------------------------------
class PopulationPredictiveModel:
    """Parametric predictive model for population quality parameters,
    represented by one GROUP of subjects for one ATTRIBUTE,
    OR for all groups pooled, and one attribute.
    Needed to transform raw samples into model quality and cat_limits.
    """
    # ****** might be sub-class of StudentRV ??? **********
    def __init__(self, pred_model, pcf, rv_class):
        """
        :param pred_model: a single StudentRV instance, from which samples can be generated
        :param pcf: a PairedCompFrame instance.
        :param rv_class: class for the decision latent variable, Thurstone or Bradley
        """
        self.pred_model = pred_model
        self.pcf = pcf
        self.rv_class = rv_class

    def __repr__(self):
        return ('PopulationPredictiveModel(' +
                '\n\tpcf=pcf,' +
                f'\n\tpred_model={repr(self.pred_model)},' +
                f'\n\trv_class={repr(self.rv_class)})')

    @property
    def quality_samples(self):
        """Samples of quality parameters from predictive distribution
        of mean vector in a population represented by a group of subjects.
        :return: 3D array q, with quality samples stored as
            q[n, t, s] = n-th sample of quality estimated for
            pcf.test_conditions()[t], pcf.objects[s],
            i.e., same format as PairedCompIndModel.quality_samples
        """

        n_q = _n_quality_params(self.pcf)
        # = number of quality elements in parameter vector
        q = self.pred_model.rvs(size=10 * N_SAMPLES)[:, :n_q]
        q = q.reshape((-1,
                       self.pcf.n_test_conditions,
                       self.pcf.n_objects - 1))
        zero_shape = (*q.shape[:-1], 1)
        # include fixed q == 0. for self.objects[0]
        return np.concatenate((np.zeros(zero_shape), q), axis=-1)

    @property
    def cat_limit_samples(self):
        """extract UPPER response-interval boundaries from self.pred_model
        """
        n_q = _n_quality_params(self.pcf)
        # = number of quality elements in parameter vector
        ln_c = self.pred_model.rvs(size=10 * N_SAMPLES)[:, n_q:]
        return cat_limits_transform(ln_c)


# -------------------------------------------------------------------
class PairedCompGroupModel:
    """A PairedCompGroupModel instance includes PairedCompIndModel instances,
    for ONE group of test subjects,
    and ONE perceptual attribute.

    Arne Leijon, 2018-04-05
    2018-07-09, include pcf= PairedCompFrame reference
    """
    def __init__(self, pcf, subjects, population, population_prior):
        """
        :param pcf: a PairedCompFrame instance.
        :param subjects: dict with (subject_label, PairedCompIndModel) elements
        :param population: a single GaussianRV instance
            representing learned distribution of population quality parameters
        :param population_prior: reference to a single GaussianRV instance
            representing a weakly informative prior for all population models.

        Arne Leijon, 2018-04-05
        2018-07-09, modified signature, include pcf
        """
        self.pcf = pcf
        self.subjects = subjects  # **** OrderedDict to allow matched subjects across Attributes ?
        self.population = population
        self.population_prior = population_prior
        self.LL = []  # list with lower-bound log-likelihood values obtained during VI learning

    def __repr__(self):
        return ('PairedCompGroupModel('+
                '\n\tpcf=pcf,' +
                f'\n\tpopulation={repr(self.population)},' +
                f'\n\tpopulation_prior={repr(self.population_prior)},' +
                f'\n\trv_class={repr(self.rv_class)})')

    @classmethod
    def learn(cls, pcf, ga_subjects, rv_class, population_prior):
        """Learn one PairedCompIndModel for each subject,
        and a single GaussianRV prior for the population represented by the subjects,
        in ONE group of test subjects tested for ONE perceptual attribute.

        :param pcf: a PairedCompFrame object defining experimental layout
        :param ga_subjects: a nested dict with elements (subject_id, s_learn_data)
            where s_learn_data is a dict with elements (tc-tuple, result-list)
        :param rv_class: class for the model latent variable,
            either Thurstone or Bradley
        :param population_prior: externally pre-calculated single prior,
            same for all groups and attribute models

        :return: a PairedCompGroupModel instance

        Arne Leijon, 2018-07-09
        """
        # **** use general baseRV.VILearning class here ???
        m_data = {s: PairedCompMdata(learn_data, pcf)
                  for (s, learn_data) in ga_subjects.items()}
        # = all subject results in format suitable for learning
        ga_model = cls.init_learn(pcf, m_data, rv_class, population_prior)
        ga_model._learn(m_data)
        logger.debug('Learned LL= [' + ', '.join(f'{ll_i:.1f}' for ll_i in ga_model.LL) + ']')
        logger.debug('Population loc = ' + np.array_str(ga_model.population.loc,
                                                        precision=3))
        logger.debug('Population individual var =\n' +
                     np.array_str(ga_model.population.predictive.var,
                                  precision=3, suppress_small=True))
        logger.debug('Population mean var =\n' +
                     np.array_str(ga_model.population.mean.predictive.var,
                                  precision=3, suppress_small=True))
        return ga_model

    @classmethod
    def init_learn(cls, pcf, m_data, rv_class, population_prior):
        """
        Create initial version of the cls instance,
        to be adapted to data later, by VI learning

        :param pcf: a PairedCompFrame object defining experimental layout
        :param m_data: observed data for one group of subjects and one attribute
        :param rv_class: class for the model latent variable, Thurstone or Bradley
        :param population_prior: externally pre-calculated single prior,
            same for all groups and attribute models

        :return: a cls instance, initialized to correct internal structure,
            with non-informative parameters, not yet learned

        Arne Leijon, 2018-07-09, slightly modified for gauss_gamma population model
        """

        nq = _n_quality_params(pcf)
        # = n quality params
        nr = pcf.n_difference_grades
        nx = nq + nr
        # = length of parameter vector
        population = copy.deepcopy(population_prior)

        # set smaller mean precision for the first subject learning step
        # to make the population mean get nearly correct from start
        # population.prec.scale[:nq, :nq] /= 100.  # gauss_wishart version
        population.prec.b[:nq] *= 100.  # gauss_gamma version
        subjects = {s: PairedCompIndModel(pcf,
                                          x_samples=np.zeros((1, nx)),
                                          x_map=np.zeros((1, nx)),
                                          rv_class=rv_class)
                    for s in m_data}
        return cls(pcf, subjects, population, population_prior)

    def _learn(self, m_data,
               min_iter=5, min_step=0.01,
               max_iter=np.inf, callback=None):
        """Learn self from observed data,
        using Variational Inference (VI).
        *** mainly copied from baseRV.VILearning.learn

        This method adapts all model parameters towards a local maximum of
        a lower bound to the total likelihood of the training data.

        :param m_data: observed data for one group of subjects and one attribute
        :param min_iter= (optional) minimum number of learning iterations
        :param min_step= (optional) minimum data log-likelihood improvement,
                 over the latest min_iter iterations,
                 for learning iterations to continue.
        :param max_iter= (optional) maximum number of iterations, regardless of result.
        :param callback= (optional) function to be called after each iteration step.
            If defined, called as callback(self, previousLowBound)
            where previousLowBound == VI lower bound BEFORE last update
        :return: LL = list of log-likelihood values, one after each iteration.
            The resulting sequence is theoretically guaranteed to be non-decreasing.

        Result: adapted self properties.

        Arne Leijon, 2016-09-01
        2018-04-05, copied from baseRV, modified for use here
        """
        min_iter = np.max([min_iter, 1])
        log_probs = []
        while (len(log_probs) <= min_iter
               or (log_probs[-1] - log_probs[-1-min_iter] > min_step
                   and (len(log_probs) < max_iter))):
            log_probs.append(self.one_learn_step(m_data))
            if callback is not None:
                callback(self, log_probs[-1])
            logger.debug('learned LL = ' + np.array_str(np.asarray(log_probs),
                                                        precision=2))
        self.LL = log_probs
        return log_probs

    def one_learn_step(self, m_data):
        """
        One VI learning step.
        :param m_data: observed data for one group of subjects and one attribute
        :return: scalar LL = current VI lower bound of log-likelihood

        Arne Leijon, 2018-07-09, eliminate arbitrary common constant in log(cat_width)
        """
        LL_sum_ind = sum(s_model.adapt(m_data[s], self.population)
                         for (s, s_model) in self.subjects.items())
        x_samples = np.array([s_model.x_samples
                              for (s, s_model) in self.subjects.items()])
        sum_ind_entropy = sum(entropy(x) for x in x_samples)
        # = sum_n E{ - ln q_n(x_samples[n]) }, with E{} = mean across samples

        # ensure sum( log(cat_width) ) == 0, because gauss_gamma uses diagonal covariance
        n_q = _n_quality_params(self.pcf)
        x_samples[..., n_q:] -= np.mean(x_samples[..., n_q:],
                                       axis=-1, keepdims=True)
        self.population.adapt(x_samples, self.population_prior)
        pop_KLdiv = self.population.relative_entropy(self.population_prior)

        # -------------------------------------------- only for logger output:
        mean_x_map = np.mean([s_model.x_map
                              for s_model in self.subjects.values()], axis=(0,1))
        logger.debug(f'mean(x_map) = {mean_x_map}')
        logger.debug(f'group.population.loc = {self.population.loc}')
        logger.debug(f'group.population.prec.mean_inv = {self.population.prec.mean_inv}')
        logger.debug(f'LL_sum_ind={LL_sum_ind}; sum_entropy={sum_ind_entropy}; -KLdiv={- pop_KLdiv}')
        # ---------------------------------------------------

        return LL_sum_ind + sum_ind_entropy - pop_KLdiv

    @classmethod
    def merge(cls, models):
        """Merge a sequence of group models into a single such model.
        :param models: iterable of PairedCompGroup instances
        :return: single PairedCompGroup instance

        Arne Leijon, 2018-05-19
        2018-07-09, remove arbitrary constant in log(cat_width) params, for gauss_gamma population
        """
        def join(subject_dicts):
            """Gather several subject dicts into a single dict
            :param subject_dicts: sequence of dicts, each with (s_id, PairedCompIndModel) elements
            :return: all_subjects = single dict with (s_id, PairedCompIndModel) elements,
                union of all s_dicts
            """
            all_subjects = dict()
            # space for result, stored as all_subjects[subject_id] = subject PairedCompIndModel instance
            for s_dict in subject_dicts:
                for (s, s_model) in s_dict.items():
                    if s in all_subjects:
                        all_subjects[s].add(s_model)
                    else:
                        all_subjects[s] = s_model
            return all_subjects
        # ----------------------------------------------------

        population_prior = models[0].population_prior  # copy reference
        pcf = models[0].pcf  # copy reference
        population = copy.deepcopy(population_prior)  # new population model
        subjects = join(m.subjects for m in models)
        x_samples = np.array([s_model.x_samples for s_model in subjects.values()])

        n_q = _n_quality_params(pcf)
        # remove any arbitrary constant from log(cat_width) params:
        x_samples[..., n_q:] -= np.mean(x_samples[..., n_q:], axis=-1, keepdims=True)
        population.adapt(x_samples, population_prior)
        return cls(pcf, subjects, population, population_prior)


# -------------------------------------------------------------------
class PairedCompIndModel:
    """A PairedCompIndModel instance represents a probabilistic model of
    psycho-acoustic paired-comparison evaluations
    of ONE perceptual attribute for
    a set of N different sound transmission objects.

    Each instance represents the posterior distribution of parameters
    in a Thurstone Case V model OR a Bradley-Terry-Luce model,
    adapted to the paired-comparison responses from ONE listener.
    """
    def __init__(self, pcf, x_samples, x_map, rv_class):
        """
        :param pcf: reference to a PairedCompFrame instance,
            common for all model instances.
        :param x_samples: 2D array of equally probable sample vectors with parameters
        :param x_map: 2D array with a single row with max-a-posteriori probable parameter vector
            parameter vectors include both quality and response-interval width parameters.
        :param rv_class: probability-distribution class for the model latent variable, with METHODS
            rv_class.log_cdf_diff, d_log_cdf_diff
            rv_class is Gaussian for the Thurstone Case V model type, and
            logistic for the Bradley-Terry-Luce model type

        NOTE: quality parameters are self.x_samples[:, :self.n_q]
        response-category intervals are defined by a transform function, as
        (b_low, b_high) = cat_limits(self.x_samples[:, self.n_q:] )
        """
        self.pcf = pcf
        self.x_samples = x_samples
        self.x_map = x_map
        self.rv_class = rv_class

    def __repr__(self):
        return ('PairedCompIndModel('+
                '\n\tpcc=pcf,' +
                '\n\tx_samples=x_samples,' +
                '\n\tx_map=x_map,' +
                f'\n\trv_class={repr(self.rv_class)})')

    @property
    def n_q(self):
        """number of quality parameters in self.x_samples and self.x_map
        """
        return _n_quality_params(self.pcf)

    @property
    def quality_samples(self):
        """extract quality parameters from self.x_samples
        Returns: 3D array q, with quality samples stored as
            q[n, t, s] = n-th sample of quality estimated for
            pcf.test_conditions()[t], pcf.objects[s]
        """
        q = self.x_samples[:, :self.n_q].reshape((-1,
                                                  self.pcf.n_test_conditions,
                                                  self.pcf.n_objects - 1))
        zero_shape = (*q.shape[:-1], 1)
        # include fixed q == 0. for self.objects[0]
        return np.concatenate((np.zeros(zero_shape), q), axis=-1)

    @property
    def quality_map(self):
        """extract MAP estimate(s) of quality parameters
        :return: 3D array q, with quality samples stored as
            q[n, t, s] = map quality estimated for n-th subject in
            pcf.test_conditions()[t], pcf.objects[s]
        """
        q = self.x_map[..., :self.n_q].reshape((-1,
                                                self.pcf.n_test_conditions,
                                                self.pcf.n_objects - 1))
        zero_shape = (*q.shape[:-1], 1)
        return np.concatenate((np.zeros(zero_shape), q), axis=-1)

    @property
    def cat_limit_samples(self):
        """extract UPPER response-interval boundaries from self.x_samples
        """
        return cat_limits_transform(self.x_samples[:, self.n_q:])

    def adapt(self, md, prior):
        """
        Adapt self to given paired-comparison data, also considering the prior,
        representing the current estimate of the distribution in the population.
        :param md: a PairedCompMdata instance, with paired-comparison data for
            one subject, one attribute, in all test conditions.
        :param prior: a single GaussianRV instance, same for all subjects.
        :return: scalar LL = current log-likelihood of observed data
            = E_q{ ln p(md | self.x_samples) p(x_samples | prior) },
            where q() is the current distribution of model parameters,
            represented by self.x_samples with equally probable sample vectors,
            so E{ f(X) } is calculated as mean( f(x_samples) )

        Arne Leijon, 2018-04-20, no re-scaling of parameter data,
            for correct prior adaptation and correct LL calculation
        """
        # --------------------------------------------
        def neg_ll(x):
            return - prior.mean_logpdf(x) - md.log_likelihood(x, self.rv_class)

        def grad_neg_ll(x):
            return - prior.grad_mean_logpdf(x) - md.grad_log_likelihood(x, self.rv_class)
        # --------------------------------------------
        # find MAP point first:
        # n_s = self.pcf.n_objects
        # n_tct = self.pcf.n_test_conditions
        n_cw = self.pcf.n_difference_grades
        n_q = self.n_q
        n_param = n_q + n_cw
        # ------------------------------------------------- TEST grad_neg_ll
        # from scipy.optimize import approx_fprime, check_grad
        # x0 = np.zeros(n_param)
        # print(f'neg_ll({x0}) = {neg_ll(x0)}')
        # x0_plus = x0 + [0., 0., 1.,1.,1.]
        # print(f'neg_ll({x0_plus}) = {neg_ll(x0_plus)}')
        # print('approx prior.grad_mean_logpdf = ', approx_fprime(x0, prior.mean_logpdf, epsilon=1e-6))
        # print('exact  prior.grad_mean_logpdf = ', prior.grad_mean_logpdf(x0))
        #
        # def fun(x):
        #     return md.log_likelihood(x, self.rv_class)
        #
        # def jac(x):
        #     return md.grad_log_likelihood(x, self.rv_class)
        #
        # print('approx md.grad_log_likelihood = ', approx_fprime(x0, fun, epsilon=1e-6))
        # print('exact  md.grad_log_likelihood = ', jac(x0))
        # print('approx grad_neg_ll = ', approx_fprime(x0, neg_ll, epsilon=1e-6))
        # print('exact  grad_neg_ll = ', grad_neg_ll(x0))
        # err = check_grad(neg_ll, grad_neg_ll, x0, epsilon=1e-6)
        # print('check_grad err = ', err)
        # -------------------------------------------- OK 2018-07-09
        res = minimize(fun=neg_ll,
                       jac=grad_neg_ll,
                       x0=np.zeros(n_param))
        # **** use Hessian to set sampler.epsilon ???
        if res.success:
            x_map = res.x.reshape((1, -1))
        else:
            print('minimize res:', res)
            raise RuntimeError('MAP search did not converge')

        if len(self.x_samples) != N_SAMPLES:
            # run sampler starting from x_map
            x0 = x_map
        else:
            # we have sampled before, start from those samples
            x0 = self.x_samples + x_map - self.x_map
        # ********* OR keep sampler as self attribute ???
        sampler = ham.HamiltonianSampler(x=x0,
                                         fun=neg_ll,
                                         jac=grad_neg_ll,
                                         epsilon=0.1
                                         )
        sampler.safe_sample(n_samples=N_SAMPLES, min_steps=2)
        logger.debug(f'sampler accept_rate = {sampler.accept_rate:.1%}, ' +
                     f'n_steps = {sampler.n_steps:.0f}, ' +
                     f'epsilon = {sampler.epsilon:.2f}')
        self.x_samples = sampler.x
        self.x_map = x_map
        return - np.mean(sampler.U)

    def add(self, other):
        """Merge data in self with other
        Input:
        other = another PairedCompIndModel instance
        Result: self.x_samples and x_map extended
        """
        assert (self.pcf is other.pcf and self.rv_class is other.rv_class), 'incompatible models'
        self.x_samples = np.concatenate((self.x_samples, other.x_samples))
        self.x_map = np.concatenate((self.x_map, other.x_map))

    @classmethod
    def join(cls, *models):
        """Join a sequence of PairedCompIndModel instances into a single such model
        Input:
        models = iterable of model objects, all with same structure
            no input models are modified
        Returns: result = new single PairedCompIndModel instance
        Arne Leijon, 2018-04-02, changed from module function, for clarity
        """
        # ******** concatenate all in one operation ? *********************
        it_models = iter(models)
        first = next(it_models)
        result = cls(first.pcf, first.x_samples.copy(), first.x_map.copy(), first.rv_class)
        for m in it_models:
            result.add(m)
        return result


# --------------------------------------------------- general module helper stuff

def _n_quality_params(pcf):
    """Number of quality parameters to be learned for each Group and each Attribute.

    :param pcf: single PairedCompFrame object defining experimental layout
    :return: scalar integer
    """
    return (pcf.n_objects - 1) * pcf.n_test_conditions


def _make_population_prior(pcf, null_quality=False):
    """Create a single prior model to be used in all learned models,
    using global scale constants.

    :param pcf: single PairedCompFrame object defining experimental layout
    :param null_quality: (optional) boolean => model with all quality params == 0.
    :return: single PopulationModel instance (or PopulationNullModel)

    Arne Leijon, 2018-07-08, modified for gauss-gamma population model
    2018-11-27, can also generate NULL model for population-model comparison
    """
    nq = _n_quality_params(pcf)
    # = n quality params
    nr = pcf.n_difference_grades
    nx = nq + nr
    # = length of parameter vector
    x_scale = np.concatenate((np.ones(nq) * PRIOR_QUALITY_SCALE,  # rv_class
                              np.ones(nr) * PRIOR_CAT_WIDTH_SCALE))
    # return gauss_gamma.GaussianRV(loc=np.zeros(nx), scale=x_scale, learned_weight=PRIOR_WEIGHT)
    if null_quality:
        return PopulationNullModel(n_null=nq,
                                   loc=np.zeros(nx), scale=x_scale, learned_weight=PRIOR_WEIGHT)
    else:
        return PopulationModel(loc=np.zeros(nx), scale=x_scale, learned_weight=PRIOR_WEIGHT)


def cat_limits_transform(log_w):
    """Transform given log-category-width parameters to response-category interval limits.
    (NOT the same transform as in MatLab PairedComparison analysis)
    :param log_w: 1D or 2D array with
        log_w[..., m] = ...-th sample of log non-normalized width of m-th interval.
        (called \eta_{nm} in JASA paper)
        (OR log_w[m] = m-th element of single vector)
        log_w.shape[-1] == M == number of intervals.

    :return: 1D or 2D array b, with all elements in (0, +inf]
        b[..., m] = UPPER limit for m-th interval,
            = LOWER limit for the (m+1)-th interval,
        b.shape == log_w.shape

    NOTE: lower limit for the first interval is NOT included
        lower limit for first interval == 0. if forced_choice,
        lower limit for first interval == - upper limit, if not forced_choice
        upper limit for highest interval always == + inf

    Method:
        Normalized widths and interval limits are defined in transformed domain (0, 1.),
        using a symmetric logistic mapping function,
        y = 2 * expit(b) - 1, where b \in (0, inf]; y \in (0, 1]
            y_{:, m} =  (w_0 +...+ w_m) / (w_0 + ... + w_{M-1};  0 <= m <= M-1
            w_m = exp(log_w[..., m])
        Thus, cat_limits b are calculated with the inverse transform
        b = logit( (1+y)/2 )
        which gives b[..., M-1] == + inf, where y == 1.
    """
    # w = np.exp(CAT_WIDTH_SCALE * log_w)
    # w = np.exp(log_w)
    # = non-normalized width of transformed intervals, always > 0
    cum_w = np.cumsum(np.exp(log_w), axis=-1)
    # sum_w = cum_w[..., -1:]
    # ************************* check timing for errstate *****************
    #alt 1:
    #  with np.errstate(divide='ignore'):  # allow b[..., -1] = inf without warning
    #     b = np.log((sum_w + cum_w) / (sum_w - cum_w))

    # alt 2:
    # b = np.log((sum_w + cum_w) / (sum_w - cum_w))

    # alt 4: **** simplest and probably fastest
    b = logit((1. + cum_w / cum_w[..., -1:]) / 2)
    return b


def d_cat_limits_transform(log_w):
    """gradient of cat_limits with respect to log_w
    :param log_w: 1D or 2D array with
        log_w[..., m] = log non-normalized width of m-th interval,
        log_w.shape[-1] = M = number of response intervals

    :return: 2D or 3D array db_dlogw, with
    db_dlogw[..., m, i] = db[..., m] / d log_w[..., i]; m = 0,..., M-2; i = 0, ..., M-1
        where b[..., m] = UPPER limit of m-th response interval
    db_dlogw.shape[-2:] == (M-1, M)

    Arne Leijon, 2017-12-07, checked with scipy check_grad
    2018-08-04, simplified code, checked
    """
    # w = np.exp(CAT_WIDTH_SCALE * log_w)
    w = np.exp(log_w)
    len_w = w.shape[-1]
    cum_w = np.cumsum(w, axis=-1)
    cw = cum_w[..., :-1, np.newaxis]
    sw = cum_w[..., -1:, np.newaxis]
    # b = logit((1+y)/2) = log(sw+cw) - log(sw-cw) = b1 - b2, where
    # cw[..., m] (w_0 +...+ w_m); m = 0, ..., len_2-2
    # sw[...] = (w_0 +...+ w_{len_w-1})
    # dcw_dw[..., m, i] = dcw[..., m] /dw[..., i]  = [1. if i <= m else 0.
    # dsw[...] / dw[..., i] = 1, all i
    dcw_dw = np.tril(np.ones((len_w-1, len_w)))
    db_dw = (1. + dcw_dw) / (sw + cw) - (1. - dcw_dw) / (sw - cw)
    return db_dw * w[..., np.newaxis,:]  # = db_dlogw


class PairedCompMdata:
    """Help class for PairedCompIndModel learning.
    The PairedCompMdata object is used only temporarily during the learning procedure,
    to provide a representation of all paired-comparison results for ONE subject, stored in
    a PairedCompDataSet instance ds, as ds.pcd[group][attribute][subject]
    The results are re-organized more compactly to facilitate learning calculations.
    """
    def __init__(self, s_res, pcf):
        """Recode paired-comparison results to facilitate learning.
        :param s_res: a list of StimRespItem objects, obtained from
            some ds.pcd[group][attribute][subject]
        :param pcf: a PairedCompFrame instance; determines how to store s_res data

        2018-08-14, simplified s_res, because of simplified PairedCompDataSet structure
        """
        counter = Counter()
        n_objects = len(pcf.objects)
        tct = list(pcf.test_conditions())
        for ((a, b), r, tc) in s_res:
            i_tc = tct.index(tc)
            tc_offset = i_tc * (n_objects - 1)
            if r < 0:  #
                # swap so response is positive, quality(b >= quality(a)
                (a, b) = (b, a)
                r = - r
            # recode ia, ib as indices into PairedCompIndModel parameter vector x, such that
            # mu_a = x[:, self.ia] if ia >= 0 else Mu_a = 0.
            # similar for mu_b
            ia = pcf.objects.index(a)
            ia = -1 if ia == 0 else tc_offset + ia - 1
            ib = pcf.objects.index(b)
            ib = -1 if ib == 0 else tc_offset + ib - 1
            counter[(ia, ib, r)] += 1

        self.n_q = _n_quality_params(pcf)
        self.n_cat = pcf.n_difference_grades
        # remaining elements in parameter vectors define response-category interval widths
        self.forced_choice = pcf.forced_choice
        # must be saved to determine lowest response category limits
        # copy counter results into self:
        self.a_index = []
        self.b_index = []
        self.cat_index = []
        self.count = []
        for ((ia, ib, r), n) in counter.items():
            self.a_index.append(ia)
            self.b_index.append(ib)
            # quality means found in q_a = x[:, self.ia] if ia >= 0 else q_a = 0.
            # similarly for q_b
            if pcf.forced_choice:
                r -= 1
                # recode category indices for origin zero,
                # because r == 0 never occurs if forced_choice
            self.cat_index.append(r)
            # interval width parameters for pcf.response_label[m]
            # stored in x[:, self.n_q + m]
            self.count.append(n)
        self.a_index = np.array(self.a_index)
        self.b_index = np.array(self.b_index)
        self.cat_index = np.array(self.cat_index)
        self.count = np.array(self.count)

    def q_diff(self, x):
        """extract quality-parameter differences from given model samples
        Input:
        x = 1D or 2D array with model parameter ROW vector(s)
            x[n, i] = n-th sample of i-th internal model parameter
        Returns:
        1D or 2D array d with elements
            d[..., p] = b - a for p-th paired-comparison (a, b) stored in self
        d.shape[-1] == number of paired-comparison trials
        """
        a = x[..., self.a_index]
        b = x[..., self.b_index]
        a[..., self.a_index == -1] = 0.
        b[..., self.b_index == -1] = 0.
        return b - a

    def cat_limits(self, x):
        """extract low and high interval limits for each response case in self.
        :param x: 2D array with tentative model parameter sample ROW vectors
            x[n, i] = n-th sample of i-th internal model parameter
        :return: tuple (b_low, b_high), where b_low and b_high are 2D arrays,
            b_low[n, p] = n-th sample of lower interval bound at p-th response case
            b_high[n,p] = similarly, higher interval bound.

        2018-08-03, simplified, with cat_limits_transform giving highest +inf limit
        """
        b = cat_limits_transform(x[..., self.n_q:])
        # = UPPER interval limits
        l_index = np.maximum(0, self.cat_index - 1)
        b_low = b[..., l_index]
        if self.forced_choice:
            b_low[..., self.cat_index == 0] = 0.
        else:
            b_low[..., self.cat_index == 0] *= -1.
        # h_index = np.minimum(b.shape[-1] - 1, self.cat_index)
        b_high = b[..., self.cat_index]
        # b_high[..., b.shape[-1] == self.cat_index] = np.inf
        return b_low, b_high

    def cdf_args(self, x):
        """extract arguments for model probability calculation
        :param x: 1D or 2D array with model parameter sample ROW vectors
            x[..., i] = ...-th sample of i-th internal model parameter
        :return: tuple( (arg_low, arg_high) arguments for probabilistic model, such that
            P[ p-th paired-comparison response | n-th model-parameter sample ] =
            = rv_class.cdf(arg_high[n, p) - rv_class.cdf(arg_low[n, p])
        """
        d = self.q_diff(x)
        (b_low, b_high) = self.cat_limits(x)
        return b_low - d, b_high - d

    def log_likelihood(self, x, rv):
        """log P{self | x} given model parameters x
        :param x: 1D or 2D array with model parameter sample ROW vectors
            x[n, i] = n-th sample of i-th internal model parameter, OR
            x[i] = i-th model parameter of a single parameter vector
            x[..., :self.n_q] are quality parameters,
            x[..., self.n_q:] are transformed response-interval width parameters
        :param rv: Latent-variable class, Thurstone or Bradley
        :return: 1D array (or scalar) ll, with one element for each row vector in x
            ll[n] = - log prob(md | x[n,:] ) if x is 2D, OR
            ll = - log prob(md | x ) if x is a single 1D parameter vector
            ll.shape == x.shape[:-1]

        Method:
        For the k-th paired-comparison response_magnitude = m[k], with choice b > a,
        the probability is
        P[ response[k] | mu_a[k], mu_b[k] ] =
        = rv.cdf(b_high - mu_diff) ) - rv.cdf(b_low - mu_diff), where
            (b_low, b_high) = (lower, upper) limits of m-th latent-variable interval
            The cdf arguments are calculated by self.cdf_args, given parameter vectors x, and
            self.count is an array of number of trials with the same pair and response.
        """
        ll = rv.log_cdf_diff(*self.cdf_args(x))
        # ll[n, k] = log ll for k-th trial category, given n-th x-sample
        # ll.shape == (n_samples, n trial categories)
        return np.dot(ll, self.count)

    def grad_log_likelihood(self, x, rv):
        """gradient of log P[self | x]
        :param x: 1D or 2D array with model parameter sample ROW vectors
            x[n, i] = n-th sample of i-th internal model parameter, OR
            x[i] = i-th model parameter of a single parameter vector
            x[..., :self.n_q] are quality parameters,
            x[..., self.n_q:] are transformed response-interval width parameters
        :param rv: Latent-variable class, Thurstone or Bradley
        :return: array dll_dx, with
            dll_dx[..., i] = d ll[...] / d x[..., i]
            dll_dx.shape == x.shape
        """
        dll_dx = np.zeros_like(x)
        # = space for result
        dll_db = np.zeros_like(x[..., self.n_q:-1])
        # = space for derivative w.r.t. intermediate interval limits, except lowest and highest
        (d_ll_low, d_ll_high) = rv.d_log_cdf_diff(*self.cdf_args(x))
        # d_ll_low[n, k] = d ll[n, k] / d cdf_args[0][n, k]; n-th sample k-th pair
        # d_ll_high[n, k] = d ll[n, k] / d cdf_args[1][n, k]; n-th sample k-th pair
        d_ll_low *= self.count
        d_ll_high *= self.count

        # cdf_args = (b_low - (q_b - q_a), b_high - (q_b - q_a))
        # thus, q_b and q_a have equal effects in d_ll_low and d_ll_high

        # gradient w.r.t q parameters in x:
        d_ll = d_ll_low + d_ll_high
        for i in range(self.n_q):
            # i = index of q_a and q_b in x
            dll_dx[..., i] = (np.sum(d_ll[..., i == self.a_index], axis=-1) -
                              np.sum(d_ll[..., i == self.b_index], axis=-1))

        # gradient w.r.t b_low and b_high parameters:
        db_dx = d_cat_limits_transform(x[..., self.n_q:])
        # db_dx[..., m, i] = grad of UPPER limit of m-th interval w.r.t x[:, self.n_q+i]
        # db_dx.shape[-1] == self.n_cat
        # db_dx.shape[-2] == self.n_cat-1

        for m in range(self.n_cat-1):
            # m = index of interval boundary,  i.e., upper limit of m-th category interval
            dll_db[..., m] = (np.sum(d_ll_high[..., m == self.cat_index], axis=-1) +
                              np.sum(d_ll_low[..., (m + 1) == self.cat_index], axis=-1))
        if not self.forced_choice:
            # special case for low limit of zero interval
            dll_db[..., 0] -= np.sum(d_ll_low[..., 0 == self.cat_index], axis=-1)  # *******, keepdims=True)
        # dll_dx[..., self.n_q:] = dll_db @ db_dx
        # dll_dx[..., self.n_q:] = np.einsum('...m, ...mi -> ...i',
        #                                    dll_db, db_dx)
        dll_dx[..., self.n_q:] = np.sum(dll_db[..., :, None] * db_dx, axis=-2)
        return dll_dx


# --------------------------------------------------------------- TEST:
if __name__ == '__main__':

    # --------------------------------------------
    print('*** test d_cat_limit_transform')
    from scipy.optimize import approx_fprime, check_grad

    # --------------------------------------------------

    # log_file = 'test_pc_model.log'
#     # = name of log file
#     result_path = Path('.')
#     # result_path.mkdir(parents=True, exist_ok=True)
#     pc_logging.setup(result_path, log_file)
#     # ----------------------------------------------------
#
    x0 = np.zeros(3)
    # x0 = np.array([1.,2., -3.])
    # x0 = np.array([-0.1, -0.25, +0.28])
    def fun(x):
        return cat_limits_transform(x)[1]
    def jac(x):
        return d_cat_limits_transform(x)[1]

    eps = 1.e-6
    print(f'cat_limits_transform{x0} = {cat_limits_transform(x0)}')
    print(f'cat_limits_transform(x0+eps) = {cat_limits_transform(x0+eps)} Should remain the same')

    print('approx gradient = ', approx_fprime(x0, fun, epsilon=1e-6))
    print('exact  gradient = ', jac(x0))
    err = check_grad(fun, jac, x0, epsilon=1e-6)
    print('check_grad err = ', err)

    # ------------------------------------- OK
    a = np.array([2.])
    b = np.array([np.inf])
    b = np.array([3.])

    print('Thurstone log_cdf_diff = ', Thurstone.log_cdf_diff(a, b))
    (da, db) = Thurstone.d_log_cdf_diff(a,b)
    print('dll_da =', da)
    print('dll_db =', db)
    eps = 1e-6
    print('approx dll_da: ', (Thurstone.log_cdf_diff(a+eps/2, b) -
                              Thurstone.log_cdf_diff(a-eps/2, b)) / eps)
    print('approx dll_db: ', (Thurstone.log_cdf_diff(a, b+eps/2) -
                              Thurstone.log_cdf_diff(a, b-eps/2)) / eps)
    # -------------------------------------- OK
