from sklearn.linear_model import PassiveAggressiveClassifier
from text_classifikation.classifiers import BaseClassifier


class PassiveAggressiveTextClassifier(BaseClassifier):
    def __init__(self, name="passive_agressive"):
        super().__init__(name)

    @property
    def classifier_class(self):
        return PassiveAggressiveClassifier(loss="hinge")



if __name__ == '__main__':
    train = True
    search = True
    name = "sentences_pa"
    clf = PassiveAggressiveTextClassifier(name)
    train_data_path = "/home/user/PycharmProjects/text_classification/text_classifikation/data/sentences.txt"
    test_data_path = "/home/user/PycharmProjects/text_classification" \
                     "/text_classifikation/data/sentences_test.txt"
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
