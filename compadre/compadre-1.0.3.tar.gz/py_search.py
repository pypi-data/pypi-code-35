import numpy as np
import scipy.spatial.kdtree as kdtree
import GMLS_Module


def get_neighborlist(source_sites, target_sites, polyOrder, dimensions):
    print GMLS_Module
    # neighbor search
    my_kdtree = kdtree.KDTree(source_sites, leafsize=10)
    neighbor_number_multiplier = (1 + polyOrder)
    neighbor_lists = []
    epsilons = []
    for target_num in range(target_sites.shape[0]):
        np_needed = GMLS_Module.getNP(polyOrder, dimensions);
        try:
            query_result = my_kdtree.query(target_sites[target_num], k=int(neighbor_number_multiplier*np_needed), eps=0)
        except:
            print "Search failed for %d"%target_num
        neighbor_lists.append([query_result[1].size,] + list(query_result[1]))
        epsilons.append(query_result[0][-1])
    neighbor_lists = np.array(neighbor_lists, dtype=np.dtype(int))
    epsilons = np.array(epsilons, dtype=np.dtype('d'))
    d = dict();
    d['neighbor_lists'] = neighbor_lists
    d['epsilons'] = epsilons
    return d