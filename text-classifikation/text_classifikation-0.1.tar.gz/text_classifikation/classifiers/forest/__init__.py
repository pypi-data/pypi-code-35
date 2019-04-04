from sklearn.ensemble import RandomForestClassifier
from text_classifikation.classifiers import BaseClassifier


class ForestTextClassifier(BaseClassifier):
    def __init__(self, name="forest"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return RandomForestClassifier(n_estimators=200, random_state=42)



if __name__ == '__main__':
    train = True
    clf = ForestTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)
