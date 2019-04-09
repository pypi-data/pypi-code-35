from sklearn.base import BaseEstimator, TransformerMixin
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


class janome_test(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        # ["私の名前は〜〜です。"]→この形で入力が入ってくる想定（pythonのlistで入ってくる想定）
        t = Tokenizer()
        surface_list = []
        for sentence in X:
            token_list = t.tokenize(sentence)
            temp_sentence = ""
            for mor in token_list:
                temp_sentence += " " + mor.surface
            temp_sentence = temp_sentence.strip()
            surface_list.append(temp_sentence)

        # tf-idfでベクトル化
        vectorizer = TfidfVectorizer(
            use_idf=True, token_pattern=r"(\b\w+-*\w*\b)")
        vecs = vectorizer.fit_transform(surface_list)
        vecslist = vecs.toarray()

        pca = PCA(n_components=50)
        x_pca = pca.fit_transform(vecslist)

        return x_pca

    def transform(self, X, y=None):  # こっちが呼ばれて実行されているらしい。。。
        # ["私の名前は〜〜です。"]→この形で入力が入ってくる想定（pythonのlistで入ってくる想定）
        t = Tokenizer()
        surface_list = []
        for sentence in X:
            token_list = t.tokenize(sentence)
            temp_sentence = ""
            for mor in token_list:
                temp_sentence += " " + mor.surface
            temp_sentence = temp_sentence.strip()
            surface_list.append(temp_sentence)

        # tf-idfでベクトル化
        vectorizer = TfidfVectorizer(
            use_idf=True, token_pattern=r"(\b\w+-*\w*\b)")
        vecs = vectorizer.fit_transform(surface_list)
        vecslist = vecs.toarray()

        pca = PCA(n_components=50)
        x_pca = pca.fit_transform(vecslist)

        return x_pca

    def fit_transform(self, X, y=None):
        # self.fit(X, y)
        return self.transform(X, y)
