# -*- coding: utf-8 -*-

"""KPCA embeddings module."""

import argparse
import codecs
import multiprocessing
import pickle
from math import ceil
from typing import Tuple

import numpy as np
import termcolor
from scipy.linalg import eigh

from ratvec.similarity import n_gram_sim_list
from ratvec.utils import ngrams, normalize_word


def similarity_function_tup(tup: Tuple):
    """Similarity function tuple."""
    a, b = tup
    return similarity_function(a, b)


def distance_function_tup(tup: Tuple):
    """Distance function tuple."""
    a, b = tup
    return 1 - similarity_function(a, b)


def project_word_tuple(tup: Tuple):
    """Project word tuple."""
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


def project_words_gpu(vocab, reprVocab, hyperparam, alphas_lambdas_div, kernel, simMatrix):
    """Project words to GPU."""
    if kernel == "poly":
        k = cm.pow(cm.CUDAMatrix(simMatrix), hyperparam)
    else:
        distMatrix = 1 - simMatrix
        k = cm.exp(-hyperparam * (cm.pow(cm.CUDAMatrix(distMatrix), 2)))
    return cm.dot(k, cm.CUDAMatrix(alphas_lambdas_div)).asarray()


def compute_similarity_split(split):
    # return [similarity_function(tup[0], tup[1]) for tup in split]
    return n_gram_sim_list(split, int(args.n_ngram))


def compute_similarity_matrix(reprVocab, vocab):
    if args.sim == "trigram_intersec":
        v_size = len(trigram_dict.keys())

        R = np.zeros([len(reprVocab), v_size], dtype=int)
        for i in np.arange(R.shape[0]):
            for t in ngrams(reprVocab[i], 3):
                R[i, trigram_dict[t]] = 1

        V = np.zeros([len(vocab), v_size], dtype=int)
        for i in np.arange(V.shape[0]):
            for t in ngrams(vocab[i], 3):
                try:
                    V[i, trigram_dict[t]] = 1
                except KeyError:
                    pass

        return cm.dot(cm.CUDAMatrix(V), cm.CUDAMatrix(R).transpose()).asarray()
    else:
        split_size = ceil((len(vocab) * len(reprVocab)) / cores)
        termcolor.cprint("Spliting pairs across the cores\n", "blue")
        splits = [[(t1, t2) for t1 in vocab for t2 in reprVocab][i * (split_size): (i + 1) * (split_size)] for i in
                  range(cores)]
        termcolor.cprint("Processing splits\n", "blue")
        # return np.array(pool.map(similarity_function_tup, [ (t1,t2) for t1 in vocab for t2 in reprVocab] )).reshape(len(vocab), len(reprVocab))
        return np.hstack(pool.map(compute_similarity_split, splits)).reshape(len(vocab), len(reprVocab))


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
                       help="Similarity function: 'ngram_sim' (n-gram similarity),'sorensen_plus' (Sørensen–Dice index for n-grams )(default: 'ngram_sim' )",
                       action='store', required=False, default="ngram_sim")
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

if args.sim == "trigram_intersec":
    termcolor.cprint("Computing trigram alphabet\n", "blue")
    alphabet = set(reprVocab[0])
    for s in reprVocab:
        alphabet |= set(s)
    alphabet |= {" "}
    aminoacid_dict = {}
    for a in alphabet:
        aminoacid_dict[normalize_word(a)] = len(aminoacid_dict.keys())
    trigram_dict = {}
    for x in alphabet:
        for y in alphabet:
            for z in alphabet:
                trigram_dict[x + y + z] = len(trigram_dict.keys())

'''
Similarity matrix computation: the similarity of all word pairs from the representative words is computed
'''
if simMatrixMode != "infer":

    termcolor.cprint("Computing similarity matrix for representatives\n", "blue")

    simMatrix = compute_similarity_matrix(reprVocab, reprVocab)

    '''
    Kernel Principal Component Analysis
    '''
    termcolor.cprint("Solving eigevector/eigenvalues problem\n", "blue")

    if kernel == "rbf":
        distMatrix = np.ones(len(simMatrix)) - simMatrix
        K = np.exp(-hyperparam * (distMatrix ** 2))
    else:  # poly
        K = simMatrix ** hyperparam

    # Centering the symmetric NxN kernel matrix.
    N = K.shape[0]
    one_n = np.ones((N, N)) / N
    K_norm = K - one_n.dot(K) - K.dot(one_n) + one_n.dot(K).dot(one_n)
    # Obtaining eigenvalues in descending order with corresponding eigenvectors from the symmetric matrix.    

    eigvals, eigvecs = eigh(K_norm)

    alphas = np.column_stack((eigvecs[:, -i] for i in range(1, n_components + 1)))
    lambdas = [eigvals[-i] for i in range(1, n_components + 1)]

    # alphas_lambdas_div = alphas / lambdas
    # TODO: investigate effect of not using the lambdas
    # projmatrix = alphas
    pickle.dump(alphas, open(
        outputPath + "/alphas_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel, hyperparam,
                                                          n_components), "wb"))
    pickle.dump(lambdas, open(
        outputPath + "/lambdas_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel, hyperparam,
                                                           n_components), "wb"))

with codecs.open(vocabPath, "r") as fIn:
    vocab = [normalize_word(w[:-1]) for w in fIn if len(w[:-1].split()) == 1]

if simMatrixMode == "infer":
    simMatrix = pickle.load(open(
        outputPath + "/simMatrix_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel, hyperparam),
        "rb"))
    # projmatrix = pickle.load( open(outputPath+"/projmatrix_{}_{}_{}_{}_{}.p".format(args.sim, len(reprVocab),kernel, hyperparam, n_components), "rb" ) )
    alphas = pickle.load(open(
        outputPath + "/alphas_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel, hyperparam,
                                                          n_components), "rb"))
    lambdas = pickle.load(open(
        outputPath + "/lambdas_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel, hyperparam,
                                                           n_components), "rb"))
else:
    termcolor.cprint("Computing similarity matrix for full vocabulary\n", "blue")
    simMatrix = compute_similarity_matrix(reprVocab, vocab)
    if simMatrixMode == "compute":
        pickle.dump(simMatrix, open(
            outputPath + "/simMatrix_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel,
                                                              hyperparam), "wb"))
        exit()

termcolor.cprint("Projecting known vocabulary to KPCA embeddings\n", "blue")

'''
Projection to KPCA embeddings of the vocabulary
'''
projmatrix = alphas / lambdas
if useGPU:
    X_train = project_words_gpu(vocab, reprVocab, hyperparam, projmatrix, kernel, simMatrix)
    cm.shutdown()
else:
    X_train = pool.map(project_word_tuple, [(word, reprVocab, hyperparam, projmatrix, kernel) for word in vocab])

pickle.dump(X_train, open(
    outputPath + "/KPCA_{}_{}_{}_{}_{}_{}.p".format(args.sim, args.n_ngram, len(reprVocab), kernel, hyperparam,
                                                    n_components), "wb"))
