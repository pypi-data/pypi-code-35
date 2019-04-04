from sklearn.linear_model import LogisticRegression
from text_classifikation.classifiers import BaseClassifier


class LogRegTextClassifier(BaseClassifier):
    def __init__(self, name):
        super().__init__(name or "logreg")

    @property
    def classifier_class(self):
        return LogisticRegression(multi_class="multinomial",
                                  solver="lbfgs")

    @property
    def parameters(self):
        return {'features__text__vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'features__text__tfidf__use_idf': (True, False),
                'clf__warm_start': (True, False),
                'clf__solver': (
                    'newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga')}


if __name__ == '__main__':
    train = True
    search = True
    name = "questions_lr"
    clf = LogRegTextClassifier(name)
    train_data_path = "/home/user/PycharmProjects/text_classification/text_classifikation/data/questions.txt"
    test_data_path = "/home/user/PycharmProjects/text_classification" \
                     "/text_classifikation/data/questions_test.txt"
    if search:
        train, train_label = clf.load_data(train_data_path)
        test, test_label = clf.load_data(test_data_path)
        best_score, best_pipeline = clf.find_best_pipeline(train, train_label,
                                                           test, test_label)
        print("BEST:", best_pipeline, "ACCURACY", best_score)
        exit(0)

    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)