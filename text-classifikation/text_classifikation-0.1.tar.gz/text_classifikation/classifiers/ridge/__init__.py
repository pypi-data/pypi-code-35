from sklearn.linear_model import RidgeClassifier
from text_classifikation.classifiers import BaseClassifier


class RidgeTextClassifier(BaseClassifier):
    def __init__(self, name="ridge"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return RidgeClassifier(solver="lbfgs")



if __name__ == '__main__':
    train = True
    search = False
    clf = RidgeTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)