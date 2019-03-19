#! /usr/bin/env python3
import sys
import os
import gzip
import dill as pickle

import numpy as np
import pandas as pd

import keras
from keras.utils import to_categorical
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D, InputLayer
from keras.layers import Dropout, LSTM, Bidirectional, GlobalMaxPool1D
import keras.backend as K
from keras.models import load_model, model_from_json

import types
import module

if len(sys.argv) > 1:
    experimentParams = {
        "label": sys.argv[1],
        "name": sys.argv[2],
        "group": sys.argv[3],
        "testSplit": 0.2,
        "devSplit": 0.2,
        "acceptanceF1": 0.90,
        "owner": sys.argv[4],
        "model": sys.argv[5],
        "location": sys.argv[6],
    }
else:
    experimentParams = {
        "testSplit": 0.2,
        "devSplit": 0.2,
        "acceptanceF1": 0.90,
        "location": "local",
    }

if experimentParams["location"] == "local":
    TRAINING_CSV_PATH = "data/raw_data_full_270918.csv"
    MODEL_OUTPUT_DIR = "artifacts"

elif experimentParams["location"] == "remote":
    TRAINING_CSV_PATH = "/storage/raw_data_full_270918.csv"
    MODEL_OUTPUT_DIR = "/artifacts"


class Text2Dataset:
    def __init__(self, wordNgrams=1, minCount=1):
        self.wordNgrams = wordNgrams
        self.minCount = minCount

        self.word2idx = None
        self.words2idx = None
        self.label2idx = None
        self.idx2label = None
        self.train_X = None
        self.train_y = None
        self.max_features = None
        self.token_indice = None
        self.max_len = None

    def preprocess(self, strings):
        preprocessed_strings = []

        for string in strings:
            text = (
                ",".join([words for words in string.split(",")])
                .strip()
                .replace("\n", "")
            )
            X = self.words2idx(text)
            X = self.add_ngram([X])
            X = sequence.pad_sequences(X, maxlen=self.max_len)
            preprocessed_strings.append(X)

        return preprocessed_strings

    def create_ngram_set(self, input_list, ngram_value=2):
        return set(zip(*[input_list[i:] for i in range(ngram_value)]))

    def add_ngram(self, sequences):
        new_sequences = []
        for input_list in sequences:
            new_list = input_list[:]
            for ngram_value in range(2, self.wordNgrams + 1):
                for i in range(len(new_list) - ngram_value + 1):
                    ngram = tuple(new_list[i : i + ngram_value])
                    if ngram in self.token_indice:
                        new_list.append(self.token_indice[ngram])
            new_sequences.append(new_list)

        return new_sequences

    def text2List(self, text_path, selected_set):
        # TODO: Fix naming of text_path which is not a path, its a dataframe
        # Load the full dataset and create train, dev, test sets
        train_set, dev_set, test_set, df = load_data_unvectorized(
            text_path,
            experimentParams["label"],
            dev=experimentParams["devSplit"],
            test=experimentParams["testSplit"],
        )
        if selected_set == 1:
            dataset = train_set
        elif selected_set == 2:
            dataset = dev_set
        elif selected_set == 3:
            dataset = test_set

        # Create lists of all sentences and labels in the selected set -> train/dev/test
        words_list = dataset["clean_text"].values.tolist()
        label_list = dataset["Label"].values.tolist()

        return words_list, label_list

    def loadTrain(self, text_path):
        words_list, label_list = self.text2List(text_path, 1)

        label_words_dict = {}
        for label, words in zip(label_list, words_list):
            if len(words) > self.minCount:
                if label in label_words_dict:
                    label_words_dict[label].append(words)
                else:
                    label_words_dict[label] = []

        self.label2idx = {label: idx for idx, label in enumerate(label_words_dict)}
        self.idx2label = {self.label2idx[label]: label for label in self.label2idx}
        self.word2idx = {
            word: idx for idx, word in enumerate(set(" ".join(words_list).split()))
        }
        self.words2idx = lambda words: [
            self.word2idx[word] for word in words.split() if word in self.word2idx
        ]

        self.train_X = [self.words2idx(words) for words in words_list]
        self.train_y = [self.label2idx[label] for label in label_list]
        self.max_features = len(self.word2idx)

        if self.wordNgrams > 1:
            print("Adding {}-gram features".format(self.wordNgrams))
            ngram_set = set()
            for input_list in self.train_X:
                for i in range(2, self.wordNgrams + 1):
                    set_of_ngram = self.create_ngram_set(input_list, ngram_value=i)
                    ngram_set.update(set_of_ngram)

            start_index = self.max_features + 1
            self.token_indice = {v: k + start_index for k, v in enumerate(ngram_set)}
            indice_token = {self.token_indice[k]: k for k in self.token_indice}

            self.max_features = np.max(list(indice_token.keys())) + 1

            self.train_X = self.add_ngram(self.train_X)

        return self.train_X, self.train_y

    def loadDatasets(self, text_path):
        ll = [1, 2, 3]
        X_list, y_list = [], []
        for data in ll:
            words_list, label_list = self.text2List(text_path, data)
            data_X = [self.words2idx(words) for words in words_list]
            data_y = [self.label2idx[label] for label in label_list]
            data_X = self.add_ngram(data_X)
            X_list.append(data_X)
            y_list.append(data_y)

        train_X, train_y = X_list[0], y_list[0]
        dev_X, dev_y = X_list[1], y_list[1]
        test_X, test_y = X_list[2], y_list[2]

        return train_X, train_y, dev_X, dev_y, test_X, test_y


class FastText:
    def __init__(self, wordNgrams=3, minCount=1, args=None):
        if args is None:
            self.text2Dataset = Text2Dataset(wordNgrams, minCount)

            self.max_features = None
            self.maxlen = None
            self.batch_size = None
            self.embedding_dims = None
            self.epochs = None
            self.lr = None
            self.num_classes = None
            self.model = None
        else:
            (
                wordNgrams,
                minCount,
                word2idx,
                label2idx,
                token_indice,
                max_len,
                self.max_features,
                self.maxlen,
                self.batch_size,
                self.embedding_dims,
                self.epochs,
                self.lr,
                self.num_classes,
                model_weights,
            ) = args
            self.text2Dataset = Text2Dataset(wordNgrams, minCount)
            self.text2Dataset.word2idx = word2idx
            self.text2Dataset.words2idx = lambda words: [
                word2idx[word] for word in words.split() if word in word2idx
            ]
            self.text2Dataset.label2idx = label2idx
            self.text2Dataset.idx2label = {
                label2idx[label]: label for label in label2idx
            }
            self.text2Dataset.token_indice = token_indice
            self.text2Dataset.max_len = max_len
            self.model = self.build_model(model_weights)

    def precision(self, y_true, y_pred):
        agreement = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        true_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        precision = agreement / (predicted_positives + K.epsilon())

        return precision

    def recall(self, y_true, y_pred):
        agreement = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        true_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = agreement / (true_positives + K.epsilon())

        return recall

    def build_model(self, weights=None):

        if experimentParams["model"] == "deep":
            model = Sequential(
                [
                    InputLayer(input_shape=(self.maxlen,), dtype="int32"),
                    Embedding(
                        self.max_features, self.embedding_dims, input_length=self.maxlen
                    ),
                    Bidirectional(LSTM(50, return_sequences=True)),
                    GlobalMaxPool1D(),
                    Dropout(0.3),
                    Dense(50, activation="relu"),
                    Dropout(0.3),
                    Dense(2, activation="sigmoid"),
                ]
            )

        elif experimentParams["model"] == "shallow":
            model = Sequential(
                [
                    InputLayer(input_shape=(self.maxlen,), dtype="int32"),
                    Embedding(
                        self.max_features, self.embedding_dims, input_length=self.maxlen
                    ),
                    Bidirectional(LSTM(16, return_sequences=True)),
                    GlobalMaxPool1D(),
                    Dense(2, activation="sigmoid"),
                ]
            )

        model.compile(
            loss="binary_crossentropy",
            optimizer=keras.optimizers.Adam(lr=self.lr),
            metrics=["acc", self.recall],
        )

        if weights is not None:
            model.set_weights(weights)
        return model

    def train(
        self,
        text_path,
        maxlen=400,
        batch_size=32,
        embedding_dims=100,
        epochs=5,
        lr=0.001,
        verbose=1,
    ):
        train_X, train_y = self.text2Dataset.loadTrain(text_path)

        self.max_features = self.text2Dataset.max_features
        self.maxlen = maxlen
        self.text2Dataset.max_len = self.maxlen
        self.batch_size = batch_size
        self.embedding_dims = embedding_dims
        self.epochs = epochs
        self.lr = lr
        self.num_classes = len(set(train_y))

        self.model = self.build_model()

        train_X = sequence.pad_sequences(train_X, maxlen=self.maxlen)
        train_Y = to_categorical(train_y, self.num_classes)

        self.model.fit(
            train_X,
            train_Y,
            batch_size=self.batch_size,
            epochs=self.epochs,
            verbose=verbose,
        )

        return self

    def save_model_bin(self, modelname):
        modelpath = "{0}.bin.gz".format(modelname)

        with gzip.open(modelpath, "wb") as f:
            pickle.dump(
                (
                    self.text2Dataset.wordNgrams,
                    self.text2Dataset.minCount,
                    self.text2Dataset.word2idx,
                    self.text2Dataset.label2idx,
                    self.text2Dataset.token_indice,
                    self.text2Dataset.max_len,
                    self.max_features,
                    self.maxlen,
                    self.batch_size,
                    self.embedding_dims,
                    self.epochs,
                    self.lr,
                    self.num_classes,
                    self.model.get_weights(),
                ),
                f,
            )
        return

    def save_model_json(self, modelname):
        model_json = self.model.to_json()
        with open("{0}.json".format(modelname), "w") as json_file:
            json_file.write(model_json)

        self.model.save_weights("{0}.h5".format(modelname))
        return

    def save_ngram_vectorizer(self, modelname):
        text2Dataset = self.text2Dataset
        text2Dataset = types.FunctionType(module.text2Dataset.__code__,{})
        with open("{0}_wordvec.pkl".format(modelname), "wb") as file:
            pickle.dump(text2Dataset, file)
        return

    def save_model(self, labelname, testResults, exportDir):
        modelFileName = "{0}_{1:3f}".format(labelname, testResults["f1_score"])
        modelPath = os.path.join(exportDir, modelFileName)

        # Save model as a binary file
        self.save_model_bin(modelPath)
        # Save model architecture and weights
        self.save_model_json(modelPath)
        self.save_ngram_vectorizer(modelPath)
        print("Export Complete.")
        return

    def predict(self, text, k=1):
        text = ",".join([words for words in text.split(",")]).strip().replace("\n", "")
        X = self.text2Dataset.words2idx(text)
        X = self.text2Dataset.add_ngram([X])
        X = sequence.pad_sequences(X, maxlen=self.maxlen)
        predict = self.model.predict(X).flatten()
        results = [
            (self.text2Dataset.idx2label[idx], predict[idx])
            for idx in range(len(predict))
        ]
        return sorted(results, key=lambda item: item[1], reverse=True)[:k]

    def calcAccuracyMetrics(self, pred_val, true_val, show_results=True):
        """ Calculates precision, recall and f1 score given arrays of predicted value and true values. """
        modelMetrics = {
            "tp": 0,
            "fp": 0,
            "tn": 0,
            "fn": 0,
            "precision": 0,
            "recall": 0,
            "f1_score": 0,
        }

        try:
            pred_val[pred_val > 0.5] = 1
            pred_val[pred_val <= 0.5] = 0
        except:
            pass

        modelMetrics["tp"] = np.sum(np.logical_and(pred_val == 1, true_val == 1))
        modelMetrics["tn"] = np.sum(np.logical_and(pred_val == 0, true_val == 0))
        modelMetrics["fp"] = np.sum(np.logical_and(pred_val == 1, true_val == 0))
        modelMetrics["fn"] = np.sum(np.logical_and(pred_val == 0, true_val == 1))

        try:
            modelMetrics["precision"] = modelMetrics["tp"] / (
                modelMetrics["tp"] + modelMetrics["fp"]
            )
        except ZeroDivisionError:
            modelMetrics["precision"] = 0

        try:
            modelMetrics["recall"] = modelMetrics["tp"] / (
                modelMetrics["tp"] + modelMetrics["fn"]
            )
        except ZeroDivisionError:
            modelMetrics["recall"] = 0

        try:
            modelMetrics["f1_score"] = 2 * (
                (modelMetrics["precision"] * modelMetrics["recall"])
                / (modelMetrics["precision"] + modelMetrics["recall"])
            )
        except ZeroDivisionError:
            modelMetrics["f1_score"] = 0

        if show_results:
            print("Precision: {0:4f}".format(modelMetrics["precision"]))
            print("Recall: {0:4f}".format(modelMetrics["recall"]))
            print("F1 Score: {0:4f}".format(modelMetrics["f1_score"]))

        return modelMetrics

    def get_accuracy_metrics(self, dataset):
        preds, real = [], []
        preds, real = np.array(preds), np.array(real)
        model = self.model
        for row in dataset.itertuples(index=True, name="Pandas"):
            if getattr(row, "Label") == "__label__0":
                real = np.append(real, 0)
            elif getattr(row, "Label") == "__label__1":
                real = np.append(real, 1)

            if self.predict(getattr(row, "clean_text"))[0][0] == "__label__0":
                preds = np.append(preds, 0)
            elif self.predict(getattr(row, "clean_text"))[0][0] == "__label__1":
                preds = np.append(preds, 1)

        metrics = self.calcAccuracyMetrics(preds, real)
        return metrics

    def evaluate_performance(self, train_set, dev_set, test_set, acceptance_f1_score):

        failedTest = {
            "tp": 0,
            "fp": 0,
            "tn": 0,
            "fn": 0,
            "precision": 0,
            "recall": 0,
            "f1_score": 0,
        }

        trainResults = self.get_accuracy_metrics(train_set)
        devResults = self.get_accuracy_metrics(dev_set)

        if devResults["f1_score"] > acceptance_f1_score:
            testResults = self.get_accuracy_metrics(test_set)
            deployable = True
        else:
            testResults = failedTest
            deployable = False

        return {
            "deployable": deployable,
            "results": {"train": trainResults, "dev": devResults, "test": testResults},
        }

def train_supervised(
    input, lr=0.01, dim=100, epoch=5, minCount=1, wordNgrams=1, verbose=1, maxlen=100
):
    fastText = FastText(wordNgrams=wordNgrams, minCount=minCount)
    fastText.train(
        text_path=input,
        maxlen=maxlen,
        embedding_dims=dim,
        epochs=epoch,
        lr=lr,
        verbose=verbose,
    )
    return fastText


def load_model(path):
    with gzip.open(path, "rb") as f:
        args = pickle.load(f)
    fastText = FastText(args=args)
    return fastText

def load_data_unvectorized(data_file, label_col_name, dev=0.2, test=0.2, neg_frac=1):
    # TODO: Update docstring to reflect actual usage / arguments (e.g. data_file may be
    # file path or may be pandas dataframe)
    """
    Takes csv file path with raw data as an argument, loads the data for the relevant training label,
    splits, the data into train/dev/test sets.
    """
    np.random.seed(0)
    try:
        input_df = pd.read_csv(
            data_file, encoding="utf-8", converters={"clean_text": str}
        )
    except:
        input_df = data_file
    df = input_df.loc[:, ["uuid", "clean_text", label_col_name]].rename(
        columns={label_col_name: "Label"}
    )

    df = df[["clean_text", "Label"]]
    df["Label"] = df["Label"].map({1: "__label__1", 0: "__label__0"})
    # Shuffling the data
    df_pos = df[df["Label"] == "__label__1"].sample(frac=1, random_state=42)
    df_neg = df[df["Label"] == "__label__0"].sample(frac=neg_frac, random_state=42)

    # Calculating train, dev, test set sizes
    m_dev_pos = int(np.floor(df_pos["Label"].count() * dev))
    m_dev_neg = int(np.floor(df_neg["Label"].count() * dev))
    m_test_pos = int(np.floor(df_pos["Label"].count() * test))
    m_test_neg = int(np.floor(df_neg["Label"].count() * test))
    m_train_pos = df_pos["Label"].count() - m_dev_pos - m_test_pos
    m_train_neg = df_neg["Label"].count() - m_dev_neg - m_test_neg

    # Combining proportionate positive and negative labels into train, dev, test splits
    train_set = pd.concat(
        [df_pos.iloc[0:m_train_pos, :], df_neg.iloc[0:m_train_neg, :]]
    )
    dev_set = pd.concat(
        [
            df_pos.iloc[m_train_pos : (m_train_pos + m_dev_pos), :],
            df_neg.iloc[m_train_neg : (m_train_neg + m_dev_neg), :],
        ]
    )
    test_set = pd.concat(
        [
            df_pos.iloc[(m_train_pos + m_dev_pos) :, :],
            df_neg.iloc[(m_train_neg + m_dev_neg) :, :],
        ]
    )

    return train_set, dev_set, test_set, df

