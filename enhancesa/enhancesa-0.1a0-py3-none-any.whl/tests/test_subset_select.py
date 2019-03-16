from enhancesa import SubsetSelect


# Dependencies
import numpy as np
import pandas as pd 


class TestSubsetSelect():

    # NOTE: To pd.DataFrame because current version of SubsetSelect only
    # accepts DataFrame inputs, numpy.array not yet implemented. In future,
    # this class should also test SubsetSelect for Numpy arrays as well.
    # df = pd.DataFrame(np.random.normal(size=(100, 11)))    
    df = pd.DataFrame(np.random.normal(size=(100, 11)))
    
    def test_best(self):
        best_subsets = SubsetSelect(method='best').fit(self.df.iloc[:,1:], self.df.iloc[:,0])
        assert isinstance(best_subsets, pd.DataFrame) and best_subsets.empty is False

    def test_forward(self):
        forward_subsets = SubsetSelect(method='forward').fit(self.df.iloc[:,1:], self.df.iloc[:,0])
        assert isinstance(forward_subsets, pd.DataFrame) and forward_subsets.empty is False

    def test_backward(self):
        backward_subsets = SubsetSelect(method='backward').fit(self.df.iloc[:,1:], self.df.iloc[:,0])
        assert isinstance(backward_subsets, pd.DataFrame) and backward_subsets.empty is False
    