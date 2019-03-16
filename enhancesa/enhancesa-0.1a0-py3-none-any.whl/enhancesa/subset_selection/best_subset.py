# Dependencies
from tqdm import tqdm



class BestSubset(object):
    """ Goes through all features and finds the ones that are best predictors of a response `Y`.

    Parameters
    --------- 
    X : multidimentional array object, or a pandas dataframe
        The independent variables in a model
    y : array or series object
        The dependent variable (also called response or target variable)
     
    Example
    --------
    >>> from enhancesa.subset_selection import BestSubset
    >>> X = np.random.normal(size=100)
    >>> y = 2 + 0.3*X + np.random.normal(size=100)
    >>> BestSubset().fit(X, y)
    some output here
    """
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __new__(self):
        return list() # returns empty list when class is called

    def fit(self):
        pass
    