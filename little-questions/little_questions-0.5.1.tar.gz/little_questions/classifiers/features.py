from little_questions.settings import AFFIRMATIONS
from little_questions.parsers import BasicQuestionParser
from little_questions.parsers.neural import NeuralQuestionParser
from sklearn.base import BaseEstimator, TransformerMixin


class DictTransformer(BaseEstimator, TransformerMixin):
    """ transofmr a list of sentences into a list of dicts """
    parser = BasicQuestionParser()

    def fit(self, *args, **kwargs):
        return self

    def transform(self, X, **transform_params):
        feats = []
        for sent in X:
            sent = sent.strip().lower().replace("``", "").replace("''", "")\
                .replace(" '", "'")
            feats.append(self.parser.parse(sent))

        return feats


class NeuralDictTransformer(DictTransformer):
    """ transofmr a list of sentences into a list of dicts """
    parser = NeuralQuestionParser()

