from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

trans = Pipeline(steps=[
    ('scl', StandardScaler(with_mean=True, with_std=True, copy=True)),
    ('pca', PCA(
        n_components='mle', svd_solver='full', whiten=False, copy=True))
])

meta = {
    'id': 'dim2',
    'name': 'PCA Minka MLE',
    'description': "Minka's MLE to guess n_components",
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA', 'Minka MLE']
}
