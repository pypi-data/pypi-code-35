from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np


class PcaEV(Pipeline):
    """Principal component analysis (PCA) with the number of components
    set to reach a required explained variance.

    Parameters
    ----------
    required_ev : float (Default 0.1)
        Required Explained Variance threshold.

    Example
    -------
        trans = PcaEV()
        trans.set_params(**{'required_ev': 0.2})
        trans.fit(X_train)
        X_new = trans.transform(X_train)

    Notes
    -----
    The class 'PcaEV' is a sklearn Pipeline and is equivalent to

        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        required_ev = 0.1
        trans = Pipeline(steps=[
            ('scl', StandardScaler()),
            ('pca', PCA(n_components = required_ev, svd_solver='full'))
        ])
        trans.fit(X_train)
        X_new = trans.transform(X_train).astype(np.float16)

    PcaEV
        - runs checks that "0.0 < PCA.n_components < 1.0",
        - transformed outputs are memory-friendly (np.float16),
        - create "feature_names_" output
    """
    def __init__(self, required_ev=0.1, prefix="pcaev"):
        self.prefix = prefix
        self.required_ev = required_ev
        super().__init__(steps=[
            ('scl', StandardScaler(with_mean=True, with_std=True, copy=True)),
            ('pca', PCA(
                n_components=self.required_ev,
                svd_solver='full', whiten=False, copy=True))
        ])

    def __str__(self):
        return 'required_ev={}, steps={}, prefix={}'.format(
            self.required_ev, self.steps, self.prefix)

    def set_params(self, **kwargs):
        if 'required_ev' in kwargs:
            self.required_ev = kwargs['required_ev']
            self.steps[1][1].set_params(**{'n_components': self.required_ev})

    def transform(self, X, y=None):
        return super().transform(X).astype(np.float16)

    def fit(self, X, y=None):
        super().fit(X)
        self.feature_names_ = [
            self.prefix + "_" + str(i) for i in
            range(self.steps[1][1].n_components_)]
        return self


trans = PcaEV(required_ev=0.1)

meta = {
    'id': 'dim3',
    'name': 'PCA req EV',
    'description': (
        "Number of components is determined by "
        "a required Explained Variance threshold"),
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA', 'Explained Variance']
}
