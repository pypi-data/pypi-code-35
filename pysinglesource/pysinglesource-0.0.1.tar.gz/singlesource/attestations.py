# -*- coding: utf-8 -*-
"""Attestation support."""

# Created: 2019-03-28 Guy K. Kloss <guy@mysinglesource.io>
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

from typing import Iterable

from pykauriid.attestations import (AttesterData,
                                    AttestationData,
                                    Attestation)
from pykauriid.claims import (ClaimSet,
                              ClaimSetKeys)
from sspyjose.jwe import Jwe
from sspyjose.jwk import Jwk


def make_foreign_claim_set(claims: Iterable[dict],
                           subject: str) -> ClaimSetKeys:
    """
    Create a new foreign claim set on the provided claims.

    :param claims: Iterable containing JSON-LD styled claims.
    :param subject: DID of the subject of the claims.
    :return: Claim set keys object containing the foreign claim set.
    """
    claim_set = ClaimSet(sub=subject)
    claims_keys = ClaimSetKeys()
    claims_keys.claim_set = claim_set
    for claim in claims:
        claims_keys.add_claim(claim)
    claims_keys.finalise_claim_set(include_commitment=False)
    return claims_keys


def attest_claim_set(claim_set_keys: ClaimSetKeys,
                     attester_data: AttesterData,
                     attestation_data: AttestationData,
                     attester_sig_key: Jwk) -> (str, dict):
    """
    Attest a (self or foreign) claim set.

    :param claim_set_keys: File to write the claim set keys to.
    :param attester_data: File containing information on the attester.
    :param attestation_data: File containing data on the specific
        attestation to make.
    :param attester_sig_key: Key to use to attest (private).
    :return: Serialised attestation object and updated claim set keys dict.
    """
    my_attestation = Attestation(claim_set_keys=claim_set_keys,
                                 attester_signing_key=attester_sig_key)
    # Add attester data.
    my_attestation.attester_data = attester_data
    my_attestation.attestation_data = attestation_data
    # Attest the claim set.
    serialised_attestation = my_attestation.finalise(attester_sig_key)
    # Return attestation with updated key data (containing trace key).
    return {
        'id': my_attestation.id,
        'attestation': serialised_attestation,
        'claim_set_keys': my_attestation.claim_set_keys.to_dict(
            claim_type_hints=True)
    }


def encrypt_to(data: dict, recipient_pub_key: Jwk) -> str:
    """
    Encrypt dqta to a recipient.

    :param data: Payload data.
    :param recipient_pub_key: Public encryption key of the recipient (X25519).
    :return: JWE encrypted, string serialised cipher text.
    """
    encrypter = Jwe.get_instance(jwk=recipient_pub_key)
    encrypter.message = data
    encrypter.encrypt()
    return encrypter.serialise()
