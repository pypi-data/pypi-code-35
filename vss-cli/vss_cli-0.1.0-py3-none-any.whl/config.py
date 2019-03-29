"""Configuration for VSS CLI (vss-cli)."""
import logging
import sys
from uuid import UUID
from typing import Any, Dict, List, Optional, Tuple, cast, Union  # noqa: F401
import platform
import click
import os
import json
from base64 import b64decode, b64encode
import vss_cli.const as const
from pyvss.manager import VssManager
from vss_cli import vssconst
from vss_cli.exceptions import VssCliError
from pyvss import __version__ as pyvss_version
from pick import pick
from vss_cli.validators import validate_email, validate_phone_number

_LOGGING = logging.getLogger(__name__)


class Configuration(VssManager):
    """The configuration context for the VSS CLI."""

    def __init__(self, tk: str = '') -> None:
        """Initialize the configuration."""
        super(Configuration, self).__init__(tk)
        self.user_agent = self._default_user_agent(
            extensions=f'pyvss/{pyvss_version}'
        )
        self.verbose = False  # type: bool
        self.server = const.DEFAULT_SERVER  # type: str
        self.output = const.DEFAULT_DATAOUTPUT  # type: str
        self.config = const.DEFAULT_CONFIG  # type: str
        self.history = const.DEFAULT_HISTORY  # type: str
        self.webdav_server = const.DEFAULT_WEBDAV_SERVER  # type: str
        self.username = None  # type: Optional[str]
        self.password = None  # type: Optional[str]
        self.token = None  # type: Optional[str]
        self.timeout = const.DEFAULT_TIMEOUT  # type: int
        self.debug = False  # type: bool
        self.showexceptions = False  # type: bool
        self.cert = None  # type: Optional[str]
        self.columns = None  # type: Optional[List[Tuple[str, str]]]
        self.no_headers = False
        self.table_format = 'plain'
        self.sort_by = None

    def get_token(self, user: str = '', password: str = ''):
        self.api_token = super(Configuration, self).get_token(user, password)
        return self.api_token

    def update_endpoints(self, endpoint: str = ''):
        """ Rebuilds API endpoints"""
        self.api_endpoint = f'{endpoint}/v2'
        self.base_endpoint = endpoint
        self.token_endpoint = f'{endpoint}/auth/request-token'

    def echo(self, msg: str, *args: Optional[Any]) -> None:
        """Put content message to stdout."""
        self.log(msg, *args)

    def log(  # pylint: disable=no-self-use
        self, msg: str, *args: Optional[str]
    ) -> None:  # pylint: disable=no-self-use
        """Log a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def secho(
            self, msg: str, *args: Optional[Any],
            **kwargs
    ) -> None:
        """Put content message to stdout with style."""
        self.slog(msg, *args, **kwargs)

    def slog(  # pylint: disable=no-self-use
        self, msg: str, *args: Optional[str],
        **kwargs,
    ) -> None:  # pylint: disable=no-self-use
        """Log a message to stdout with style."""
        if args:
            msg %= args
        click.secho(msg, file=sys.stdout, **kwargs)

    def vlog(self, msg: str, *args: Optional[str]) -> None:
        """Log a message only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def __repr__(self) -> str:
        """Return the representation of the Configuration."""
        view = {
            "server": self.server,
            "access-token": 'yes' if self.token is not None else 'no',
            "user": 'yes' if self.username is not None else 'no',
            "user-password": 'yes' if self.password is not None else 'no',
            "output": self.output,
            "verbose": self.verbose,
        }

        return "<Configuration({})".format(view)

    def auto_output(self, auto_output: str) -> str:
        """Configure output format."""
        if self.output == "auto":
            if auto_output == 'data':
                auto_output = const.DEFAULT_RAW_OUTPUT
            _LOGGING.debug("Setting auto-output to: %s", auto_output)
            self.output = auto_output
        return self.output

    @staticmethod
    def _default_user_agent(name: str = const.PACKAGE_NAME,
                            version: str = const.__version__,
                            extensions: str = ''):
        environment = {'product': name,
                       'product_version': version,
                       'python_version': platform.python_version(),
                       'system': platform.system(),
                       'system_version': platform.release(),
                       'platform_details': platform.platform(),
                       'extensions': extensions
                       }
        # User-Agent:
        # <product>/<version> (<system-information>)
        # <platform> (<platform-details>) <extensions>
        user_agent = '{product}/{product_version}' \
                     ' ({system}/{system_version}) ' \
                     'Python/{python_version} ({platform_details}) ' \
                     '{extensions}'.format(**environment)
        return user_agent

    def load_profile_from_config(self, endpoint):
        username, password, token = None, None, None
        profiles = self.load_raw_config_file()
        profile = profiles.get(endpoint)
        if profile:
            # get auth attr
            auth = profile.get('auth')
            # get token attr
            token = profile.get('token')
            if not auth or not token:
                raise Exception('Invalid configuration file')
            auth_enc = auth.encode()
            credentials_decoded = b64decode(auth_enc)
            # get user/pass
            username, password = \
                credentials_decoded.split(b':')
        return username, password, token

    def load_raw_config_file(self):
        try:
            with open(self.config, 'r') as f:
                profiles = json.load(f)
                return profiles
        except ValueError as ex:
            _LOGGING.error(
                f'Error loading configuration file: {ex}'
            )
            raise Exception('Invalid configuration file.')

    def load_config(self):
        try:
            if self.server:
                self.update_endpoints(self.server)
            # check for environment variables
            if self.token or (self.username and self.password):
                _LOGGING.debug(f'Loading from input')
                # don't load config file
                if self.token:
                    _LOGGING.debug(f'Checking token')
                    # set api token
                    self.api_token = self.token
                    return self.username, self.password, self.api_token
                elif self.username and self.password:
                    _LOGGING.debug(f'Checking user/pass to generate token')
                    # generate a new token - won't save
                    _LOGGING.warning(
                        'A new token will be generated but not persisted. '
                        'Consider running command "configure mk" to save your '
                        'credentials'
                    )
                    self.get_token(self.username, self.password)
                    _LOGGING.debug(f'Token generated {self.api_token}')
                    return self.username, self.password, self.api_token
                else:
                    raise VssCliError(
                        'Environment variables error. Please, verify '
                        'VSS_TOKEN or VSS_USER and VSS_USER_PASS')
            else:
                _LOGGING.debug(f'Loading configuration file: {self.config}')
                if os.path.isfile(self.config):
                    # read config and look for profile
                    self.username, self.password, self.api_token = \
                        self.load_profile_from_config(self.base_endpoint)
                    _LOGGING.debug(
                        f'Loaded from file {self.base_endpoint}:'
                        f' {self.username}'
                    )
                    creds = self.username and self.password
                    if not (creds or self.api_token):
                        raise VssCliError(
                            "Invalid endpoint {} configuration. \n "
                            "Please, run 'vss-cli configure mk' to add "
                            "endpoint to "
                            "configuration.".format(self.base_endpoint))
                    try:
                        self.whoami()
                        _LOGGING.debug('Token validated successfully.')
                    except Exception as ex:
                        self.vlog(str(ex))
                        _LOGGING.debug('Generating a new token')
                        self.api_token = self.get_token(
                            self.username,
                            self.password
                        )
                        _LOGGING.debug('Token generated successfully')
                        self.write_config_file(new_token=self.api_token)
                        # check for updates
                        # self.check_for_updates()
                        # check for unread messages
                        self.check_unread_messages()
                    return self.username, self.password, self.api_token
            raise VssCliError(
                "Invalid configuration. Please, run 'vss-cli "
                "configure mk' to initialize configuration."
            )
        except Exception as ex:
            raise VssCliError(str(ex))

    def check_unread_messages(self):
        try:
            _LOGGING.debug('Checking for unread messages')
            messages = self.get_user_messages(filter='status,eq,Created',
                                              per_page=100)
            n_messages = len(messages)
            if messages:
                envelope_str = vssconst.EMOJI_ENVELOPE.decode('utf-8')
                self.secho(
                    'You have {0} unread messages {1} '.format(
                        n_messages, envelope_str), fg='green', nl=False)
                self.secho('Run ', fg='green', nl=False)
                self.secho('vss-cli message ls', fg='red', nl=False)
                self.secho(' to list unread messages.', fg='green')
            else:
                _LOGGING.debug('No messages with Created status')
        except ValueError as ex:
            _LOGGING.error('Could not check for messages {}'.format(ex))

    def write_config_file(self, new_token=None):
        """
        Creates or updates configuration file with different
        endpoints.

        :param new_token: new api token to store
        :return:
        """
        token = new_token or self.get_token(self.username,
                                            self.password)
        username = self.username if isinstance(self.username, bytes) \
            else self.username.encode()
        password = self.password if isinstance(self.password, bytes) \
            else self.password.encode()
        credentials = b':'.join([username,
                                 password])
        config_dict = {self.base_endpoint: {
            'auth': b64encode(credentials).strip().decode('utf-8'),
            'token': token}
        }
        try:
            _LOGGING.debug(
                f'Writing configuration file:'
                f' {self.config}'
            )
            # validate if file exists
            if os.path.isfile(self.config):
                with open(self.config, 'r+') as fp:
                    try:
                        _conf_dict = json.load(fp)
                    except ValueError:
                        _conf_dict = {}
                    _conf_dict.update(config_dict)
                    fp.seek(0)
                    json.dump(_conf_dict, fp,
                              sort_keys=True,
                              indent=4)
                    fp.truncate()
            else:
                with open(self.config, 'w') as fp:
                    _conf_dict = config_dict
                    json.dump(_conf_dict, fp,
                              sort_keys=True,
                              indent=4)
        except IOError as e:
            raise VssCliError('An error occurred writing '
                              'configuration file: {}'.format(e))
        _LOGGING.debug(
            f'Successfully written'
            f' configuration file {self.config}'
        )

    def configure(self, username, password, endpoint, replace=False):
        self.username = username
        self.password = password
        # update instance endpoints if provided
        self.update_endpoints(endpoint)
        # directory available
        if not os.path.isdir(os.path.dirname(self.config)):
            os.mkdir(os.path.dirname(self.config))
        # config file
        if os.path.isfile(self.config):
            try:
                # load credentials by endpoint
                e_username, e_password, e_api_token = \
                    self.load_profile_from_config(self.base_endpoint)
                if not (e_username and e_password and e_api_token):
                    self.echo('Profile not found.')
                    self.write_config_file()

                if e_username and e_password and e_api_token:
                    confirm = replace or click.confirm(
                        'Would you like to replace existing configuration?')
                    if confirm:
                        self.write_config_file()
                else:
                    self.echo(
                        'Successfully configured credentials for {}. '
                        'You are ready to use '
                        'VSS CLI.'.format(self.base_endpoint))
            except VssCliError as ex:
                self.echo(str(ex))
                confirm = click.confirm(
                    'Would you like to replace existing configuration?'
                )
                if confirm:
                    self.write_config_file()
        else:
            self.write_config_file()

    def get_vskey_stor(self, **kwargs):
        from webdav3 import client as wc
        options = dict(
            webdav_login=self.username,
            webdav_password=self.password,
            webdav_hostname=self.webdav_server,
            verbose=self.verbose
        )
        self.vskey_stor = wc.Client(options=options)
        return self.vskey_stor.valid()

    def get_vm_by_uuid_or_name(
            self,
            uuid_or_name: str
    ):
        try:
            # is uuid?
            uuid = UUID(uuid_or_name)
            v = self.get_vm(str(uuid))
            if not v:
                raise click.BadArgumentUsage(
                    'uuid should be an existing Virtual Machine '
                    'or template'
                )
            return [v]
        except ValueError:
            # not an uuid
            _LOGGING.debug(f'not an uuid {uuid_or_name}')
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            # get vm by name
            g_vms = self.get_vms()
            uuid_or_name = uuid_or_name.lower()
            v = list(filter(
                lambda i: uuid_or_name in i['name'].lower(), g_vms)
            )
            if not v:
                raise click.BadParameter(
                    f'{uuid_or_name} could not be found'
                )
            v_count = len(v)
            if v_count > 1:
                msg = f"Found {v_count} matches. Please select one:"
                sel, index = pick(
                    title=msg, indicator='=>',
                    options=[f"{i['uuid']} ({i['name']})" for i in v]
                )
                return [v[index]]
            return v

    def get_domain_by_name_or_moref(
            self, name_or_moref: str
    ):
        g_domains = self.get_domains()
        name_or_moref = name_or_moref.lower()
        d = list(
            filter(
                lambda i: name_or_moref in i['name'].lower(), g_domains
            )
        ) or list(
            filter(
                lambda i: name_or_moref in i['moref'], g_domains
            )
        )
        if not d:
            raise click.BadParameter(
                f'{name_or_moref} could not be found'
            )
        d_count = len(d)
        if d_count > 1:
            msg = f"Found {d_count} matches. Please select one:"
            sel, index = pick(
                title=msg, indicator='=>',
                options=[f"{i['name']} ({i['moref']})" for i in d]
            )
            return [d[index]]
        return d

    def get_network_by_name_or_moref(
            self, name_or_moref: str
    ) -> List[Any]:
        g_networks = self.get_networks(sort='name')
        name_or_moref = name_or_moref.lower()
        # search by name or moref
        n = list(
            filter(
                lambda i: name_or_moref in i['name'].lower(),
                g_networks
            )
        ) or list(
            filter(
                lambda i: name_or_moref in i['moref'].lower(),
                g_networks
            )
        )
        if not n:
            raise click.BadParameter(
                f'{name_or_moref} could not be found'
            )
        net_count = len(n)
        if net_count > 1:
            msg = f"Found {net_count} matches. Please select one:"
            sel, index = pick(
                title=msg, indicator='=>',
                options=[f"{i['name']} ({i['moref']})" for i in n]
            )
            return [n[index]]
        return n

    def get_folder_by_name_or_moref_path(
            self, name_moref_path: str
    ) -> List[Any]:
        g_folders = self.get_folders(sort='path', summary=1)
        # search by name or moref
        name_moref_path = name_moref_path.lower()
        f = list(
            filter(
                lambda i: name_moref_path in i['name'].lower(),
                g_folders
            )
        ) or list(
            filter(
                lambda i: name_moref_path in i['path'].lower(),
                g_folders
            )
        ) or list(
            filter(
                lambda i: name_moref_path in i['moref'].lower(),
                g_folders
            )
        )

        if not f:
            raise click.BadParameter(
                f'{name_moref_path} could not be found'
            )
        f_count = len(f)
        if f_count > 1:
            msg = f"Found {f_count} matches. Please select one:"
            sel, index = pick(
                title=msg, indicator='=>',
                options=[f"{i['path']} ({i['moref']})" for i in f]
            )
            return [f[index]]
        return f

    def get_os_by_name_or_guest(
            self, name_or_guest: str
    ) -> List[Any]:
        g_os = self.get_os(sort='guestFullName,desc')
        try:
            o_f = list(
                filter(
                    lambda i: int(name_or_guest) == i['id'],
                    g_os
                )
            )
        except ValueError:
            # not an integer
            _LOGGING.debug(f'not an id {name_or_guest}')
            name_or_guest = name_or_guest.lower()
            o_f = list(
                filter(
                    lambda i: name_or_guest in i['guestId'].lower(),
                    g_os
                )
            ) or list(
                filter(
                    lambda i: name_or_guest in i['guestFullName'].lower(),
                    g_os
                )
            )
        if not o_f:
            raise click.BadParameter(
                f'{name_or_guest} could not be found'
            )
        o_count = len(o_f)
        if o_count > 1:
            msg = f"Found {o_count} matches. Please select one:"
            sel, index = pick(
                title=msg, indicator='=>',
                options=[f"{i['guestFullName']} ({i['guestId']})" for i in o_f]
            )
            return [o_f[index]]
        return o_f

    def get_vss_service_by_name_label_or_id(
            self,
            name_label_or_id: Union[str, int]
    ) -> List[Any]:
        vss_services = self.get_vss_services(show_all=True)
        try:
            svc_id = int(name_label_or_id)
            svc_ref = list(
                filter(
                    lambda i: i['id'] == svc_id, vss_services
                )
            )
        except ValueError as ex:
            # not an integer
            _LOGGING.debug(f'not an id {name_label_or_id} ({ex})')
            # checking name or label
            svc = str(name_label_or_id).lower()
            svc_ref = list(
                filter(
                    lambda i: svc in i['name'].lower(),
                    vss_services
                )
            ) or list(
                filter(
                    lambda i: svc in i['label'].lower(), vss_services
                )
            )
        # check if there's no ref
        if not svc_ref:
            raise click.BadParameter(
                f'{name_label_or_id} could not be found'
            )
        # count for dup results
        o_count = len(svc_ref)
        if o_count > 1:
            msg = f"Found {o_count} matches. Please select one:"
            sel, index = pick(
                title=msg, indicator='=>',
                options=[f"{i['label']}" for i in svc_ref]
            )
            return [svc_ref[index]]
        return svc_ref

    def get_iso_by_name_or_guest(
            self,
            name_or_path_or_id: Union[str, int]
    ) -> List[Any]:
        user_isos = self.get_user_isos()
        pub_isos = self.get_isos(show_all=True)
        try:
            iso_id = int(name_or_path_or_id)
            # public or user
            iso_ref = list(
                filter(
                    lambda i: i['id'] == iso_id, pub_isos
                )
            ) or list(
                filter(
                    lambda i: i['id'] == iso_id, user_isos
                )
            )
        except ValueError as ex:
            # not an integer
            _LOGGING.debug(f'not an id {name_or_path_or_id} ({ex})')
            # checking name or path
            # check in public and user isos
            iso = str(name_or_path_or_id)
            iso = iso.lower()
            iso_ref = list(
                filter(
                    lambda i: iso in i['name'].lower(), pub_isos
                )
            ) or list(
                filter(
                    lambda i: iso in i['path'].lower(), pub_isos
                )
            ) or list(
                filter(
                    lambda i: iso in i['name'].lower(), user_isos
                )
            ) or list(
                filter(
                    lambda i: iso in i['path'].lower(), user_isos
                )
            )
        # check if there's no ref
        if not iso_ref:
            raise click.BadParameter(
                f'{name_or_path_or_id} could not be found'
            )
        # count for dup results
        o_count = len(iso_ref)
        if o_count > 1:
            msg = f"Found {o_count} matches. Please select one:"
            sel, index = pick(
                title=msg, indicator='=>',
                options=[f"{i['name']}" for i in iso_ref]
            )
            return [iso_ref[index]]
        return iso_ref

    def get_vm_image_by_name_or_id_path(
            self,
            name_or_path_or_id: Union[str, int]
    ) -> List[Any]:
        user_imgs = self.get_user_vm_images()
        pub_imgs = self.get_images(show_all=True)
        try:
            img_id = int(name_or_path_or_id)
            # public or user
            img_ref = list(
                filter(
                    lambda i: i['id'] == img_id, pub_imgs
                )
            ) or list(
                filter(
                    lambda i: i['id'] == img_id, user_imgs
                )
            )
        except ValueError as ex:
            # not an integer
            _LOGGING.debug(f'not an id {name_or_path_or_id} ({ex})')
            # checking name or path
            # check in public and user img
            img = str(name_or_path_or_id)
            img = img.lower()
            img_ref = list(
                filter(
                    lambda i: img in i['name'].lower(), pub_imgs
                )
            ) or list(
                filter(
                    lambda i: img in i['path'].lower(), pub_imgs
                )
            ) or list(
                filter(
                    lambda i: img in i['name'].lower(), user_imgs
                )
            ) or list(
                filter(
                    lambda i: img in i['path'].lower(), user_imgs
                )
            )
        # check if there's no ref
        if not img_ref:
            raise click.BadParameter(
                f'{name_or_path_or_id} could not be found'
            )
        # count for dup results
        o_count = len(img_ref)
        if o_count > 1:
            msg = f"Found {o_count} matches. Please select one:"
            sel, index = pick(
                title=msg, indicator='=>',
                options=[f"{i['name']}" for i in img_ref]
            )
            return [img_ref[index]]
        return img_ref

    def get_spec_payload(
            self, payload: dict, built: str
    ) -> dict:
        spec_payload = dict()
        # sections
        machine_section = payload['machine']
        networking_section = payload['networking']
        metadata_section = payload['metadata']
        if built == 'os_install':
            # machine section parse and update
            spec_payload.update(machine_section)
            # replace with valid values
            spec_payload['os'] = self.get_os_by_name_or_guest(
                machine_section['os']
            )[0]['guestId']
            spec_payload['iso'] = self.get_iso_by_name_or_guest(
                machine_section['iso']
            )[0]['path']
            # folder
            spec_payload['folder'] = self.get_folder_by_name_or_moref_path(
                machine_section['folder']
            )[0]['moref']
            # networking
            spec_payload['networks'] = [
                self.get_network_by_name_or_moref(
                    n['network']
                )[0]['moref'] for n in networking_section['interfaces']
            ]
            # metadata section
            spec_payload.update(metadata_section)
            spec_payload['built'] = built
            spec_payload['bill_dept'] = metadata_section['billing']
            # optional
            if 'inform' in metadata_section:
                spec_payload['inform'] = [
                    validate_email(None, 'inform', i)
                    for i in metadata_section['inform']
                ]
            if 'vss_service' in metadata_section:
                service = self.get_vss_service_by_name_label_or_id(
                    metadata_section['vss_service']
                )[0]['id']
                spec_payload['vss_service'] = service
            if 'admin' in metadata_section:
                admin_name = metadata_section['admin']['name']
                admin_email = metadata_section['admin']['email']
                admin_phone = metadata_section['admin']['phone']
                if admin_name and admin_email and admin_phone:
                    validate_email(None, '', admin_email)
                    validate_phone_number(None, '', admin_phone)
                spec_payload['admin'] = f"{admin_name}:" \
                    f"{admin_phone}:{admin_email}"
        return spec_payload
