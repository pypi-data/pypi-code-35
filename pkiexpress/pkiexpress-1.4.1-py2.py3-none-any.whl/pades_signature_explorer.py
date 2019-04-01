from .pades_signature import PadesSignature
from .pki_express_config import PkiExpressConfig
from .signature_explorer import SignatureExplorer


class PadesSignatureExplorer(SignatureExplorer):

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(PadesSignatureExplorer, self).__init__(config)

    def open(self):
        if self._signature_file_path is None:
            raise Exception('The signature file was not set')

        args = [self._signature_file_path]

        if self._validate:
            args.append('--validate')

        # This operation can only be used on versions greater than 1.3 of the
        # PKI Express.
        self._version_manager.require_version('1.3')

        # Invoke command.
        response = self._invoke(self.COMMAND_OPEN_PADES, args)
        output = PadesSignatureExplorer._parse_output(response[0])
        return PadesSignature(output)


__all__ = ['PadesSignatureExplorer']
