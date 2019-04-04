from sklearn.naive_bayes import MultinomialNB
from text_classifikation.classifiers import BaseClassifier


class NaiveTextClassifier(BaseClassifier):
    def __init__(self, name="naive"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return MultinomialNB()

    @property
    def parameters(self):
        return {'features__text__vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'features__text__tfidf__use_idf': (True, False),
                'clf__fit_prior': (True, False)}



if __name__ == '__main__':
    train = True
    clf = NaiveTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)