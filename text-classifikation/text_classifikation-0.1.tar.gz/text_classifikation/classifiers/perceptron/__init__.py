from sklearn.linear_model import Perceptron
from text_classifikation.classifiers import BaseClassifier


class PerceptronTextClassifier(BaseClassifier):
    def __init__(self, name="perceptron"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return Perceptron()




if __name__ == '__main__':
    train = True
    search = False
    clf = PerceptronTextClassifier()
    train_data_path = ""
    test_data_path = ""
    if train:
        t, t_label = clf.load_data(train_data_path)
        clf.train(t, t_label)
        clf.save()
    else:
        clf.load()
    clf.evaluate_model(test_data_path)

