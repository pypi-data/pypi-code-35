from sklearn.linear_model import SGDClassifier
from text_classifikation.classifiers import BaseClassifier


class SGDTextClassifier(BaseClassifier):
    def __init__(self):
        super().__init__("sgd")

    @property
    def classifier_class(self):
        return SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3,
                             n_iter=5, random_state=42)

    @property
    def parameters(self):
        return {'features__text__vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'features__text__tfidf__use_idf': (True, False),
                'clf__early_stopping': (True, False),
                'clf__shuffle': (True, False),
                'clf__learning_rate': ('constant', 'optimal', 'adaptive',
                                       'invscaling'),
                'clf__penalty': ('l1', 'l2', 'elasticnet'),
                'clf__loss': ('hinge', 'log', 'modified_huber',
                              'squared_hinge', 'perceptron'),
                'clf__fit_intercept': (True, False)}


if __name__ == '__main__':
    train = True
    clf = SGDTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)
