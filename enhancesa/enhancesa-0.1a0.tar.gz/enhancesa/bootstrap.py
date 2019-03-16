# TODO: Add more test statistics, a whole table preferably.

# Dependencies
import numpy as np
import pandas as pd



def bootstrap(X, iters=1):
    """ Estimate population mu and SE of a sample with boothstrap subset selection method.  
    For a quick intro, got `here <https://alisiina.github.io/2019/02/13/resampling-methods.html>`_.

    Parameters
    ----------
    X : an array/series object
        A fitted Statsmodels ols model.  
    iters : int, optional
        The number of resampling iterations. Usually a large value, e.g. 1000
    
    Returns
    -------
    DataFrame or Series object
        Contains estimated population mean and stadnard deviation of :math:`n` 
        samples from the the given ``x`` sample.
     
    Examples
    --------
    >>> x = np.random.normal(size=100)
    >>> enhancesa.bootstrap(x, iters=1000)
    Estimated mean: -0.025309
    Estimated SE: 0.095531
    dtype: float64
    """
    
    # By convention, n is usually length of the sample
    n = len(X)
    
    # Random n index numbers
    idx = np.random.randint(0, n , (iters, n))
    
    # Stores n random samples, each of size n
    samples = []
    
    means = []
    std_devs = []
    
    for i in range(0, len(idx)):
        samples.append(X[idx[i]])
        means.append(samples[i].mean())
        std_devs.append(np.std(samples[i]))
    
    total_mean = np.mean(means)
    se = np.mean(std_devs)/np.sqrt(n)
    
    return pd.Series({'Estimated mean': total_mean, 'Estimated SE': se},
                    dtype='float64') # If dtype not given, dtype is inferred.

    # Add confidence interval this way:
    # >>> results = bootstrap(boston['medv'], iters=1000)
    # >>> print('Confidence interval:', results[0]-2*results[1], results[0]+2*results[1])