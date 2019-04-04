from os.path import join, isfile

from text_classifikation.settings import MODELS_PATH
from text_classifikation.classifiers.pipelines import pipeline__text, \
    pipeline__lemma_w2v, default_pipelines,  default_pipeline_unions
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, \
    confusion_matrix

import json

from pprint import pprint


class BaseClassifier(object):
    def __init__(self, name):
        self.name = name.replace('_model.pkl', "")
        self.text_clf = None

    def find_best_pipeline(self, train_data, target_data, test_data,
                           test_label, pipelines=None, unions=None,
                           outfolder=None, save_all=False,
                           skip_existing=True, verbose=True, save_best=True):
        pipelines = pipelines or default_pipelines
        unions = unions or default_pipeline_unions
        if verbose:
            from pprint import pprint
            print("Finding best out of ")
            pprint(sorted(list(pipelines.keys()) + list(unions.keys())))
        best_score = 0
        best_clf = None
        outfolder = outfolder or MODELS_PATH
        acs = {}
        if isfile(join(outfolder, self.name + "_acc.json")):
            with open(join(outfolder, self.name + "_acc.json"), "r") as f:
                acs = json.load(f)

            if verbose:
                print("resuming from ")
                pprint(acs)
                best_pipeline = max(acs, key=lambda key: acs[key])
                print("MAX", best_pipeline, acs[best_pipeline])
        for p in pipelines:
            if p in acs:
                print("skipping", p)
                continue
            try:
                path = join(outfolder, self.name + "_" + p + '_model.pkl')
                if isfile(path) and skip_existing:
                    if verbose:
                        print("already fitted ", self.name + "_" + p, "SKIPPING")

                    #if accuracy > best_score:
                    #    best_clf = clf
                    #    best_pipeline = p
                    #    best_score = accuracy
                    #clf = joblib.load(path)
                    #preds = clf.predict(test_data)
                    #accuracy = accuracy_score(test_label, preds)
                    #acs[p] = accuracy
                    #if verbose:
                    #    print(p, "Accuracy:", accuracy)
                    if self.name + "_" + p not in acs:
                        with open(join(outfolder, self.name + "_acc.json"),
                                  "w") as f:
                            json.dump(acs, f, indent=4)
                    continue

                if verbose:
                    print("fitting", p)
                line = [
                    ('features', pipelines[p]),
                    ('clf', self.classifier_class)
                ]
                clf = Pipeline(line)
                clf.fit(train_data, target_data)
                preds = clf.predict(test_data)
                accuracy = accuracy_score(test_label, preds)
                acs[p] = accuracy
                if verbose:
                    print(p, "Accuracy:", accuracy)
                with open(join(outfolder, self.name + "_acc.json"), "w") as f:
                    json.dump(acs, f, indent=4)
                if accuracy > best_score:
                    best_score = accuracy
                    best_clf = clf
                if save_all:
                    joblib.dump(clf, path)
            except Exception as e:
                if verbose:
                    print(e)
                    print("bad pipeline", p)

        for p in unions:
            if p in acs:
                continue
            try:
                path = join(outfolder, self.name + "_" + p + '_model.pkl')
                if isfile(path) and skip_existing:
                    continue
                line = [
                    ('features', unions[p]),
                    ('clf', self.classifier_class)
                ]
                clf = Pipeline(line)
                clf.fit(train_data, target_data)
                preds = clf.predict(test_data)
                accuracy = accuracy_score(test_label, preds)
                acs[p] = accuracy
                if verbose:
                    print(p, "Accuracy:", accuracy)
                with open(join(outfolder, self.name + "_acc.json"), "w") as f:
                    json.dump(acs, f, indent=4, sort_keys=True)
                if accuracy > best_score:
                    best_score = accuracy
                    best_clf = clf
                if save_all:
                    joblib.dump(clf, path)
            except Exception as e:
                if verbose:
                    print(e)
                    print("bad union", p)
        best_pipeline = max(acs, key=lambda key: acs[key])
        if verbose:
            print("MAX", best_pipeline, acs[best_pipeline])
        if not save_all and save_best and best_clf:
            path = join(outfolder, self.name + "_" + best_pipeline + '_model.pkl')
            if verbose:
                print("Saving best model", path)
            joblib.dump(best_clf, path)
        return acs[best_pipeline], best_pipeline, acs

    def train(self, train_data, target_data):
        self.text_clf = Pipeline(self.pipeline)
        self.text_clf.fit(train_data, target_data)
        return self.text_clf

    @property
    def pipeline(self):
        return [
            ('features', pipeline__text),
            ('clf', self.classifier_class)
        ]

    @property
    def classifier_class(self):
        raise NotImplementedError

    @property
    def parameters(self):
        return {'features__vect__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'features__tfidf__use_idf': (True, False)}

    def grid_search(self, train_data, target_data):
        self.text_clf = Pipeline(self.pipeline)
        gs_clf = GridSearchCV(self.text_clf, self.parameters, n_jobs=-1)
        gs_clf = gs_clf.fit(train_data, target_data)
        print("best_score", gs_clf.best_score_)
        print("best_params", gs_clf.best_params_)
        return gs_clf

    def predict(self, text):
        return self.text_clf.predict(text)

    def save(self, path=None):
        path = path or join(MODELS_PATH, self.name + '_model.pkl')
        joblib.dump(self.text_clf, path)

    def load(self, path=None):
        path = path or join(MODELS_PATH, self.name + '_model.pkl')
        self.text_clf = joblib.load(path)
        return self

    def load_data(self, filename):
        raise NotImplementedError
        return train_data, target_data

    def load_test_data(self, filename):
        return self.load_data(filename)

    def evaluate_model(self, path):
        X_test, y_test = self.load_test_data(path)
        preds = self.predict(X_test)
        accuracy = accuracy_score(y_test, preds)
        report = classification_report(y_test, preds)
        matrix = confusion_matrix(y_test, preds)
        return accuracy, report, matrix
