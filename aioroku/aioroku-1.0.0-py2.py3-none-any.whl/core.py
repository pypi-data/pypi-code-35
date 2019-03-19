import logging
from urllib.parse import quote_plus

from aiohttp import client_exceptions
from aiologger import Logger

import xml.etree.ElementTree as ET

COMMANDS = {
    # Standard Keys
    'home': 'Home',
    'reverse': 'Rev',
    'forward': 'Fwd',
    'play': 'Play',
    'select': 'Select',
    'left': 'Left',
    'right': 'Right',
    'down': 'Down',
    'up': 'Up',
    'back': 'Back',
    'replay': 'InstantReplay',
    'info': 'Info',
    'backspace': 'Backspace',
    'search': 'Search',
    'enter': 'Enter',
    'literal': 'Lit',

    # For devices that support "Find Remote"
    'find_remote': 'FindRemote',

    # For Roku TV
    'volume_down': 'VolumeDown',
    'volume_up': 'VolumeUp',
    'volume_mute': 'VolumeMute',

    # For Roku TV while on TV tuner channel
    'channel_up': 'ChannelUp',
    'channel_down': 'ChannelDown',

    # For Roku TV current input
    'input_tuner': 'InputTuner',
    'input_hdmi1': 'InputHDMI1',
    'input_hdmi2': 'InputHDMI2',
    'input_hdmi3': 'InputHDMI3',
    'input_hdmi4': 'InputHDMI4',
    'input_av1': 'InputAV1',

    # For devices that support being turned on/off
    'power': 'Power',
    'poweroff': 'PowerOff',
}

SENSORS = ('acceleration', 'magnetic', 'orientation', 'rotation')
TOUCH_OPS = ('up', 'down', 'press', 'move', 'cancel')


class AioRokuException(Exception):
    pass


class Application:
    '''Application class with the icon property.'''

    def __init__(self, roku_id, version, name, roku=None,
                 is_screensaver=False):
        self.id = str(roku_id)
        self.version = version
        self.name = name
        self.is_screensaver = is_screensaver
        self.roku = roku

    def __eq__(self, other):
        return isinstance(other, Application) and \
            (self.id, self.version) == (other.id, other.version)

    def __repr__(self):
        return ('<Application: [%s] %s v%s>' %
                (self.id, self.name, self.version))

    @property
    def icon(self):
        if self.roku:
            return self.roku.icon(self)

    def launch(self):
        if self.roku:
            self.roku.launch(self)

    def store(self):
        if self.roku:
            self.roku.store(self)


class DeviceInfo:

    def __init__(self, model_name, model_num, software_version, software_build,
                 serial_num, user_device_name, roku_type):
        self.model_name = model_name
        self.model_num = model_num
        self.software_version = software_version
        self.software_build = software_build
        self.serial_num = serial_num
        self.user_device_name = user_device_name
        self.roku_type = roku_type

    def __repr__(self):
        return ('<DeviceInfo: %s-%s, SW v%s, Ser# %s (%s)>' %
                (self.model_name, self.model_num,
                 self.software_version, self.serial_num, self.roku_type))


class AioRoku:

    def __init__(self, host, session, port=8060):
        self.host = host
        self.port = port
        self.session = session
        self._sw_info = self.roku_type = self.dinfo = 'unknown'
        self.log = Logger.with_default_handlers(name=__name__ + '.AioRoku',
                                                level=logging.INFO)

    def __repr__(self):
        return "<AioRoku: %s:%s>" % (self.host, self.port)

    async def __getattr__(self, *args):
        if args[0] not in COMMANDS and args[0] not in SENSORS:
            raise AttributeError('%s is not a valid method' % args[0])

        elif args[0] in SENSORS:
            keys = ['%s.%s' % (args[0], axis) for axis in ('x', 'y', 'z')]
            params = dict(zip(keys, args))
            self.input(params)
        elif args[0] == 'literal':
            for char in args[1]:
                path = '/keypress/%s_%s' % (COMMANDS[args[0]],
                                            quote_plus(char))
                await self.request('POST', path)
        elif args[0] == 'search':
            keys = ['title', 'season', 'launch', 'provider', 'type']
            params = dict(zip(keys, args))
            path = '/search/browse'
            await self.request('POST', path)

        path = '/keypress/%s' % COMMANDS[args[0]]
        await self.request('POST', path)

    def __getitem__(self, key):
        key = str(key)
        app = self._app_for_name(key)
        if not app:
            app = self._app_for_id(key)
        return app

    def _app_for_name(self, name):
        for app in self.apps:
            if app.name == name:
                return app

    def _app_for_id(self, app_id):
        for app in self.apps:
            if app.id == app_id:
                return app

    async def request(self, method, path, params=None):
        url = 'http://%s:%s%s' % (self.host, self.port, path)
        await self.log.debug('HTTP: %s on %s', method, url)
        try:
            async with self.session.request(method, url, params=params) as res:
                await self.log.debug('%s Status: %s', res.headers, res.status)
                data = await res.read()
                return data
        except client_exceptions.ClientError as err:
            raise ValueError(err)

    @property
    async def sw_info(self):
        """Return the software version after it gets cached."""
        if self._sw_info == 'unknown':
            dinfo = await self.device_info
            self._sw_info = (dinfo.software_version, dinfo.software_build)
            return self._sw_info
        else:
            return self._sw_info

    @property
    async def apps(self):
        response = await self.request('get', '/query/apps')
        applications = deserialize_apps(response, self)
        for a in applications:
            a.roku = self
        return applications

    @property
    async def active_app(self):
        response = await self.request('get', '/query/active-app')
        active_app = deserialize_apps(response, self)
        if type(active_app) is Application:
            return active_app
        elif type(active_app) is list:
            return active_app[0]
        else:
            return None

    @property
    async def device_info(self):
        response = await self.request('get', '/query/device-info')
        root = ET.fromstring(response)

        self.roku_type = "Box"
        if root.find('is-tv') is not None and root.find(
                'is-tv').text == "true":
            self.roku_type = "TV"
        elif root.find('is-stick') is not None and \
                root.find('is-stick').text == "true":
            self.roku_type = "Stick"
        self.dinfo = DeviceInfo(
            model_name=root.find('model-name').text,
            model_num=root.find('model-number').text,
            software_version=root.find('software-version').text,
            software_build=root.find('software-build').text,
            serial_num=root.find('serial-number').text,
            user_device_name=root.find('user-device-name').text,
            roku_type=self.roku_type
            )
        return self.dinfo

    @property
    def commands(self):
        return sorted(COMMANDS.keys())

    @property
    async def power_state(self):
        response = await self.request('get', '/query/device-info')
        root = ET.fromstring(response)
        if root.find('power-mode').text:
            return root.find('power-mode').text

    def icon(self, app):
        return self.request('get', '/query/icon/%s' % app.id)

    async def launch(self, app):
        if app.roku and app.roku != self:
            raise AioRokuException('this app belongs to another Roku')
        launch_url = '/launch/%s' % app.id
        return await self.request('post', launch_url, {'contentID': app.id})

    async def store(self, app):
        return await self.request('post', '/launch/11',
                                  params={'contentID': app.id})

    async def input(self, params):
        return await self.request('post', '/input', params=params)

    async def touch(self, x, y, op='down'):

        if op not in TOUCH_OPS:
            raise AioRokuException('%s is not a valid touch operation' % op)

        params = {
            'touch.0.x': x,
            'touch.0.y': y,
            'touch.0.op': op,
        }

        await self.input(params)


def deserialize_apps(doc, roku_inst):

    applications = []
    root = ET.fromstring(doc)
    if root.find('screensaver') is not None:
        app_node = root.find('screensaver')
        return Application(roku_id=app_node.attrib['id'],
                           version=app_node.attrib['version'],
                           name=app_node.text,
                           is_screensaver=True,
                           roku=roku_inst)
    app_node = root.find('app')
    for elem in root:
        app = Application(roku_id=elem.get('id'), version=elem.get('version'),
                          name=elem.text, is_screensaver=False, roku=roku_inst)
        applications.append(app)
    return applications
