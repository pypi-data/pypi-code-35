from sklearn.ensemble import AdaBoostClassifier
from text_classifikation.classifiers import BaseClassifier


class AdaBoostTextClassifier(BaseClassifier):
    def __init__(self, name="adaboost"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return AdaBoostClassifier()


if __name__ == '__main__':
    train = True
    clf = AdaBoostTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)
