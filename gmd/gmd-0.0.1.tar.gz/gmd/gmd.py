"""
This is the scikit-learn compatible gmd module
"""
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils import check_random_state
from sklearn.utils.validation import check_array, check_is_fitted
from libgmdc import avg_deviation
from libgmdc import set_seed

class GMD(BaseEstimator):
    """GMD Estimator. Used to compute interesting subspaces in a dataset.
    """
    def __init__(self, alpha=0.1, runs=100, random_state=None):
        """Constructor for the GMD class

        Parameters
        ----------
        alpha :: float, default=0.1
            Determines the slice slice.
        runs :: int, default=100
            Number of Monte Carlo iterations
        random_state :: int, default=None
            Used to seed the C PRNG
        """
        self.alpha = alpha
        self.runs = runs
        self.random_state = random_state

    def fit(self, X, y=None):
        """Compute the interesting subspaces. The result can be found in `subspaces_`.

        Parameters
        ----------
        X :: {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.
        y :: default=None,
            Not used in the unsupervised setting.

        Returns
        -------
        self :: object
            Returns self.
        """
        self._deviations = None
        self.is_fitted_ = False
        self.subspaces_ = {}
        self._sorted = None
        set_seed(self.random_state)

        X = check_array(X, ensure_min_samples=2)

        res = np.empty_like(X, dtype=np.int32)
        self._sorted = np.concatenate([X, np.array([range(0, len(X))]).T], axis=1)
        for i in range(X.shape[1]):
            self._sorted = self._sorted[self._sorted[:, i].argsort(kind='mergesort')]
            res[:, i] = self._sorted[:, -1]
        self._sorted = res.astype(np.int32)
  
        self.subspaces_ = self._interesting_subspaces()
        
        self.is_fitted_ = True
        return self

    def _avg_devation(self, subspaces, reference_dim):
        """
        Compute the deviation in a subspace given the reference dimension.

        Parameters
        ----------
        subspaces : orthogonal projections defining the constraints of the hypercube
        reference_dim : the unconstrained projection

        Returns
        -------
        float with the deviation of the subspaces wrt. the reference_dim
        """
        return avg_deviation(self._sorted, np.array(subspaces, dtype=np.int32), reference_dim, self.alpha, self.runs)

    def _deviation_matrix(self):
        """
        Compute the deviation of each pair of dimensions. Runs lazily.

        Returns
        -------
        2-D array m x m, m being the count of attributes
        """
        if self._deviations is None:
            cols = self._sorted.shape[1]
            out = np.zeros((cols, cols))
            for i in range(cols):
                for j in range(cols): # TODO: use symmetry
                    if i != j:
                        res = self._avg_devation([i, j], i)
                        out[i, j] = res
            self._deviations = out
        return self._deviations
    
    def _max_deviation_subspaces(self, reference_dimension):
        subspaces = []
        deviations = self._deviation_matrix() # TODO: only use vector here
        sorted_indices = np.argsort(deviations[reference_dimension]) # highest is last
        current_max = -1
        subspaces.append(reference_dimension)
        for i in reversed(sorted_indices):
            if i != reference_dimension:
                subspaces.append(i)
                tmp = self._avg_devation(subspaces, reference_dimension)
                if tmp < current_max:
                    subspaces.pop()
                else:
                    current_max = tmp
        return subspaces
    
    def _interesting_subspaces(self):
        res = {}
        for i in range(self._sorted.shape[1]):
            res[i] = self._max_deviation_subspaces(i)
        return res