"""

Standard signature policies constants

"""
PKI_BRAZIL_CADES_ADR_BASICA = 'adrb'
PKI_BRAZIL_CADES_ADR_BASICA_WITH_REVOCATION_VALUE = 'adrb-rv'
PKI_BRAZIL_CADES_ADR_TEMPO = 'adrt'
PKI_BRAZIL_CADES_ADR_COMPLETA = 'adrc'
CADES_BES = 'cades'
CADES_BES_WITH_REVOCATION_VALUES = 'cades-rv'
CADES_T = 'cades-t'

PADES_BASIC = 'pades'
PADES_BASIC_WITH_LTV = 'pades-ltv'
PADES_T = 'pades-t'
PKI_BRAZIL_PADES_ADR_BASICA = 'adrb'
PKI_BRAZIL_PADES_ADR_BASICA_WITH_LTV = 'adrb-ltv'
PKI_BRAZIL_PADES_ADR_TEMPO = 'adrt'


NFE_PADRAO_NACIONAL = 'nfe'
XADES_BES = 'xades'
XML_DSIG_BASIC = 'basic'
PKI_BRAZIL_XML_ADR_BASICA = 'adrb'
PKI_BRAZIL_XML_ADR_TEMPO = 'adrt'
COD_WITH_SHA1 = 'cod-sha1'
COD_WITH_SHA256 = 'cod-sh256'


def require_timestamp(policy):
    if not policy:
        return False

    return policy is PKI_BRAZIL_CADES_ADR_TEMPO or \
           policy is PKI_BRAZIL_CADES_ADR_COMPLETA or \
           policy is CADES_T or \
           policy is PADES_T or \
           policy is PKI_BRAZIL_PADES_ADR_TEMPO or \
           policy is PKI_BRAZIL_XML_ADR_TEMPO


__all__ = [
    'PKI_BRAZIL_CADES_ADR_BASICA',
    'PKI_BRAZIL_CADES_ADR_BASICA_WITH_REVOCATION_VALUE',
    'PKI_BRAZIL_CADES_ADR_TEMPO',
    'PKI_BRAZIL_CADES_ADR_COMPLETA',
    'CADES_BES',
    'CADES_BES_WITH_REVOCATION_VALUES',
    'CADES_T',
    'PADES_BASIC',
    'PADES_BASIC_WITH_LTV',
    'PADES_T',
    'PKI_BRAZIL_PADES_ADR_BASICA',
    'PKI_BRAZIL_PADES_ADR_BASICA_WITH_LTV',
    'PKI_BRAZIL_PADES_ADR_TEMPO',
    'NFE_PADRAO_NACIONAL',
    'XADES_BES',
    'XML_DSIG_BASIC',
    'PKI_BRAZIL_XML_ADR_BASICA',
    'PKI_BRAZIL_XML_ADR_TEMPO',
    'COD_WITH_SHA1',
    'COD_WITH_SHA256',
    'require_timestamp'
]
