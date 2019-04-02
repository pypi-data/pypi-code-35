# -*- coding: utf-8 -*-
"""
Handy functions used in LTRI Machine Learning Lab

@author: Khashayar Namdar  knamdar@uwo.ca
"""
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
import csv
import numpy as np
import sys


def get_fname():
    """
    get_fname opens up a GUI. The user selects a file and the whole path and
    filename is returned

    Local Variables:
        fname: a string containing path+name+extension of the selected file
    """
    root = Tk()
    root.withdraw()
    print("initializing Dialogue...\nPlease select a file")
    fname = askopenfilename(initialdir=os.getcwd(),
                            title="Please select a file")
    root.destroy()
    if len(fname) > 0:
        print("The selected file is:\n%s" % fname)
        return fname
    else:
        fname = None
        print("\nNo file was selected \nNone is returned \n ")
        return fname


def get_dirname():
    """
    get_dirname function adopted from:
    https://www.programcreek.com/python/example/16883/tkFileDialog.askdirectory

    get_dirname opens up a GUI. The user selects a folder and the whole path
    is returned

    Local Variables:
        dirname: a string containing path of the selected directory
    """
    root = Tk()
    root.withdraw()
    print("initializing Dialogue...\nPlease select a direcory.")
    dirname = askdirectory(initialdir=os.getcwd(),
                           title="please select a directory")
    root.destroy()
    if len(dirname) > 0:
        print("The selected directory is:\n%s" % dirname)
        return dirname
    else:
        dirname = os.getcwd()
        print("\nNo directory selected \ninitializing with %s \n "
              % os.getcwd())
        return dirname


def find_in_excel_column_labels(excel, label):
    print()
    for i in range(excel.ncols):
        if excel.cell(0, i).value == label:
            return i
            break


def dcm_file_list(path):
    file_list = []
    """
    The next for loop lists all .dcm files together with their path in
    file_list.
    ex: Z:/shared/Liver/test.SeparatedDCE_Phases\\A016\\22157\1.3.6.1.....dcm
    """
    for subdir, dirs, files in os.walk(path):
        if files:
            for file in files:
                if ".dcm" in file.lower():
                    file_list.append(os.path.join(subdir, file))
    return file_list


def list_of_dict_to_csv(data, filename):
    max_dic_len = max(len(data[i]) for i in range(len(data)))
    for i in range(len(data)):
        if len(data[i]) == max_dic_len:
            keys = data[i].keys()
            break
    with open(filename, 'w', newline='') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(data)


def pca(X=np.array([]), no_dims=50):
    """
        Runs PCA on the NxD array X in order to reduce its dimensionality to
        no_dims dimensions.
    """

    print("Preprocessing the data using PCA...")
    (n, d) = X.shape
    X = X - np.tile(np.mean(X, 0), (n, 1))
    (l, M) = np.linalg.eig(np.dot(X.T, X))
    Y = np.dot(X, M[:, 0:no_dims])
    return Y


def Hbeta(D=np.array([]), beta=1.0):
    """
        Compute the perplexity and the P-row for a specific value of the
        precision of a Gaussian distribution.
    """

    # Compute P-row and corresponding perplexity
    P = np.exp(-D.copy() * beta)
    sumP = sum(P)+np.finfo(np.double).eps
    H = np.log(sumP) + beta * np.sum(D * P) / sumP
    P = P / sumP
    return H, P


def x2p(X=np.array([]), tol=1e-5, perplexity=30.0):
    """
        Performs a binary search to get P-values in such a way that each
        conditional Gaussian has the same perplexity.
    """

    # Initialize some variables
    print("Computing pairwise distances...")
    (n, d) = X.shape
    sum_X = np.sum(np.square(X), 1)
    D = np.add(np.add(-2 * np.dot(X, X.T), sum_X).T, sum_X)
    P = np.zeros((n, n))
    beta = np.ones((n, 1))
    logU = np.log(perplexity)

    # Loop over all datapoints
    for i in range(n):

        # Print progress
        if i % 500 == 0:
            print("Computing P-values for point %d of %d..." % (i, n))

        # Compute the Gaussian kernel and entropy for the current precision
        betamin = -np.inf
        betamax = np.inf
        Di = D[i, np.concatenate((np.r_[0:i], np.r_[i+1:n]))]
        (H, thisP) = Hbeta(Di, beta[i])

        # Evaluate whether the perplexity is within tolerance
        Hdiff = H - logU
        tries = 0
        while np.abs(Hdiff) > tol and tries < 50:

            # If not, increase or decrease precision
            if Hdiff > 0:
                betamin = beta[i].copy()
                if betamax == np.inf or betamax == -np.inf:
                    beta[i] = beta[i] * 2.
                else:
                    beta[i] = (beta[i] + betamax) / 2.
            else:
                betamax = beta[i].copy()
                if betamin == np.inf or betamin == -np.inf:
                    beta[i] = beta[i] / 2.
                else:
                    beta[i] = (beta[i] + betamin) / 2.

            # Recompute the values
            (H, thisP) = Hbeta(Di, beta[i])
            Hdiff = H - logU
            tries += 1

        # Set the final row of P
        P[i, np.concatenate((np.r_[0:i], np.r_[i+1:n]))] = thisP

    # Return final P-matrix
    print("Mean value of sigma: %f" % np.mean(np.sqrt(1 / beta)))
    return P


def tsne(X=np.array([]), no_dims=2, initial_dims=50, perplexity=30.0,
         seeding='n'):
    """
        Runs t-SNE on the dataset in the NxD array X to reduce its
        dimensionality to no_dims dimensions. The syntaxis of the function is
        `Y = tsne.tsne(X, no_dims, perplexity), where X is an NxD NumPy array.
    """

    # Check inputs
    if isinstance(no_dims, float):
        print("Error: array X should have type float.")
        return -1
    if round(no_dims) != no_dims:
        print("Error: number of dimensions should be an integer.")
        return -1

    # Initialize variables
    X = pca(X, initial_dims).real
    (n, d) = X.shape
    max_iter = 1000
    initial_momentum = 0.5
    final_momentum = 0.8
    eta = 500
    min_gain = 0.01
    if seeding == 'n':
        Y = np.random.randn(n, no_dims)
    elif seeding == 'y':
        np.random.seed(0)
        Y = np.random.randn(n, no_dims)
    else:
        print("Not a valid seedind flag. Run the code again.")
        sys.exit(0)
    dY = np.zeros((n, no_dims))
    iY = np.zeros((n, no_dims))
    gains = np.ones((n, no_dims))

    # Compute P-values
    P = x2p(X, 1e-5, perplexity)
    P = P + np.transpose(P)
    P = P / np.sum(P)
    P = P * 4.									# early exaggeration
    P = np.maximum(P, 1e-12)

    # Run iterations
    for iter in range(max_iter):

        # Compute pairwise affinities
        sum_Y = np.sum(np.square(Y), 1)
        num = -2. * np.dot(Y, Y.T)
        num = 1. / (1. + np.add(np.add(num, sum_Y).T, sum_Y))
        num[range(n), range(n)] = 0.
        Q = num / np.sum(num)
        Q = np.maximum(Q, 1e-12)

        # Compute gradient
        PQ = P - Q
        for i in range(n):
            dY[i, :] = np.sum(np.tile(
                    PQ[:, i] * num[:, i], (no_dims, 1)).T * (Y[i, :] - Y), 0)

        # Perform the update
        if iter < 20:
            momentum = initial_momentum
        else:
            momentum = final_momentum
        gains = (gains + 0.2) * ((dY > 0.) != (iY > 0.)) + \
                (gains * 0.8) * ((dY > 0.) == (iY > 0.))
        gains[gains < min_gain] = min_gain
        iY = momentum * iY - eta * (gains * dY)
        Y = Y + iY
        Y = Y - np.tile(np.mean(Y, 0), (n, 1))

        # Compute current value of cost function
        if (iter + 1) % 10 == 0:
            C = np.sum(P * np.log(P / Q))
            print("Iteration %d: error is %f" % (iter + 1, C))

        # Stop lying about P-values
        if iter == 100:
            P = P / 4.

    # Return solution
    return Y


name = "LTRI_Funcs"
