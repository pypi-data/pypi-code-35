# -*- coding: utf-8 -*-

import argparse
import codecs
import multiprocessing
import pickle
from math import ceil
from random import shuffle

import numpy as np
import termcolor
from scipy.sparse import dok_matrix
from sklearn.model_selection import KFold
from tqdm import tqdm

from ratvec.classifiers import nearest_neighbor_classifier
from ratvec.similarity import n_gram_sim_list
from ratvec.utils import ngrams, normalize_word


def similarity_function_tup(tup):
    a, b = tup
    return similarity_function(a, b)


def distance_function_tup(tup):
    a, b = tup
    return 1 - similarity_function(a, b)


def projectWordTup(tup):
    word = tup[0]
    tuples = tup[1]
    hyperparam = tup[2]
    alphas_lambdas_div = tup[3]
    kernel = tup[4]

    if kernel == "poly":  # Polynomial kernel
        pair_sim = np.array([similarity_function(word, t) for t in tuples])

        k = pair_sim ** hyperparam

    else:  # RBF kernel
        pair_dist = np.array([1 - similarity_function(word, t) for t in tuples])
        k = np.exp(-hyperparam * (pair_dist ** 2))

    return k.dot(alphas_lambdas_div)


def projectWordsGPU(vocab, reprVocab, hyperparam, alphas_lambdas_div, kernel, simMatrix):
    if kernel == "poly":
        k = cm.pow(cm.CUDAMatrix(simMatrix), hyperparam)
    else:
        distMatrix = 1 - simMatrix
        k = cm.exp((cm.pow(cm.CUDAMatrix(distMatrix), 2)).mult(-hyperparam))
    return cm.dot(k, cm.CUDAMatrix(alphas_lambdas_div)).asarray()


def computeSimSplit(split):
    # return [similarity_function(tup[0], tup[1]) for tup in split]
    return n_gram_sim_list(split, int(args.n_ngram))


def computeSimMatrix(reprVocab, vocab):
    if args.sim == "ngram_intersec":
        v_size = len(ngram_dict.keys())

        # R = np.zeros([len(reprVocab), v_size], dtype=int)
        # R = dok_matrix((len(reprVocab), v_size), dtype=np.int8)
        # R is the transposed matrix of the one-hot representations of the representative vocab
        R = dok_matrix((v_size, len(reprVocab)), dtype=int)
        R_ng = np.zeros([len(reprVocab)], dtype=int)
        # for i in np.arange(R.shape[0]):
        for i in np.arange(R.shape[1]):
            ng = ngrams(reprVocab[i], int(args.n_ngram))
            R_ng[i] = len(ng)
            for j in range(len(ng)):
                # R[i,ngram_dict[ng[j]]] = 1
                # Transposed representation
                R[ngram_dict[ng[j]], i] = 1
        R.tocsr()

        # V = np.zeros([len(vocab), v_size], dtype=int)
        V = dok_matrix((len(vocab), v_size), dtype=int)
        V_ng = np.zeros([len(vocab)], dtype=int)
        for i in np.arange(V.shape[0]):
            ng = ngrams(vocab[i], int(args.n_ngram))
            V_ng[i] = len(ng)
            for j in range(len(ng)):
                try:
                    V[i, ngram_dict[ng[j]]] = 1
                except KeyError:
                    pass
        V.tocsr()

        L = np.empty([len(V_ng), len(R_ng)], dtype=int)
        for i in range(len(V_ng)):
            for j in range(len(R_ng)):
                L[i, j] = max(V_ng[i], R_ng[j])

                # return cm.dot(cm.CUDAMatrix(V), cm.CUDAMatrix(R).transpose()).divide(cm.CUDAMatrix(L)).asarray()
        return V.dot(R).toarray() / L
    else:
        split_size = ceil((len(vocab) * len(reprVocab)) / cores)
        termcolor.cprint("Spliting pairs across the cores\n", "blue")
        splits = [[(t1, t2) for t1 in vocab for t2 in reprVocab][i * (split_size): (i + 1) * (split_size)] for i in
                  range(cores)]
        termcolor.cprint("Processing splits\n", "blue")
        # return np.array(pool.map(similarity_function_tup, [ (t1,t2) for t1 in vocab for t2 in reprVocab] )).reshape(len(vocab), len(reprVocab))
        return np.hstack(pool.map(computeSimSplit, splits)).reshape(len(vocab), len(reprVocab))


'''
Parsing user arguments
'''

argParser = argparse.ArgumentParser(description="KPCA embeddings training script",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argParser.add_argument('--repr', type=str,
                       help="Representative words (use a subset of your vocabulary if it is too large for your memory restrictions)",
                       action='store', required=False)
argParser.add_argument('--vocab', type=str, help="Vocabulary path", action='store', required=True)
argParser.add_argument('--sim', type=str,
                       help="Similarity function: 'ngram_sim' (n-gram similarity),'sorensen_plus' (Sørensen–Dice index for n-grams )(default: 'ngram_intersec' )",
                       action='store', required=False, default="ngram_intersec")
argParser.add_argument('--n_ngram', type=str,
                       help="Size of the n-grams when n-gram similarity function is used (default: 2)", action='store',
                       required=False, default=2)
argParser.add_argument('--kernel', type=str, help="Kernel: 'poly','rbf' (default: 'poly' )", action='store',
                       required=False, default="poly")
argParser.add_argument('--hyperparam', type=float,
                       help="Hyperparameter for the selected kernel: sigma for RBF kernel and the degree for the polynomial kernel (default 2)",
                       action='store', required=False, default=2)
argParser.add_argument('--size', type=int, help="Number of principal components of the embeddings (default 1500)",
                       action='store', required=False, default=1500)
argParser.add_argument('--cores', type=int,
                       help="Number of processes to be started for computation (default: number of available cores)",
                       action='store', required=False, default=multiprocessing.cpu_count())
argParser.add_argument('--output', type=str, help="Output folder for the KPCA embeddings (default: current folder)",
                       action='store', required=False, default=".")
argParser.add_argument('--use_gpu', type=bool, help="Output folder for the KPCA embeddings (default: current folder)",
                       action='store', required=False, default=False)
argParser.add_argument('--sim_matrix', type=str,
                       help="'compute' for computing the similarity matrix only, 'infer' for loading a precomputed matrix and infer KPCA embeddings, 'full' for computing all (default 'full') ",
                       action='store', required=False, default='full')
argParser.add_argument('--labels', type=str, help="Labels path for the given vocabulary", action='store', required=True)
args = argParser.parse_args()

n_components = args.size
reprPath = args.repr
vocabPath = args.vocab
kernel = args.kernel
hyperparam = args.hyperparam
cores = args.cores
outputPath = args.output
useGPU = args.use_gpu
simMatrixMode = args.sim_matrix
labelsPath = args.labels


# Similarity function to be used as dot product for KPCA
def similarity_function(a, b):
    if args.sim == "ngram_sim":
        return eval(args.sim)(a, b, int(args.n_ngram))
    else:
        return eval(args.sim)(a, b)


if useGPU:
    import cudamat as cm

    cm.cublas_init()

if reprPath == None:
    reprPath = vocabPath

pool = multiprocessing.Pool(processes=cores)

'''
Preprocessing

'''
with codecs.open(reprPath, "r") as fIn:
    reprVocab = [normalize_word(w[:-1]) for w in fIn if len(w[:-1].split()) == 1]

if args.sim == "ngram_intersec":
    termcolor.cprint("Computing ngram alphabet\n", "blue")
    alphabet = set(reprVocab[0])
    for s in reprVocab:
        alphabet |= set(s)
    alphabet |= {" "}
    aminoacid_dict = {}
    for a in alphabet:
        aminoacid_dict[normalize_word(a)] = len(aminoacid_dict.keys())
    ngram_dict = {}
    for x in alphabet:
        for y in alphabet:
            for z in alphabet:
                if int(args.n_ngram) == 4:
                    for t in alphabet:
                        ngram_dict[x + y + z + t] = len(ngram_dict.keys())
                else:
                    ngram_dict[x + y + z] = len(ngram_dict.keys())

with codecs.open(labelsPath, "r") as f_in:
    # with codecs.open(data_path +"Y_test.txt", "r") as f_in:
    Y = np.array([l[:-1] for l in f_in])

with codecs.open(vocabPath, "r") as fIn:
    vocab = [normalize_word(w[:-1]) for w in fIn if len(w[:-1].split()) == 1]

eval_file = open("plos_evaluation_{}_{}_{}_{}.csv".format(args.sim, args.n_ngram, len(vocab), args.size), "w")
eval_file.write("|".join(["family", "n", "sensitivity", "specificity", "accuracy"]) + '\n')

# kernels = ["poly", "rbf"]
kernels = ["poly"]
hyperparams = {"poly": [17]}

for kernel in kernels:
    for hyperparam in hyperparams[kernel]:

        simMatrix = np.load(outputPath + "/simMatrix_{}_{}_{}.npy".format(args.sim, args.n_ngram, len(reprVocab)),
                            allow_pickle=False)
        # projmatrix = pickle.load( open(outputPath+"/projmatrix_{}_{}_{}_{}_{}.p".format(args.sim, len(reprVocab),kernel, hyperparam, n_components), "rb" ) )
        alphas = pickle.load(open(
            outputPath + "/alphas_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel,
                                                              hyperparam, n_components), "rb"))
        lambdas = pickle.load(open(
            outputPath + "/lambdas_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel,
                                                               hyperparam, n_components), "rb"))

        X_train = pickle.load(open(
            outputPath + "/KPCA_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel, hyperparam,
                                                            n_components), "rb"))

        termcolor.cprint("10-fold cross-validation\n", "blue")
        X = X_train
        k = 1
        # clf = neighbors.KNeighborsClassifier(n_neighbors=k)
        clf = nearest_neighbor_classifier()
        scoreDict = {}
        scores = []
        weights = []
        kf = KFold(n_splits=10)
        for fam in tqdm(set(Y), desc="Computing protein families"):
            n = len(np.where(Y == fam)[0])
            if n >= 10:
                idx_pos = np.where(Y == fam)
                X_pos = X[idx_pos]
                idx_neg = np.where(Y != fam)
                X_neg = X[idx_neg][:n]
                X_fam = np.concatenate((X_pos, X_neg), axis=0)
                Y_fam = np.array(n * [True] + n * [False])
                idx = np.array(range(2 * n))
                shuffle(idx)

                split_scores = []
                for train, test in kf.split(idx):
                    # idx_train= idx[:int(0.9*n)]
                    # idx_test= idx[int(0.9*n):]
                    idx_train = idx[train]
                    idx_test = idx[test]
                    Y_train = Y_fam[idx_train]
                    Y_test = Y_fam[idx_test]
                    X_train = X_fam[idx_train]
                    X_test = X_fam[idx_test]
                    # print("{}: {}".format(fam,clf.fit(X_train, Y_train).score(X_test, Y_test)))
                    Y_pred = clf.fit(X_train, Y_train).predict(X_test)
                    idx_pos = np.where(Y_test)
                    idx_neg = np.where(Y_test == False)
                    if (len(idx_pos[0]) == 0 or len(idx_neg[0]) == 0):
                        print("{} skipped".format(fam))
                        continue
                    sensitivity = len(np.where(clf.predict(X_test[idx_pos]))[0]) / len(idx_pos[0])

                    specificity = len(np.where(clf.predict(X_test[idx_neg]) == False)[0]) / len(idx_neg[0])
                    accuracy = len(np.where(clf.predict(X_test) == Y_test)[0]) / len(Y_test)
                    split_scores.append([sensitivity, specificity, accuracy])
                # print("{}|{}|{}|{}".format(fam,sensitivity, specificity, accuracy))
                if len(split_scores) == 0:
                    continue
                    # scores.append(([np.mean(np.array(split_scores)[:,i]) for i in range(3)]))
                scoreDict[fam] = {}
                scoreDict[fam]["scores"] = ([np.mean(np.array(split_scores)[:, i]) for i in range(3)])

                # weights.append(n)
                scoreDict[fam]["weight"] = n
                eval_file.write("|".join(
                    [fam, str(n), str(scoreDict[fam]["scores"][0]), str(scoreDict[fam]["scores"][1]),
                     str(scoreDict[fam]["scores"][2])]) + '\n')
                eval_file.flush()

        # scores = np.array(scores)
        # sensitivity = np.dot(scores[:,0], weights) / np.sum(weights)
        # specificity = np.dot(scores[:,1], weights) / np.sum(weights)
        # accuracy = np.dot(scores[:,2], weights) / np.sum(weights)
        # eval_file.write("|".join([kernel, str(hyperparam), str(sensitivity), str(specificity), str(accuracy)])+'\n')
        # eval_file.flush()
        pickle.dump(scoreDict, open(
            outputPath + "/scores_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel,
                                                              hyperparam, n_components), "wb"))
eval_file.close()
