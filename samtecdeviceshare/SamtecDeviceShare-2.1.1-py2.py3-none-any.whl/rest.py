import os
import glob
import tempfile
import copy
import zipfile
from functools import partial
import asyncio
from asyncio import CancelledError, shield
from concurrent.futures import ThreadPoolExecutor
import lockfile
import aiohttp
from aiohttp import web
import aiohttp_cors
from .helper import isOnline, getIPAddress, setupWIFIHotSpot, setupWIFIClient
from .ethernethandler import EthernetHandler
from .logger import setupLogger
CUR_DIR = os.path.dirname(os.path.realpath(__file__))

logger = setupLogger()

# pylint: disable=too-many-instance-attributes,too-many-public-methods
class SamtecDeviceShare:
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=12)
        self.loop = asyncio.get_event_loop()
        self.loop.set_default_executor(self.pool)

        # Balena provided env vars
        prefix = 'BALENA' if os.getenv('BALENA') else 'RESIN' if os.getenv('RESIN') else 'DEBUG'
        self.onDevice = os.getenv('BALENA', None) is not None
        self.deviceUUID = os.getenv(prefix+'_DEVICE_UUID', '0000000')
        self.deviceType = os.getenv(prefix+'_DEVICE_TYPE', 'raspberrypi3')
        self.appId = int(os.getenv(prefix+'_APP_ID', '0'))
        self.appName = os.getenv(prefix+'_APP_NAME')
        self.appUpdateLockPath = os.getenv(prefix+'_APP_LOCK_PATH', '/tmp/balena.lock')
        self.appUpdateCheck = False
        # BALENA_APP_RELEASE
        # Use version to determine capabilities (RESIN OR BALENA, commit, etc)
        self.supervisorVersion = os.getenv(prefix+'_SUPERVISOR_VERSION', '0.0.0')
        self.supervisorAddress = os.getenv(prefix+'_SUPERVISOR_ADDRESS', 'http://localhost:48484')
        self.supervisorAPIKey = os.getenv(prefix+'_SUPERVISOR_API_KEY', '')
        self.supervisorSession = None
        self.supervisorParams = {'apikey': self.supervisorAPIKey}

        self.appVersion = os.getenv('APP_VERSION', '0.0.0')
        self.appLogPath = os.getenv('APP_LOG_PATH', '/tmp/logs')
        self.sdcWIFIType = os.getenv('SDC_WIFI_TYPE', 'HOTSPOT').upper() # HOTSPOT, CLIENT
        self.sdcWIFISSID = os.getenv('SDC_WIFI_SSID', 'SDC-'+self.deviceUUID[:7])
        self.sdcWIFIPass = os.getenv('SDC_WIFI_PASS', 'samtec1!')
        self.appWebPort = int(os.getenv('APP_WEB_PORT', '80'))
        self.appImgPath = os.getenv('APP_IMG_PATH', os.path.join(CUR_DIR, '../static/img.png'))
        self.appImg = b''

        self.appLockHandler = lockfile.LockFile(
            os.path.splitext(self.appUpdateLockPath)[0]
        ) if self.appUpdateLockPath else None
        self.ethernetHandler = EthernetHandler()
        self.internetAccess = False
        self.deviceState = {
            'status': 'IDLE',
            'appCommit': None,
            'appVersion': self.appVersion,
            'appDownloadProgress': 0,
            'appUpdateAvailable': False,
            'appDownloading': False,
            'appUpdating': False,
            'appUpdateCheck': self.appUpdateCheck,
            'ipAddress': '',
            'deviceUUID': self.deviceUUID,
            'internetAccess': False,
            'apMode': False
        }
        self.config = {}
        self.app = None

    async def checkInternetAccess(self):
        self.internetAccess = await shield(self.loop.run_in_executor(self.pool, isOnline))
        return self.internetAccess

    async def launchDefaultWIFI(self):
        if self.sdcWIFIType == 'HOTSPOT':
            await self.launchHotSpot()
        elif self.sdcWIFIType == 'CLIENT':
            await self.launchWIFIClient()
        else:
            logger.warning('Invalid default WIFI setup provided')

    async def launchHotSpot(self, credentials=None):
        if credentials is None:
            credentials = {'ssid': self.sdcWIFISSID, 'passphrase': self.sdcWIFIPass}
        if not isinstance(credentials.get('ssid', None), str) or \
           not isinstance(credentials.get('passphrase', None), str):
            raise TypeError('Invalid wifi config json file. Requires both ssid and passphrase')
        routine = partial(
            setupWIFIHotSpot,
            ssid=credentials['ssid'],
            passphrase=credentials['passphrase'],
            action='UP',
            timeout=20
        )
        await shield(self.loop.run_in_executor(self.pool, routine))

    async def launchWIFIClient(self, credentials=None):
        if credentials is None:
            credentials = {'ssid': self.sdcWIFISSID, 'passphrase': self.sdcWIFIPass}
        if not isinstance(credentials.get('ssid', None), str) or \
           not isinstance(credentials.get('passphrase', None), str):
            raise TypeError('Invalid wifi config json file. Requires both ssid and passphrase')
        routine = partial(
            setupWIFIClient,
            ssid=credentials['ssid'],
            passphrase=credentials['passphrase'],
            identity=credentials.get('identity', None),
            action=credentials.get('action', 'UP'),
            timeout=20
        )
        await shield(self.loop.run_in_executor(self.pool, routine))

    def getLogZipData(self):
        zipPath = os.path.join(tempfile.gettempdir(), 'app_logs.zip')
        zipfp = zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED)
        for logFile in glob.glob(os.path.join(self.appLogPath, '*.log')):
            zipfp.write(logFile, os.path.basename(logFile))
        zipfp.close()
        with open(zipPath, 'rb') as fp:
            data = fp.read()
        return data

    def setLockFile(self, lockHandler, lock, timeout=5):
        if lockHandler is None:
            raise Exception('Invalid lock handler provided')
        if lock == lockHandler.is_locked():
            logger.warning('Lock file already set')
        elif lock:
            try:
                lockHandler.acquire(timeout=timeout)
            except lockfile.LockError as err:
                raise err
            logger.info('Lock file successfully locked')
        else:
            try:
                lockHandler.release()
            except lockfile.UnlockError as err:
                logger.warning('Forcefully breaking lock file.')
                lockHandler.break_lock()
            logger.info('Lock file successfully unlocked')

    async def setAppLock(self, locked, timeout=5):
        if self.appUpdateLockPath:
            routine = partial(
                self.setLockFile,
                lockHandler=self.appLockHandler,
                lock=locked,
                timeout=timeout
            )
            await shield(self.loop.run_in_executor(self.pool, routine))

    async def startBackgroundTasks(self, app):
        # try:
        #     with open(os.path.join(CUR_DIR, '../static/config.json'), 'r') as fp:
        #         config = json.load(fp)
        #         self.config = config
        # except Exception as err:
        #     logger.exception('Failed loading config file w/ error: %s', err)
        try:
            await self.checkInternetAccess()
            await self.setAppLock(locked=True, timeout=5)
        except Exception as err:
            logger.exception('Failed acquiring lock w/ error: %s', err)
        try:
            await self.launchDefaultWIFI()
        except Exception as err:
            logger.exception('Failed launching hotspot w/ error: %s', err)
        try:
            with open(self.appImgPath, 'rb') as fp:
                self.appImg = fp.read()
        except Exception as err:
            logger.exception('Failed loading app image w/ error: %s', err)
        try:
            await self.updateDeviceState(force=True)
        except Exception as err:
            logger.exception('Failed updating device state w/ error: %s', err)
        app['dispatch'] = app.loop.create_task(self.processQueue())

    async def cleanupBackgroundTasks(self, app):
        app['dispatch'].cancel()
        await app['dispatch']
        if self.supervisorSession and not self.supervisorSession.closed:
            await self.supervisorSession.close()

    async def on_shutdown(self, app):
        logger.warning('Server shutting down')

    async def processQueue(self):
        while True:
            try:
                await asyncio.sleep(1)
                await self.updateNetworkRoutine()
                await asyncio.sleep(1)
                await self.updateNetworkRoutine()
                await asyncio.sleep(1)
                await self.updateNetworkRoutine()
                await self.updateDeviceState()
                await self.checkInternetAccess()
            except CancelledError:
                logger.warning('Background task(s) cancelled')
                return
            except Exception as err:
                logger.exception('Failed performing update routine w/ error: %s', err)

    async def updateNetworkRoutine(self):
        operation = None
        try:
            operation = shield(self.loop.run_in_executor(self.pool, self.ethernetHandler.update))
            await operation
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed updating network due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed updating network w/ error: %s', err)
            raise err

    async def getAppDataRequest(self, request):
        try:
            return web.json_response(dict(
                type=self.appName,
                port=self.appWebPort
            ))
        except Exception as err:
            logger.exception('Failed to get app data due to error: %s', err)
            return web.Response(status=400, text='Failed to get app data due to error: {0}'.format(err))

    async def getAppImgRequest(self, request):
        # SDC expects this to return binary and not base64 encoded string
        try:
            return web.Response(
                headers={'Content-Type': 'application/octet-stream'},
                status=200, body=self.appImg
            )
        except Exception as err:
            logger.exception('Failed to get app image due to error: %s', err)
            return web.Response(status=400, text='Failed to get app image due to error: {0}'.format(err))

    async def getDeviceState(self):
        return copy.deepcopy(self.deviceState)

    # pylint: disable=too-many-locals
    async def updateDeviceState(self, force=False):
        internetAccess = self.internetAccess
        ipAddress = ' '.join([getIPAddress(ifname) for ifname in ['eth0', 'wlan0']])
        appCommit = self.deviceState.get('appCommit', None)
        self.deviceState.update({
            'internetAccess': internetAccess,
            'ipAddress': ipAddress,
            'apMode': '10.42.0.1' in ipAddress,
            'appUpdateCheck': self.appUpdateCheck
        })
        if internetAccess or force:
            appDownloading = False
            appDownloaded = True
            appDownloadProgress = 0
            appUpdating = False
            appUpdateAvailable = False
            uri = self.supervisorAddress+'/v1/device'
            async with self.supervisorSession.get(uri, params=self.supervisorParams) as resp:
                deviceState = await resp.json()
            updatePending = deviceState.get('update_pending', False)
            uri = self.supervisorAddress+'/v2/applications/state'
            async with self.supervisorSession.get(uri, params=self.supervisorParams) as resp:
                appState = await resp.json()
            services = appState.get(self.appName, {}).get('services', {})
            # pylint: disable=unused-variable
            for (serviceName, serviceState) in services.items():
                serviceStatus = serviceState.get('status', 'IDLE').upper()
                serviceUpdating = serviceStatus == 'INSTALLING'
                serviceDownloading = serviceStatus == 'DOWNLOADING'
                serviceDownloaded = serviceStatus == 'DOWNLOADED'
                appDownloadProgress += serviceState.get('downloadProgress', 0) or 0 if serviceDownloading else 100
                appDownloading |= serviceDownloading
                appDownloaded &= serviceDownloaded
                appUpdating |= serviceUpdating
            appDownloadProgress /= max(1, len(services.keys()))
            appUpdateAvailable = (appDownloaded or updatePending) and not appUpdating
            self.deviceState.update({
                'appDownloading': appDownloading and internetAccess,
                'appDownloadProgress': appDownloadProgress,
                'appUpdateAvailable': appUpdateAvailable,
                'appUpdating': appUpdating,
                'status': 'INSTALLING' if appUpdating else 'DOWNLOADING' if appDownloading else 'IDLE'
            })
            appCommit = appState.get(self.appName, {}).get('commit', appCommit)
        if appCommit is None and force:
            uri = self.supervisorAddress+'/v1/device'
            async with self.supervisorSession.get(uri, params=self.supervisorParams) as resp:
                deviceState = await resp.json()
            appCommit = deviceState.get('commit', None)
        if appCommit is not None:
            self.deviceState.update({
                'appCommit': appCommit
            })
        return copy.deepcopy(self.deviceState)

    async def supervisorUpdateCheck(self, force=False):
        uri = self.supervisorAddress+'/v1/update'
        status = 400
        async with self.supervisorSession.post(uri, params=self.supervisorParams, json=dict(force=force)) as resp:
            status = resp.status
        return status

    async def getAppLogsRequest(self, request):
        try:
            logger.info('GET /api/v2/app/logs')
            data = await shield(self.loop.run_in_executor(self.pool, self.getLogZipData))
            return web.Response(
                headers={'Content-Type': 'application/octet-stream'},
                status=200, body=data
            )
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed to get app logs due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed to get app logs due to error: %s', err)
            return web.Response(status=400, text='Failed to get app logs due to error: {0}'.format(err))

    async def getDeviceStateRequest(self, request):
        try:
            deviceState = await self.getDeviceState()
            return web.json_response(deviceState)
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed to get device state due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed to get device state due to error:  %s', err)
            return web.Response(status=400, text='Failed to get device state due to error: {0}'.format(err))

    async def getAppStateRequest(self, request):
        try:
            uri = self.supervisorAddress+'/v2/applications/state'
            async with self.supervisorSession.get(uri, params=self.supervisorParams) as resp:
                appState = await resp.json()
            return web.json_response(appState)
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed to get app state due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed to get app state due to error:  %s', err)
            return web.Response(status=400, text='Failed to get app state due to error: {0}'.format(err))

    async def performBlinkRequest(self, request):
        try:
            logger.info('POST /api/v2/device/blink')
            uri = self.supervisorAddress+'/v1/blink'
            status = 400
            async with self.supervisorSession.post(uri, params=self.supervisorParams) as resp:
                status = resp.status
            return web.Response(status=status, text='Success' if status == 200 else 'Failure')
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed to perform blink due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed to perform blink due to error: %s', err)
            return web.Response(status=400, text='Failed to perform blink due to error: {0}'.format(err))

    async def performRestartRequest(self, request):
        try:
            logger.info('POST /api/v2/device/restart')
            await self.setAppLock(locked=False)
            uri = self.supervisorAddress+'/v1/reboot'
            status = 400
            async with self.supervisorSession.post(uri, params=self.supervisorParams) as resp:
                status = resp.status
            return web.Response(status=status, text='Success' if status == 202 else 'Failure')
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed to perform restart due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed to perform restart due to error: %s', err)
            return web.Response(status=400, text='Failed to perform restart due to error: {0}'.format(err))

    async def performOTAUpdateCheck(self, credentials):
        try:
            self.appUpdateCheck = True
            # Already online so just use it
            internetAccess = await self.checkInternetAccess()
            if internetAccess:
                await shield(self.supervisorUpdateCheck(force=False))
                await asyncio.sleep(1)
                self.appUpdateCheck = False
                return
            # Connect to supplied network
            if credentials is None:
                raise Exception('No internet access and no/invalid Wi-Fi credentials provided.')
            # peername = request.transport.get_extra_info('peername')
            # host, port = peername if peername is not None else '', ''
            # if '10.42.' in host:
            #     raise Exception('Cant join another Wi-Fi network when client is connected via Acess Point')
            await self.launchWIFIClient(credentials)
            numAttempts = 0
            online = False
            while numAttempts < 20:
                online = await self.checkInternetAccess()
                if online:
                    break
                numAttempts += 1
                await asyncio.sleep(1)
            if not online:
                raise Exception('Timeout reached trying to contact server.')
            # Trigger supervisor to check for an update
            logger.info('OTA Update Check: Started')
            await self.updateDeviceState()
            await asyncio.sleep(20)
            logger.info('OTA Update Check: Request update')
            await self.supervisorUpdateCheck(force=False)
            await asyncio.sleep(20)
            appDownloading = True
            while appDownloading:
                logger.info('OTA Update Check: Waiting for potential app update to complete')
                deviceState = await self.updateDeviceState()
                appDownloading = deviceState.get('appDownloading', False)
                await asyncio.sleep(10)
            logger.info('OTA Update Check: Finished')
            await self.updateDeviceState()
            await self.launchDefaultWIFI()
            self.appUpdateCheck = False
            return
        except Exception as err:
            logger.exception('OTA Update Check: Failed due to error: %s', err)
            await self.launchDefaultWIFI()
            self.appUpdateCheck = False
            raise err

    async def performAppUpdateCheckRequest(self, request):
        try:
            logger.info('POST /api/v2/app/update/check')
            if self.appUpdateCheck:
                return web.Response(status=204, text='Success')
            credentials = None
            try:
                credentials = await request.json()
            except Exception:
                credentials = None
            operation = shield(self.performOTAUpdateCheck(credentials))
            await operation
            return web.Response(status=204, text='Success')
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed to perform update check due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed to perform update check due to error: %s', err)
            return web.Response(status=400, text='Failed to perform update check due to error: {0}'.format(err))

    async def performAppUpdateRequest(self, request):
        try:
            logger.info('POST /api/v2/app/update/install')
            deviceState = await self.updateDeviceState()
            if deviceState['appUpdating']:
                return web.Response(status=204, text='Success')
            if deviceState['appDownloading']:
                return web.Response(status=400, text='App update still downloading')
            await self.supervisorUpdateCheck(force=False)
            if not deviceState['appUpdateAvailable']:
                return web.Response(status=400, text='No app update available')
            # Remove update lock file
            await self.setAppLock(locked=False)
            await self.supervisorUpdateCheck(force=True)
            return web.Response(status=204, text='Success')
        except (CancelledError, ConnectionResetError) as err:
            logger.exception('Failed to perform update due to cancelled or reset error: %s', err)
            raise err
        except Exception as err:
            logger.exception('Failed to perform update due to error: %s', err)
            return web.Response(status=400, text='Failed to perform update due to error: {0}'.format(err))

    async def getWIFICredentialsRequest(self, request):
        try:
            logger.info('GET /api/v2/network/wifi/credentials')
            return web.json_response([
                'unknown'
            ])
        except Exception as err:
            logger.exception('Failed to get wifi credentials due to error:  %s', err)
            return web.Response(status=400, text='Failed to get wifi credentials due to error: {0}'.format(err))

    async def updateWIFICredentialsRequest(self, request):
        try:
            logger.info('POST /api/v2/network/wifi/credentials')
            credentials = await request.json()
            await self.launchWIFIClient(credentials)
            return web.Response(status=200, text='Success')
        except Exception as err:
            logger.exception('Failed to update wifi credentials due to error: %s', err)
            return web.Response(status=400, text='Failed to update wifi credentials due to error: {0}'.format(err))

    async def enableHotspotRequest(self, request):
        try:
            logger.info('POST /api/v2/network/wifi/hotspot')
            await self.launchHotSpot()
            return web.Response(status=200, text='Success')
        except Exception as err:
            logger.exception('Failed to enable hotspot due to error: %s', err)
            return web.Response(status=400, text='Failed to enable hotspot due to error: {0}'.format(err))

    async def createApp(self):
        self.supervisorSession = aiohttp.ClientSession()
        app = web.Application()
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods='*'
            )
        })
        # Support legacy routines
        app.router.add_get('/data.json', self.getAppDataRequest)
        app.router.add_get('/img.png', self.getAppImgRequest)

        # New routines
        app.router.add_get('/api/v2/device', self.getDeviceStateRequest)
        app.router.add_get('/api/v2/app', self.getAppStateRequest)
        app.router.add_get('/api/v2/app/logs', self.getAppLogsRequest)
        app.router.add_get('/api/v2/network/wifi/credentials', self.getWIFICredentialsRequest)
        app.router.add_post('/api/v2/device/blink', self.performBlinkRequest)
        app.router.add_post('/api/v2/device/restart', self.performRestartRequest)
        app.router.add_post('/api/v2/app/update/check', self.performAppUpdateCheckRequest)
        app.router.add_post('/api/v2/app/update/install', self.performAppUpdateRequest)
        app.router.add_post('/api/v2/network/wifi/credentials', self.updateWIFICredentialsRequest)
        app.router.add_post('/api/v2/network/wifi/hotspot', self.enableHotspotRequest)
        for route in list(app.router.routes()):
            cors.add(route)
        return app

    def runApp(self, host, port):
        try:
            loop = self.loop
            app = loop.run_until_complete(self.createApp())
            app.on_startup.append(self.startBackgroundTasks)
            app.on_cleanup.append(self.cleanupBackgroundTasks)
            self.app = app
            web.run_app(app, host=host, port=port, handle_signals=False)
        except Exception as err:
            raise err


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description='SDS Rest Server.'
    # )
    # parser.add_argument(
    #     '--configpath',
    #     type=str,
    #     help='Path to the config json file.',
    #     default=None
    # )
    sds = SamtecDeviceShare()
    try:
        sds.runApp(
            host=os.getenv('REST_ADDRESS', '0.0.0.0'),
            port=int(os.getenv('REST_PORT', '47546'))
        )
    except KeyboardInterrupt:
        logger.warning('Exiting... due to sigkill')
    except Exception as err:
        logger.exception('Uncaught exception: %s', err)
