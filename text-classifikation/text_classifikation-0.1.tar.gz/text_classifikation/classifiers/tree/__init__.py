from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from text_classifikation.classifiers import BaseClassifier


class TreeTextClassifier(BaseClassifier):
    def __init__(self, name="tree"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return DecisionTreeClassifier()


class ExtraTreeTextClassifier(BaseClassifier):
    def __init__(self, name="extra_tree"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return ExtraTreeClassifier()


if __name__ == '__main__':
    train = True
    clf = TreeTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)
