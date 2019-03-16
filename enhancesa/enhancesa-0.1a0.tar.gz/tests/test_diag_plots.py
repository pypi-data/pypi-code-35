from enhancesa import diag_plots

# Import dependencies for testing
from statsmodels.formula.api import ols
import numpy as np
from pandas import DataFrame

def test_diag_plots():
    x = np.random.uniform(size=100)
    y = 2 + 0.5*x + np.random.normal(size=100)

    df = DataFrame(data={'x':x, 'y':y})
    model = ols('y ~ x', data=df).fit()

    assert diag_plots(model, y) is None
    #  NOTE: This is a type(None) object.
    # Go to https://matplotlib.org/devel/testing.html for a better testing method.
    # Also, functions that do not have explicit return values return None:
    # https://docs.python.org/3/library/stdtypes.html#the-null-object
    # !!!: This test isn't really testing whether plots are properly generated.