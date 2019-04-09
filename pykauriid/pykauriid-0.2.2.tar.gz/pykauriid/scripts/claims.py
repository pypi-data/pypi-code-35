# -*- coding: utf-8 -*-
"""
Module providing an entry point to make and read claims via a CLI.
"""

# Created: 2018-08-23 Guy K. Kloss <guy@mysinglesource.io>
#
# (c) 2018-2019 by SingleSource Limited, Auckland, New Zealand
#     http://mysinglesource.io/
#     Apache 2.0 Licence.
#
# This work is licensed under the Apache 2.0 open source licence.
# Terms and conditions apply.
#
# You should have received a copy of the licence along with this
# program.

__author__ = 'Guy K. Kloss <guy@mysinglesource.io>'

import argparse
import io
import json
import logging

from sspyjose.jwk import Jwk

from pykauriid import claims


logger = logging.getLogger(__name__)


def new_claim_set(claims_fd: io.TextIOBase,
                  claimset_file: str,
                  claimsetkeys_file: str,
                  subject: str,
                  sig_key_fd: io.TextIOBase):
    """
    Create a new claim set on the provided claims.

    :param claims_fd: File for the claims.
    :param claimset_file: File to write the claim set to.
    :param claimsetkeys_file: File to write the claim set keys to.
    :param subject: DID of the claim set subject.
    :param sig_key_fd: Key to use for signing (private). If not present,
        the claim set won't contain a commitment (foreign claim set).
    """
    plain_claims = json.load(claims_fd)
    signing_key = (Jwk.get_instance(from_json=sig_key_fd.read())
                   if sig_key_fd else None)
    if signing_key and not signing_key.d:
        raise ValueError('Signing key does not contain a private key.')
    claim_set = claims.ClaimSet(sub=subject, signing_key=signing_key)
    claims_keys = claims.ClaimSetKeys()
    claims_keys.claim_set = claim_set
    for claim in plain_claims:
        claims_keys.add_claim(claim)
    serialised_claim_set = claims_keys.finalise_claim_set(
        include_commitment=(signing_key is not None))
    serialised_claim_set_keys = claims_keys.serialise(claim_type_hints=True)
    with open(claimset_file, 'wt') as fd:
        fd.write(serialised_claim_set)
    with open(claimsetkeys_file, 'wt') as fd:
        fd.write(serialised_claim_set_keys)
    print('Claim set created with the following claim types:')
    for item in claims_keys.claim_type_hints:
        print('- {}'.format(item))


def access_claim_set(claimsetkeys_file: str,
                     sig_key_fd: io.TextIOBase,
                     index: int,
                     to_list: bool):
    """
    Access a claim set in a file using the given claim set keys.

    :param claimsetkeys_file: File to read the claim set keys from.
    :param sig_key_fd: Key to use for signature verification (public). If not
        present, only foreign claim sets can be accessed.
    :param index: Index of the claim to access (-1 for all).
    :param to_list: List the claim types of a claim set.
    """
    signing_key = (Jwk.get_instance(from_json=sig_key_fd.read())
                   if sig_key_fd else None)
    with open(claimsetkeys_file, 'r') as fd:
        claims_keys = claims.ClaimSetKeys(data=fd.read(),
                                          signing_key=signing_key)
    claim_set = claims_keys.claim_set
    if to_list:
        print('Claim set contains claims with the following types:')
        for item in claims_keys.claim_type_hints:
            print('- {}'.format(item))
    elif index == -1:
        print('All claims:')
        for i in range(len(claim_set.claims)):
            claim_key = claims_keys.claim_keys[i]
            print('- {}'.format(json.dumps(
                claim_set.access_claim(i, claim_key), indent=2)))
    else:
        claim_key = claims_keys.claim_keys[index]
        print('Claim index {}:'.format(index))
        print(json.dumps(claim_set.access_claim(index, claim_key), indent=2))


def main(args: argparse.Namespace):
    """
    Delegate to the right functions from given (command line) arguments.

    :param args: Command line arguments provided:

        - args.operation - type: str
        - args.subject - type: str
        - args.subject_sig_key - type: io.TextIOBase
        - args.claims - type: io.TextIOBase
        - args.claimset - type: str
        - args.claimsetkeys - type: str
        - args.index - type: int
        - args.list - type: bool
    """
    if args.operation == 'new':
        new_claim_set(args.claims, args.claimset, args.claimsetkeys,
                      args.subject, args.subject_sig_key)
    elif args.operation == 'access':
        access_claim_set(args.claimsetkeys, args.subject_sig_key, args.index,
                         args.list)
    else:
        raise ValueError('Unsupported operation "{}" for claims.'
                         .format(args.operation))

    logger.info('Operation "{}" finished.'.format(args.operation))
