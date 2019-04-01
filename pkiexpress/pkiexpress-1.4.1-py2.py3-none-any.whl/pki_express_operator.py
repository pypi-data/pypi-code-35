import base64
import json
import os
import platform
import random
import tempfile

from abc import ABCMeta
from subprocess import Popen, PIPE
from distutils.version import StrictVersion

from .installation_not_found_error import InstallationNotFoundError
from .pki_express_config import PkiExpressConfig
from .version_manager import VersionManager


class PkiExpressOperator(object):
    __metaclass__ = ABCMeta

    COMMAND_SIGN_CADES = 'sign-cades'
    COMMAND_SIGN_PADES = 'sign-pades'
    COMMAND_SIGN_XML = 'sign-xml'
    COMMAND_START_CADES = 'start-cades'
    COMMAND_START_PADES = 'start-pades'
    COMMAND_START_XML = 'start-xml'
    COMMAND_COMPLETE_SIG = 'complete-sig'
    COMMAND_OPEN_PADES = 'open-pades'
    COMMAND_OPEN_CADES = 'open-cades'
    COMMAND_EDIT_PDF = 'edit-pdf'
    COMMAND_MERGE_CMS = 'merge-cms'
    COMMAND_START_AUTH = 'start-auth'
    COMMAND_COMPLETE_AUTH = 'complete-auth'
    COMMAND_STAMP_PDF = 'stamp-pdf'
    COMMAND_READ_CERT = 'read-cert'

    def __init__(self, config=None):
        self.__temp_files = []
        self.__file_references = {}

        if config is None:
            config = PkiExpressConfig()
        self._config = config
        self._version_manager = VersionManager()
        self._trusted_roots = []
        self._offline = False
        self._trust_lacuna_test_root = False
        self._signature_policy = None
        self._timestamp_authority = None
        self._crl_download_timeout = None
        self._ca_issuers_download_timeout = None

    def __del__(self):
        for temp_file in self.__temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def _invoke_plain(self, command, args=None):
        if args is None:
            args = []
        return self._invoke(command, args, True)

    def _invoke(self, command, args=None, plain_output=False):
        if args is None:
            args = []

        # Add PKI Express invocation arguments
        cmd_args = []
        for invocation_arg in self._get_pki_express_invocation():
            cmd_args.append(invocation_arg)

        # Add PKI Express command
        cmd_args.append(command)

        # Add PKI Express arguments
        cmd_args.extend(args)

        # Add file references if added
        if self.__file_references:
            for key, value in self.__file_references.items():
                cmd_args.append('--file-reference')
                cmd_args.append("%s=%s" % (key, value))

        # Add trust Lacuna test root if set
        if self._trust_lacuna_test_root:
            cmd_args.append('--trust-test')

        # Add offline option if provided
        if self._offline:
            cmd_args.append('--offline')
            # This option can only be used on versions greater than 1.2 of the
            # PKI Express
            self._version_manager.require_version('1.2')

        if self._crl_download_timeout:
            cmd_args.append('--crl-timeout')
            cmd_args.append(str(self._crl_download_timeout))
            # This option can only be used on versions greater than 1.12.2 of
            # the PKI Express
            self._version_manager.require_version('1.12.2')

        if self._ca_issuers_download_timeout:
            cmd_args.append('--ca-issuers-timeout')
            cmd_args.append(str(self._ca_issuers_download_timeout))
            # This option can only be used on versions greater than 1.12.2 of
            # the PKI Express
            self._version_manager.require_version('1.12.2')

        # Add base64 output option
        if not plain_output:
            cmd_args.append('--base64')

        # Verify the necessity of using the --min-version flag.
        if self._version_manager.require_min_version_flag:
            cmd_args.append('--min-version')
            cmd_args.append(self._version_manager.min_version.__str__())

        # Perform the "dotnet" command
        try:
            proc = Popen(cmd_args, stderr=PIPE, stdout=PIPE)
            (output, _), code = proc.communicate(), proc.returncode
        except OSError:
            raise InstallationNotFoundError('Could not find PKI Express\'s '
                                            'installation')

        if code != 0:
            split_output = output.decode('ascii').split(os.linesep)
            if code == 1 and \
                    self._version_manager.min_version > StrictVersion('1.0'):
                raise Exception('%s %s >>>>> TIP: This operation require '
                                'PKI Express %s, please check your PKI Express '
                                'version.' %
                                (split_output,
                                 os.linesep,
                                 self._version_manager.min_version))
            raise Exception(split_output)

        return output.decode('ascii').split(os.linesep)

    def _get_pki_express_invocation(self):

        # Identify OS
        if platform.system() == 'Linux':
            system = 'linux'
        elif platform.system() == 'Windows':
            system = 'win'
        else:
            raise Exception('Unsupported OS: %s' % platform.system())

        # Verify if the PKI Express home is set on configuration
        home = self._config.pki_express_home
        if home:

            if system == 'linux':
                if not os.path.exists(os.path.join(home, 'pkie.dll')):
                    raise InstallationNotFoundError(
                        "The file pkie.dll could not be found on directory %s" %
                        home)
            elif not os.path.exists(os.path.join(home, 'pkie.exe')):
                raise InstallationNotFoundError(
                    "The file pki.exe could not be found on directory %s" %
                    home)

        elif system == 'win':

            if os.path.exists(os.path.join(os.getenv('ProgramW6432'),
                                           'Lacuna Software',
                                           'PKI Express',
                                           'pkie.exe')):
                home = os.path.join(os.getenv('ProgramW6432'),
                                    'Lacuna Software',
                                    'PKI Express')

            elif os.path.exists(os.path.join(os.getenv('ProgramFiles(x86)'),
                                             'Lacuna Software',
                                             'PKI Express',
                                             'pkie.exe')):
                home = os.path.join(os.getenv('ProgramFiles(x86)'),
                                    'Lacuna Software',
                                    'PKI Express')

            elif os.path.exists(os.path.join(os.getenv('LOCALAPPDATA'),
                                             'Lacuna Software',
                                             'PKI Express',
                                             'pkie.exe')):
                home = os.path.join(os.getenv('LOCALAPPDATA'),
                                    'Lacuna Software',
                                    'PKI Express')

            elif os.path.exists(os.path.join(os.getenv('LOCALAPPDATA'),
                                             'Lacuna Software',
                                             'PKI Express (x86)',
                                             'pkie.exe')):
                home = os.path.join(os.getenv('LOCALAPPDATA'),
                                    'Lacuna Software',
                                    'PKI Express (x86)')

            if home is None or len(home) <= 0:
                raise InstallationNotFoundError(
                    'Could not determine the installation folder of PKI '
                    'Express. If you installed PKI Express on a custom folder, '
                    'make sure your are specifying it on the PkiExpressConfig '
                    'object')

        if system == 'linux':

            if home is not None:
                return ['dotnet', os.path.join(home, 'pkie.dll')]
            return ['pkie']

        return [os.path.join(home, 'pkie.exe')]

    def create_temp_file(self):
        file_desc, temp_file = tempfile.mkstemp(prefix='pkie',
                                                dir=self._config.temp_folder)
        os.close(file_desc)
        self.__temp_files.append(temp_file)
        return temp_file

    @staticmethod
    def get_transfer_file_name():
        n_bytes = 16
        rnd_bytes = random.getrandbits(n_bytes * 8)
        return hex(rnd_bytes)

    @staticmethod
    def _parse_output(data_base64):
        content = base64.standard_b64decode(str(data_base64))
        obj_dict = json.loads(content)
        return obj_dict

    def add_file_reference(self, alias, path):
        if path is None or not os.path.exists(path):
            raise Exception('The provided file path was not found')

        self.__file_references[alias] = path

    def add_trusted_root(self, path):
        if path is None or not os.path.exists(path):
            raise Exception('The provided trusted root was not found')
        self._trusted_roots.append(path)

    @property
    def offline(self):
        return self._offline

    @offline.setter
    def offline(self, value):
        self._offline = value

    @property
    def trust_lacuna_test_root(self):
        return self._trust_lacuna_test_root

    @trust_lacuna_test_root.setter
    def trust_lacuna_test_root(self, value):
        self._trust_lacuna_test_root = value

    @property
    def signature_policy(self):
        return self._signature_policy

    @signature_policy.setter
    def signature_policy(self, value):
        self._signature_policy = value

    @property
    def timestamp_authority(self):
        return self._timestamp_authority

    @timestamp_authority.setter
    def timestamp_authority(self, value):
        self._timestamp_authority = value

    # region "crl_download_timeout" accessors

    @property
    def crl_download_timeout(self):
        return self.__get_crl_download_timeout()

    def __get_crl_download_timeout(self):
        return self._crl_download_timeout

    @crl_download_timeout.setter
    def crl_download_timeout(self, value):
        self.__set_crl_download_timeout(value)

    def __set_crl_download_timeout(self, value):
        if value is None:
            raise Exception('The provided "crl_download_timeout" is not valid')
        self._crl_download_timeout = value

    # endregion

    # region "ca_issuers_download_timeout" accessors

    @property
    def ca_issuers_download_timeout(self):
        return self.__get_ca_issuers_download_timeout()

    def __get_ca_issuers_download_timeout(self):
        return self._ca_issuers_download_timeout

    @ca_issuers_download_timeout.setter
    def ca_issuers_download_timeout(self, value):
        self.__set_ca_issuers_download_timeout(value)

    def __set_ca_issuers_download_timeout(self, value):
        if value is None:
            raise Exception('The provided "ca_issuers_download_timeout" is not '
                            'valid')
        self._ca_issuers_download_timeout = value

    # endregion


__all__ = ['PkiExpressOperator']
