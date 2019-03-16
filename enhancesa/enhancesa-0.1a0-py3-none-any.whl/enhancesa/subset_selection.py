# Dependencies
from tqdm import tqdm
import statsmodels.api as sm
import pandas as pd
import itertools
import numpy as np

# TODO: Implement the plot method for SubsetSelect
# TODO: Try out adding this helper functions as static methods to the 
# SubsetSelect class. https://realpython.com/instance-class-and-static-methods-demystified/


def _get_rss(X, y, feature_names):
    """Fits a ``statsmodels.OLS`` function, returns RSS of the model."""
    X = sm.add_constant(X[list(feature_names)])
    model = sm.OLS(y, X[list(feature_names)]).fit()
    RSS = ((model.predict(X[list(feature_names)]) - y) ** 2).sum()

    return {'Model': model, 'RSS': RSS}


def _best_select(X, y, K):
    """Carries out best subset selection, where best is defined by
    RSS of the model.
    """
    results = []
    for combo in itertools.combinations(X.columns, K):
        results.append(_get_rss(X, y, combo))
    all_models =  pd.DataFrame(results)

    return all_models.loc[all_models["RSS"].idxmin()] 


def _forward_select(X, y, feature_names):
    """Carries out forward stepwise selection, returning the model with
    the lowest RSS.
    """
    remaining_predictors = [p for p in X.columns if p not in feature_names]
    results = []
    for p in remaining_predictors:
        results.append(_get_rss(X, y, feature_names+[p]))  
    all_models =  pd.DataFrame(results)

    return all_models.loc[all_models["RSS"].idxmin()]


def _backward_select(X, y, feature_names):
    """Carries out backward stepwise selection, returning the model with
    the lowest RSS.
    """
    results = []
    for combo in itertools.combinations(feature_names, len(feature_names)-1):
        results.append(_get_rss(X, y, combo))
    all_models =  pd.DataFrame(results)

    return all_models.loc[all_models["RSS"].idxmin()]


class SubsetSelect:
    """ Goes through all features and finds the ones that are best predictors 
    of a response :math:`y`.

    Parameters
    ----------
    method : str, default='best'
        Subset selection method. Currently implemented subset selection methods
        are ``best``, ``forward`` stepwise, and ``backward`` stepwise.

    """
    def __init__(self, method='best'):
        self.method = method

    def fit(self, X, y):
        """ Fits a subset selection method to the data. 

        Parameters
        ----------
        X : a multidimensional array or dataframe object
            This is X predictor variables.
        y : an array or Series object
            The target or response variable.

        Returns
        -------
        DataFrame object 
            A dataframe with the best models selected by the given
            ``method`` parameter and their corresponding residual sum of squares (RSS).

        Examples
        --------
        >>> from enhancesa.subset_selection import SubsetSelect
        >>> from sklearn.preprocessing import PolynomialFeatures
        >>> # Generate data
        >>> X = np.random.normal(size=100)
        >>> y = 0.5 + 2*X - 5*(X**2) + 3*(X**3) + np.random.normal(size=100)
        >>> # Make it a model with polynomial features
        >>> poly = PolynomialFeatures(degree=10, include_bias=False)
        >>> X_arr = poly.fit_transform(X[:, np.newaxis])
        >>> # Put them in a dataframe, coz SubsetSelect accepts dataframe only (yet)
        >>> col_names = ['Y']+['X'+ str(i) for i in range(1, 11)]
        >>> df = pd.DataFrame(np.concatenate((y[:, np.newaxis], X_arr), axis=1), columns=col_names)
        >>> subsets = SubsetSelect(method='best').fit(df.iloc[:,1:], df.iloc[:,0])
        100%|██████████| 10/10 [00:05<00:00,  1.97it/s]
        """
        if self.method == 'best':
            best_models = pd.DataFrame(columns=['Model', 'RSS'])
            for k in tqdm(range(1, X.shape[1] + 1)):
                best_models.loc[k] = _best_select(X, y, k)

            return best_models

        elif self.method == 'forward':
            forward_models = pd.DataFrame(columns=['Model', 'RSS'])
            feature_list = []
            for k in tqdm(range(1, X.shape[1] + 1)):
                forward_models.loc[k] = _forward_select(X, y, feature_list)
                feature_list = forward_models.loc[k]['Model'].model.exog_names

            return forward_models

        elif self.method == 'backward':
            backward_models = pd.DataFrame(columns=['Model', 'RSS'], index=range(1, X.shape[1]))
    
            if isinstance(X, pd.DataFrame):
                feature_list = X.columns
            elif isinstance(X, np.ndarray): # FIXME: what to do if numpy array of X?
                raise NotImplementedError('Current version only supports X to \
                                            be a Pandas DataFrame.')    
            else:
                raise TypeError('X can only be Numpy array or Pandas dataframe.')

            while len(feature_list) > 1:
                backward_models.loc[len(feature_list)] = _backward_select(X, y, feature_list)
                feature_list = backward_models.loc[len(feature_list)]['Model'].model.exog_names

            return backward_models
        
        else:
            raise ValueError('Invalid method for subset selection.')
