from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np


class PcaMinka(Pipeline):
    """Principal component analysis (PCA) with Minka's MLE
    to guess n_components.

    Example
    -------
        trans = PcaMinka()
        trans.fit(X_train)
        X_new = trans.transform(X_train)

    Notes
    -----
    The class 'PcaMinka' is a sklearn Pipeline and is equivalent to

        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        trans = Pipeline(steps=[
            ('scl', StandardScaler(with_mean=True, with_std=True, copy=True)),
            ('pca', PCA(
                n_components='mle', svd_solver='full',
                whiten=False, copy=True))
        ])
        trans.fit(X_train)
        X_new = trans.transform(X_train).astype(np.float16)
    """
    def __init__(self, prefix="minka"):
        self.prefix = prefix
        super().__init__(steps=[
            ('scl', StandardScaler(with_mean=True, with_std=True, copy=True)),
            ('pca', PCA(
                n_components='mle', svd_solver='full',
                whiten=False, copy=True))
        ])

    def transform(self, X, y=None):
        return super().transform(X).astype(np.float16)

    def fit(self, X, y=None):
        super().fit(X)
        self.feature_names_ = [
            self.prefix + "_" + str(i) for i in
            range(self.steps[1][1].n_components_)]
        return self


trans = PcaMinka()

meta = {
    'id': 'dim2',
    'name': 'PCA Minka MLE',
    'description': "Minka's MLE to guess n_components",
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA', 'Minka MLE']
}
