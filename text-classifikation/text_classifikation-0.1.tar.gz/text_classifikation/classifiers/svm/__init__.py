from sklearn.svm import SVC, LinearSVC
from text_classifikation.classifiers import BaseClassifier


class SVCTextClassifier(BaseClassifier):
    def __init__(self, name="svc"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return SVC(kernel='poly')

    @property
    def parameters(self):
        return {'features__text__vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'features__text__tfidf__use_idf': (True, False),
                'clf__probability': (True, False),
                'clf__shrinking': (True, False),
                'clf__kernel': ('linear', 'poly', 'rbf', 'sigmoid',
                                'precomputed'),
                'clf__decision_function_shape': ('ovo', 'ovr')}


class LinearSVCTextClassifier(BaseClassifier):
    def __init__(self, name="linear_svc"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return LinearSVC()

    @property
    def parameters(self):
        return {'features__text__vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'features__text__tfidf__use_idf': (True, False),
                'clf__probability': (True, False),
                'clf__shrinking': (True, False),
                'clf__kernel': ('linear', 'poly', 'rbf', 'sigmoid',
                                'precomputed'),
                'clf__decision_function_shape': ('ovo', 'ovr')}


if __name__ == '__main__':
    train = True
    clf = LinearSVCTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)

