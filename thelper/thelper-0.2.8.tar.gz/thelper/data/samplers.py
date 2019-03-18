"""Samplers module.

This module contains classes used for raw dataset rebalancing or augmentation.

All samplers here should aim to be compatible with PyTorch's sampling interface
(torch.utils.data.sampler.Sampler) so that they can be instantiated at runtime
through a configuration file and used as the input of a data loader.
"""
import copy
import logging

import torch
import torch.utils.data.sampler

import thelper.data.utils

logger = logging.getLogger(__name__)


class WeightedSubsetRandomSampler(torch.utils.data.sampler.Sampler):
    r"""Provides a rebalanced list of sample indices to use in a data loader.

    Given a list of sample indices and the corresponding list of class labels, this sampler
    will produce a new list of indices that rebalances the distribution of samples according
    to a specified strategy. It can also optionally scale the dataset's total sample count to
    avoid undersampling large classes as smaller ones get bigger.

    The currently implemented strategies are:

      * ``random``: will return a list of randomly picked samples based on the multinomial \
        distribution of the initial class weights. This sampling is done with replacement, \
        meaning that each index is picked independently of the already-picked ones.

      * ``uniform``: will rebalance the dataset by normalizing the sample count of all classes, \
        oversampling and undersampling as required to distribute all samples equally. All \
        removed or duplicated samples are selected randomly without replacement.

      * ``root``: will rebalance the dataset by normalizing class weight using an n-th degree \
        root. More specifically, for a list of initial class weights :math:`W^0=\{w_1^0, w_2^0, ... w_n^0\}`, \
        we compute the adjusted weight :math:`w_i` of each class via:

        .. math::
          w_i = \frac{\sqrt[\leftroot{-1}\uproot{3}n]{w_i^0}}{\sum_j\sqrt[\leftroot{-1}\uproot{3}n]{w_j^0}}

        Then, according to the new distribution of weights, all classes are oversampled and
        undersampled as required to reobtain the dataset's total sample count (which may be
        scaled). All removed or duplicated samples are selected randomly without replacement.

        Note that with the ``root`` strategy, if a very large root degree ``n`` is used, this
        strategy is equivalent to ``uniform``. The ``root`` strategy essentially provides a
        solution for extremely unbalanced datasets where uniform oversampling and undersampling
        would be too aggressive.

    By default, this interface will try to keep the dataset size constant and balance oversampling
    with undersampling. If undersampling is undesired, the user can increase the total dataset
    size via a scale factor. Finally, note that the rebalanced list of indices is generated by
    this interface every time the ``__iter__`` function is called, meaning two consecutive lists
    might not contain the exact same indices.

    Example configuration file::

        # ...
        # the sampler is defined inside the 'loaders' field
        "loaders": {
            # ...
            # this field is completely optional, and can be omitted entirely
            "sampler": {
                # the type of the sampler we want to instantiate
                "type": "thelper.data.samplers.WeightedSubsetRandomSampler",
                # the parameters passed to the sampler's constructor
                "params": {
                    "stype": "root3",
                    "scale": 1.2
                },
                # specifies whether the sampler should receive class labels
                "pass_labels": true
            },
            # ...
        },
        # ...

    Attributes:
        nb_samples: total number of samples to rebalance (i.e. scaled size of original dataset).
        label_groups: map that splits all samples indices into groups based on labels.
        stype: name of the rebalancing strategy to use.
        indices: copy of the original list of sample indices provided in the constructor.
        sample_weights: list of weights used for random sampling.
        label_counts: number of samples in each class for the ``uniform`` and ``root`` strategies.
        seeds: dictionary of seeds to use when initializing RNG state.
        epoch: epoch number used to reinitialize the RNG to an epoch-specific state.

    .. seealso::
        | :func:`thelper.data.utils.create_loaders`
        | :func:`thelper.data.utils.get_class_weights`
    """

    def __init__(self, indices, labels, stype="uniform", scale=1.0, seeds=None, epoch=0):
        """Receives sample indices, labels, rebalancing strategy, and dataset scaling factor.

        This function will validate all input arguments, parse and categorize samples according to
        labels, initialize rebalancing parameters, and determine sample counts for each valid class.
        Note that an empty list of indices is an acceptable input; the resulting object will also
        create and empty list of samples when ``__iter__`` is called.

        Args:
            indices: list of integers representing the indices of samples of interest in the dataset.
            labels: list of labels tied to the list of indices (must be the same length).
            stype: rebalancing strategy given as a string. Should be either "random", "uniform", or
                "rootX", where the 'X' is the degree to use in the root computation (float).
            scale: scaling factor used to increase/decrease the final number of sample indices to
                generate while rebalancing.
            seeds: dictionary of seeds to use when initializing RNG state.
            epoch: epoch number used to reinitialize the RNG to an epoch-specific state.
        """
        super().__init__(None)
        if not isinstance(indices, list) or not isinstance(labels, list):
            raise AssertionError("expected indices and labels to be provided as lists")
        if len(indices) != len(labels):
            raise AssertionError("mismatched indices/labels list sizes")
        if not isinstance(scale, float) or scale < 0:
            raise AssertionError("invalid scale parameter; should be greater than zero")
        self.seeds = {}
        if seeds is not None:
            if not isinstance(seeds, dict):
                raise AssertionError("unexpected seed pack type")
            self.seeds = seeds
        if not isinstance(epoch, int) or epoch < 0:
            raise AssertionError("invalid epoch value")
        self.epoch = epoch
        self.nb_samples = int(round(len(indices) * scale))
        if self.nb_samples > 0:
            self.stype = stype
            self.indices = copy.deepcopy(indices)
            self.label_groups = {}
            for idx, label in enumerate(labels):
                if label in self.label_groups:
                    self.label_groups[label].append(indices[idx])
                else:
                    self.label_groups[label] = [indices[idx]]
            if not isinstance(stype, str) or (stype not in ["uniform", "random"] and "root" not in stype):
                raise AssertionError("unexpected sampling type")
            if stype == "random":
                self.sample_weights = [1.0 / len(self.label_groups[label]) for label in labels]
            else:
                weights = thelper.data.utils.get_class_weights(self.label_groups, stype, invmax=False)
                self.label_counts = {}
                curr_nb_samples, max_sample_label = 0, None
                for label_idx, (label, indices) in enumerate(self.label_groups.items()):
                    self.label_counts[label] = int(self.nb_samples * weights[label])
                    curr_nb_samples += self.label_counts[label]
                    if max_sample_label is None or len(self.label_groups[label]) > len(self.label_groups[max_sample_label]):
                        max_sample_label = label
                if curr_nb_samples != self.nb_samples:
                    self.label_counts[max_sample_label] += self.nb_samples - curr_nb_samples

    def set_epoch(self, epoch=0):
        """Sets the current epoch number in order to offset the RNG state for sampling."""
        if not isinstance(epoch, int) or epoch < 0:
            raise AssertionError("invalid epoch value")
        self.epoch = epoch

    def __iter__(self):
        """Returns the list of rebalanced sample indices to load.

        Note that the indices are repicked every time this function is called, meaning that samples
        eliminated due to undersampling (or duplicated due to oversampling) might not receive the same
        treatment twice.

        This function will reseed the RNGs it uses every time it is called, and revert their state before
        returning its output.
        """
        if self.nb_samples == 0:
            self.epoch += 1
            return iter([])
        rng_state = None
        if "torch" in self.seeds:
            rng_state = torch.random.get_rng_state()
            torch.random.manual_seed(self.seeds["torch"] + self.epoch)
        result = None
        if self.stype == "random":
            result = (self.indices[idx] for idx in torch.multinomial(
                torch.FloatTensor(self.sample_weights),self.nb_samples, replacement=True))
        elif self.stype == "uniform" or "root" in self.stype:
            indices = []
            for label, count in self.label_counts.items():
                max_samples = len(self.label_groups[label])
                while count > 0:
                    subidxs = torch.randperm(max_samples)
                    for subidx in range(min(count, max_samples)):
                        indices.append(self.label_groups[label][subidxs[subidx]])
                    count -= max_samples
            if len(indices) != self.nb_samples:
                raise AssertionError("messed up something internally...")
            result = (indices[i] for i in torch.randperm(len(indices)))
        if rng_state is not None:
            torch.random.set_rng_state(rng_state)
        self.epoch += 1
        return result

    def __len__(self):
        """Returns the number of sample indices that will be generated by this interface.

        This number is the scaled size of the originally provided sample indices list.
        """
        return self.nb_samples


class SubsetRandomSampler(torch.utils.data.sampler.Sampler):
    r"""Samples elements randomly from a given list of indices, without replacement.

    This specialization handles seeding based on the epoch number, and scaling (via duplication/decimation)
    of samples.

    Arguments:
        indices (list): a list of indices
        seeds (dict): dictionary of seeds to use when initializing RNG state.
        epoch (int): epoch number used to reinitialize the RNG to an epoch-specific state.
        scale (float): scaling factor used to increase/decrease the final number of samples.
    """

    def __init__(self, indices, seeds=None, epoch=0, scale=1.0):
        super().__init__(indices)
        self.seeds = {}
        if seeds is not None:
            if not isinstance(seeds, dict):
                raise AssertionError("unexpected seed pack type")
            self.seeds = seeds
        if not isinstance(epoch, int) or epoch < 0:
            raise AssertionError("invalid epoch value")
        self.epoch = epoch
        self.indices = indices
        if not isinstance(scale, (float, int)) or scale < 0:
            raise AssertionError("invalid scale parameter; should be greater than zero")
        self.num_samples = int(round(len(self.indices) * scale))

    def set_epoch(self, epoch=0):
        """Sets the current epoch number in order to offset the RNG state for sampling."""
        if not isinstance(epoch, int) or epoch < -1:
            raise AssertionError("invalid epoch value")
        self.epoch = epoch

    def __iter__(self):
        rng_state = None
        if "torch" in self.seeds:
            rng_state = torch.random.get_rng_state()
            torch.random.manual_seed(self.seeds["torch"] + self.epoch)
        indices = []
        max_samples = len(self.indices)
        req_count = self.num_samples
        while req_count > 0:
            subidxs = torch.randperm(max_samples)
            for subidx in range(min(req_count, max_samples)):
                indices.append(self.indices[subidxs[subidx]])
            req_count -= max_samples
        result = (indices[i] for i in torch.randperm(len(indices)))
        if rng_state is not None:
            torch.random.set_rng_state(rng_state)
        self.epoch += 1
        return result

    def __len__(self):
        return self.num_samples


class SubsetSequentialSampler(torch.utils.data.sampler.Sampler):
    r"""Samples element indices sequentially, always in the same order.

    Arguments:
        indices (list): a list of indices
    """

    def __init__(self, indices):
        super().__init__(indices)
        self.indices = indices

    def __iter__(self):
        return iter(self.indices)

    def __len__(self):
        return len(self.indices)
