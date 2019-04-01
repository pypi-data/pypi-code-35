"""

Module containing the BaseSigner class.

"""
from pkiexpress import standard_signature_policies
from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class BaseSigner(PkiExpressOperator):
    """

    Class containing all common fields and methods between signers and signature
    starters.

    """

    def __init__(self, config=None):
        if config is None:
            config = PkiExpressConfig()
        super(BaseSigner, self).__init__(config)

    def _verify_and_add_common_options(self, args):

        if standard_signature_policies.require_timestamp(
                self._signature_policy) and not self._timestamp_authority:
            raise Exception('The provided policy requires a timestamp '
                            'authority and none was provided')

        # Set the signature policy
        if self._signature_policy:
            args.append('--policy')
            args.append(self._signature_policy)

            # This operation evolved after version 1.5 to other signature
            # policies.
            if self._signature_policy is not \
                    standard_signature_policies.XML_DSIG_BASIC and \
                    self._signature_policy is not \
                    standard_signature_policies.NFE_PADRAO_NACIONAL:
                # This operation can only be used on versions greater than 1.5
                # of the PKI Express.
                self._version_manager.require_version('1.5')

            if self._signature_policy is \
                    standard_signature_policies.COD_WITH_SHA1 and \
                    self._signature_policy is \
                    standard_signature_policies.COD_WITH_SHA256:
                # These policies can only be used on version greater than 1.6
                # of the PKI Express.
                self._version_manager.require_version('1.6')

            if self._signature_policy is \
                    standard_signature_policies.PKI_BRAZIL_PADES_ADR_BASICA \
                    and self._signature_policy is \
                    standard_signature_policies\
                            .PKI_BRAZIL_PADES_ADR_BASICA_WITH_LTV \
                    and self._signature_policy is \
                    standard_signature_policies.PKI_BRAZIL_PADES_ADR_TEMPO:
                # These policies can only be used on version greater than 1.12
                # of the PKI Express.
                self._version_manager.require_version('1.12')

        # Add timestamp authority
        if self._timestamp_authority:
            self._timestamp_authority\
                .add_cmd_arguments(args, self._version_manager)

            # This option can only be used on version greater than 1.5 of the
            # PKI Express.
            self._version_manager.require_version('1.5')


__all__ = ['BaseSigner']
