from enhancesa import bootstrap

# Dependencies
import pandas as pd 
import numpy as np 

def test_bootstrap():
    x = np.random.normal(size=100)
    result = bootstrap(x, iters=1000)
    assert isinstance(result, pd.Series)