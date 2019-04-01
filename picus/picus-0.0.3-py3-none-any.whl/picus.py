#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from picus import __version__
from picus.core.variantclassification import VariantClassification
from picus.core.evidencecollection import EvidenceCollection
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser()

    # Not functional
    parser.add_argument('-v', '--verbose', required=False, action='store_true',
                        help='WIP.Write what is happening to stdout.')

    parser.add_argument('--version',
                        action='version', version=__version__)

    parser.add_argument('-i', '--input', required=True,
                        default=None, type=str, help='input annotation file.')

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    input_file = args.input

    df = pd.read_csv(input_file, low_memory=False)
    evidence_collector = EvidenceCollection()
    variant_classifier = VariantClassification()

    variants = evidence_collector.collect_evidences(df)

    for variant in variants:
        variant['significance'] = variant_classifier.classify_variant(variant['evidences'])
        print(variant)


if __name__ == '__main__':
    main()
