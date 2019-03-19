import math
from random import random

import numpy as np


def visualize(alloc, num_sockets):
    d = len(alloc[0])
    n = num_sockets
    b = d // n

    for t in range(n):
        S1 = [' '] * (b // 2)
        S2 = [' '] * (b // 2)
        for job_id, job in enumerate(alloc):
            for i in range(t * b, (t + 1) * b):
                if job[i] == 1:
                    if (i - b) % 2 == 0:
                        S1[(i - b) // 2] = str(job_id + 1)
                    else:
                        S2[(i - b) // 2] = str(job_id + 1)
        print('| ' + ' | '.join(S1) + ' |')
        print('| ' + ' | '.join(S2) + ' |')
        if (t < n - 1):
            print('| ' + '-' * len(' | '.join(S1)) + ' |')


def draw_workloads(num_workloads, avg_per_workload, std_per_workload, max_budget, fill_up_ratio=1.0):
    k_gamma = float(avg_per_workload * avg_per_workload) / std_per_workload
    theta_gamma = float(std_per_workload) / avg_per_workload
    draws = []
    while sum(draws) < fill_up_ratio * max_budget and len(draws) < num_workloads:
        probe = max(np.round(np.random.gamma(k_gamma, theta_gamma, 1)).astype(np.int32)[0], 1)
        curr_sum = sum(draws)
        if probe + curr_sum > fill_up_ratio * max_budget:
            draws.append(math.floor(fill_up_ratio * max_budget - curr_sum))
            break
        else:
            draws.append(probe)
    return draws


def draw_workloads_empirical(num_workloads, max_budget, with_remainder=True):
    # Empirical distribution of logical CPUs requested over a week
    # as of Nov '18:
    reqs = [1, 2, 4, 5, 8, 16, 32, 64]
    cdf = [0.268, 0.416, 0.895, 0.897, 0.989, 0.993, 0.998, 1.]
    # cdf = np.cumsum([0.268, 0.148, 0.479, 0.002, 0.092, 0.004, 0.005, 0.002])
    draws = []
    while sum(draws) < max_budget and len(draws) < num_workloads:
        v = random()
        ind = 0
        while v > cdf[ind]:
            ind += 1
        ind = min(ind, len(cdf) - 1)
        probe = reqs[ind]
        curr_sum = sum(draws)
        if probe + curr_sum > max_budget:
            if with_remainder:
                draws.append(math.floor(max_budget - curr_sum))
            break
        else:
            draws.append(probe)
    return draws
