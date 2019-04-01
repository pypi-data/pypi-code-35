# -*- coding: utf-8 -*-

"""Compute statistics of a KG to be able to interpret the performance of KGE models."""

import operator
from collections import Counter, OrderedDict

import numpy as np


def get_sorted_dict_from_counter(counter):
    """Return sorted dict for Counter object."""
    temp_dict = OrderedDict()

    for key, value in counter.items():
        temp_dict[' '.join(key)] = value

    sorted_x = sorted(temp_dict.items(), key=operator.itemgetter(1))
    sorted_x = OrderedDict(sorted_x)

    return sorted_x


def compute_number_objects_per_subject_relation_tuples(triples):
    """Compute number of objects subject-relation pairs."""
    subjects = triples[:, 0:1]
    relations = triples[:, 1:2]
    subjs_rels = np.concatenate([subjects, relations], axis=-1).tolist()
    temp_tuple = map(tuple, subjs_rels)
    stats = Counter(temp_tuple)

    stats = get_sorted_dict_from_counter(stats)

    return stats


def compute_number_subjects_per_object_relation_tuples(triples):
    """Compute number of subjects per relation-object pairs."""
    objects = triples[:, 2:3]
    relations = triples[:, 1:2]
    objs_rels = np.concatenate([relations, objects], axis=-1).tolist()
    temp_tuple = map(tuple, objs_rels)
    stats = Counter(temp_tuple)

    stats = get_sorted_dict_from_counter(stats)

    return stats

if __name__ == '__main__':

    path = '/Users/mehdi/PycharmProjects/BioKEEN/data/hsdn.keen.tsv'
    triples = np.reshape(np.loadtxt(
        fname=path,
        dtype=str,
        comments='@Comment@ Subject Predicate Object',
        delimiter='\t',
    ), newshape=(-1, 3))

    stats = compute_number_objects_per_subject_relation_tuples(triples)

    import os,json

    output_directory = '/Users/mehdi/PycharmProjects/BioKEEN/data/out'
    with open(os.path.join(output_directory, 'stats_hsdn_objects_per_subject_rels_tuples'), 'w') as file:
        # In HPO model inital configuration is different from final configurations, thats why we differentiate
        json.dump(stats, file, indent=2)

    stats = compute_number_subjects_per_object_relation_tuples(triples)

    output_directory = '/Users/mehdi/PycharmProjects/BioKEEN/data/out'
    with open(os.path.join(output_directory, 'stats_hsdn_subject_per_rel_object_tuples'), 'w') as file:
        # In HPO model inital configuration is different from final configurations, thats why we differentiate
        json.dump(stats, file, indent=2)