#! /usr/bin/env python

import numpy as np
import itertools

def heaviside(x):
    return 0.5 * (np.sign(x) + 1)

def norm(x):
    normed = (x-min(x))/(max(x)-min(x))
    return normed

def filter2D(fx, gx, target):
    fx0 = fx[target==0]
    fx1 = fx[target==1]
    gx0 = gx[target==0]
    gx1 = gx[target==1]
    return np.asarray(fx0), np.asarray(fx1), np.asarray(gx0), np.asarray(gx1)


def calc_ADO(fx, gx, target, n_data):
    # normalize input data
    fx = norm(fx)
    gx = norm(gx)

    min_length = min(len(fx), len(gx))

    # Data is shuffled to select a random subset of the input
    data = np.vstack((fx[0:min_length], gx[0:min_length], target[0:min_length])).T
    np.random.seed(123)
    np.random.shuffle(data)

    # Reduce dataset to n_data size
    data = data[0:n_data]

    # Filter data into signal and background
    fx0, fx1, gx0, gx1 = filter2D(data[:,0], data[:,1], data[:,2])

    hside = heaviside(np.multiply([(x-y) for x in fx0 for y in fx1 ],[(x-y) for x in gx0 for y in gx1 ]))

    heavisum = np.abs(((1.0/len(hside)) * np.sum(hside)))
    if heavisum < 0.5:
        heavisum = 1- heavisum
    else:
        pass

    return heavisum

def calc_ADO_itertools(fx, gx, target, n_data):
    # This is an alternate way of calculating the ADO. But testing has shown that it's about half as fast as the numpy approach
    # normalize input data
    fx = norm(fx)
    gx = norm(gx)

    min_length = min(len(fx), len(gx))

    # Data is shuffled to select a random subset of the input
    data = np.vstack((fx[0:min_length], gx[0:min_length], target[0:min_length])).T
    np.random.seed(123)
    np.random.shuffle(data)

    # Reduce dataset to n_data size
    data = data[0:n_data]

    # Filter data into signal and background
    fx0, fx1, gx0, gx1 = filter2D(data[:,0], data[:,1], data[:,2])

    hside = heaviside(np.multiply([(x-y) for x in fx0 for y in fx1 ],[(x-y) for x in gx0 for y in gx1 ]))

    heavisum = np.abs(((1.0/len(hside)) * np.sum(hside)))
    if heavisum < 0.5:
        heavisum = 1- heavisum
    else:
        pass

    return heavisum

def boot_strap(fx, gx, target, n_data, boot_loops):
    n_bootstraps = boot_loops
    rng_seed = 42
    bootstrapped_scores = []
    rng = np.random.RandomState(rng_seed)
    for i in range(n_bootstraps):
        indices = rng.random_integers(0, n_data - 1, n_data)
        score = calc_ADO(fx[indices], gx[indices], target[indices], len(fx[indices]))
        bootstrapped_scores.append(score)
        sorted_scores = np.array(bootstrapped_scores)
        sorted_scores.sort()
        confidence_lower = sorted_scores[int(0.025 * len(sorted_scores))]
        confidence_upper = sorted_scores[int(0.975 * len(sorted_scores))]
    ADO_mean = np.mean(bootstrapped_scores)
    ADO_var = np.std(bootstrapped_scores)
    return ADO_mean, ADO_var


''' Main ADO function '''
def ADO(fx, gx, target, n_data=None, stats=False, boot_loops=100):
    if n_data == None:
        n_data = min(len(fx), len(gx))
    if stats==True:
        return boot_strap(fx, gx, target, n_data, boot_loops)
    else:
        return calc_ADO(fx, gx, target, n_data)

